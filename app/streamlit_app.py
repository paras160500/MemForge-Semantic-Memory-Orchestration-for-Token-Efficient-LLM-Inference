import streamlit as st

from config.settings import (
    OPENAI_CHAT_MODEL,
    OPENAI_EMBEDDING_MODEL,
    OPENAI_EMBEDDING_DIMENSIONS,
)
from database.mongodb import MongoDB
from memory.store import MemoryStore
from memory.classifier import InputClassfier
from memory.extractor import FactExtractor
from memory.updater import MemoryUpdater
from memory.retriever import MemoryRetriever
from llm.client import OpenAIClient
from llm.embeddings import EmbeddingService
from llm.prompts import build_answer_prompt
from app.ui import (
    setup_page,
    render_header,
    render_sidebar,
    render_memory_card,
    render_result,
)


# ============================================================
# PAGE SETUP
# ============================================================

setup_page()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ============================================================
# INITIALIZE SERVICES
# ============================================================

@st.cache_resource
def initialize_services():
    database = MongoDB()
    database.test_connection()

    memory_store = MemoryStore(database)
    classifier = InputClassfier()
    extractor = FactExtractor()
    updater = MemoryUpdater(memory_store)
    retriever = MemoryRetriever(memory_store)
    llm = OpenAIClient()
    embeddings = EmbeddingService()

    return {
        "database": database,
        "memory_store": memory_store,
        "classifier": classifier,
        "extractor": extractor,
        "updater": updater,
        "retriever": retriever,
        "llm": llm,
        "embeddings": embeddings,
    }


try:
    services = initialize_services()
except Exception as error:
    st.error("❌ Failed to initialize application.")
    st.exception(error)
    st.stop()


# ============================================================
# SERVICES
# ============================================================

database = services["database"]
memory_store = services["memory_store"]
classifier = services["classifier"]
extractor = services["extractor"]
updater = services["updater"]
retriever = services["retriever"]
llm = services["llm"]
embeddings = services["embeddings"]


# ============================================================
# HEADER
# ============================================================

render_header()


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(
    memory_count=memory_store.count(),
    embedding_dimensions=embeddings.get_embedding_dimensions(),
    model_name=OPENAI_CHAT_MODEL,
    embedding_model=OPENAI_EMBEDDING_MODEL,
)


# ============================================================
# TABS
# ============================================================

chat_tab, memory_tab, architecture_tab = st.tabs(
    [
        "💬 Chat",
        "🧠 Memory",
        "🏗️ Architecture",
    ]
)


# ============================================================
# CHAT TAB
# ============================================================

with chat_tab:
    st.subheader("Talk to your AI")
    st.caption(
        "Statements can become long-term memories. "
        "Questions retrieve relevant memories."
    )

    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------------------------------------------------------
    # USER INPUT
    # --------------------------------------------------------

    user_input = st.chat_input(
        "Tell me something or ask me a question..."
    )

    if user_input:
        # ----------------------------------------------------
        # SHOW USER MESSAGE
        # ----------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        # ----------------------------------------------------
        # CLASSIFY INPUT
        # ----------------------------------------------------

        with st.spinner("Analyzing your message..."):
            classification = classifier.classify(user_input)

        # ====================================================
        # STATEMENT
        # ====================================================

        if classification == "statement":
            with st.chat_message("assistant"):
                st.markdown("🧠 **Statement detected**")

                # --------------------------------------------
                # EXTRACT FACTS
                # --------------------------------------------

                with st.spinner("Extracting useful information..."):
                    recent_context = ""

                    if st.session_state.messages:
                        recent_messages = st.session_state.messages[-6:]
                        recent_context = "\n".join(
                            f"{msg['role']}: {msg['content']}"
                            for msg in recent_messages
                        )

                    facts = extractor.extract_facts(
                        statement=user_input,
                        recent_context=recent_context,
                    )

                if not facts:
                    response_text = (
                        "I couldn't find any useful long-term "
                        "information to store from that statement."
                    )

                    st.markdown(response_text)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response_text,
                        }
                    )
                else:
                    st.markdown(
                        f"Found **{len(facts)}** useful fact(s)."
                    )

                    all_results = []

                    # ----------------------------------------
                    # PROCESS EACH FACT
                    # ----------------------------------------

                    for fact_index, fact in enumerate(facts, start=1):
                        st.markdown(
                            f"**Fact {fact_index}:** {fact}"
                        )

                        with st.spinner("Updating memory..."):
                            result = updater._process_fact(
                                fact=fact,
                                turn_index=len(
                                    st.session_state.messages
                                ),
                            )

                        all_results.append(result)
                        render_result(result)

                    response_text = (
                        "I've processed the information and "
                        "updated my long-term memory."
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": response_text,
                        }
                    )

        # ====================================================
        # QUERY
        # ====================================================

        else:
            with st.chat_message("assistant"):
                with st.spinner("Searching memory..."):
                    relevant_memories = retriever.retrieve(user_input)

                # --------------------------------------------
                # DISPLAY RETRIEVED MEMORY
                # --------------------------------------------

                if relevant_memories:
                    st.markdown("### 🧠 Relevant Memories")

                    for memory, score in relevant_memories:
                        render_memory_card(memory, score)

                # --------------------------------------------
                # BUILD CONTEXT
                # --------------------------------------------

                memory_context = retriever.format_memories(
                    relevant_memories
                )

                # --------------------------------------------
                # ASK CHATGPT
                # --------------------------------------------

                with st.spinner("Generating answer..."):
                    answer_prompt = build_answer_prompt(
                        query=user_input,
                        relevant_memories=memory_context,
                    )

                    response = llm.chat(
                        [
                            {
                                "role": "system",
                                "content": (
                                    "You are a helpful "
                                    "AI assistant."
                                ),
                            },
                            {
                                "role": "user",
                                "content": answer_prompt,
                            },
                        ],
                        temperature=0,
                    )

                answer = response["content"]
                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )


# ============================================================
# MEMORY TAB
# ============================================================

with memory_tab:
    st.subheader("🧠 Long-Term Memory")

    memory_count = memory_store.count()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Memories", memory_count)

    with col2:
        st.metric(
            "Embedding Dimensions",
            embeddings.get_embedding_dimensions(),
        )

    st.divider()

    memories = memory_store.get_all()

    if not memories:
        st.info("No memories stored yet.")
    else:
        for memory in memories:
            render_memory_card(memory)

    st.divider()

    # --------------------------------------------------------
    # CLEAR MEMORY
    # --------------------------------------------------------

    st.warning(
        "⚠️ Clearing memory permanently deletes all stored memories."
    )

    if st.button(
        "🗑️ Clear All Memories",
        type="secondary",
    ):
        memory_store.clear()
        st.success("All memories have been deleted.")
        st.rerun()


# ============================================================
# ARCHITECTURE TAB
# ============================================================

with architecture_tab:
    st.subheader("🏗️ System Architecture")

    st.markdown(
        """
        ### User Input

        ↓

        ### Input Classifier

        **OpenAI ChatGPT**

        ↓

        ┌──────────────────────┬──────────────────────┐

        │                      │

        ▼                      ▼

        **STATEMENT**          **QUERY**

        │                      │

        ▼                      ▼

        **Fact Extraction**    **Embedding**

        │                      │

        │                      ▼

        │                 **Semantic Search**

        │                      │

        ▼                      ▼

        **Embedding**      **Relevant Memories**

        │                      │

        ▼                      │

        **Similarity Search**  │

        │                      │

        ▼                      ▼

        **ChatGPT Decision**  **ChatGPT**

        │                      │

        ┌───────┬───────┐      ▼

        │       │       │    **Answer**

        ▼       ▼       ▼

        **ADD** **UPDATE** **NOOP**

        │       │       │

        └───────┼───────┘

                ▼

        ### MongoDB Atlas

        Persistent Long-Term Memory
        """
    )

    st.divider()

    st.markdown("### 🔧 Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **🤖 AI**

            - OpenAI ChatGPT
            - OpenAI Embeddings
            """
        )

    with col2:
        st.markdown(
            """
            **🧠 Memory**

            - Semantic Retrieval
            - ADD / UPDATE / NOOP
            - Cosine Similarity
            """
        )

    with col3:
        st.markdown(
            """
            **🗄️ Infrastructure**

            - MongoDB Atlas
            - Streamlit
            - Python
            """
        )

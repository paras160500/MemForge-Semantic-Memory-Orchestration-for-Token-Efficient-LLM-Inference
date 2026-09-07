import streamlit as st


def setup_page():
    st.set_page_config(
        page_title="Memory Efficient LLM",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header():
    st.markdown(
        """
        <div style="
            padding: 1.5rem 0 1rem 0;
        ">
            <h1 style="
                font-size: 2.6rem;
                margin-bottom: 0.3rem;
            ">
                🧠 Memory Efficient LLM
            </h1>
            <p style="
                font-size: 1.15rem;
                color: #666;
            ">
                A long-term memory system powered by
                OpenAI and MongoDB.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(
    memory_count: int,
    embedding_dimensions: int,
    model_name: str,
    embedding_model: str,
):
    with st.sidebar:
        st.markdown("## ⚙️ System")
        st.divider()

        st.markdown("### 🤖 LLM")
        st.info(model_name)

        st.markdown("### 🔢 Embeddings")
        st.info(
            f"{embedding_model}\n\n"
            f"Dimensions: {embedding_dimensions}"
        )

        st.markdown("### 🗄️ Memory")
        st.metric("Stored Memories", memory_count)

        st.divider()

        st.markdown(
            """
            ### 🔄 Memory Flow

            `User Input`

            ↓

            `Classify`

            ↓

            `Extract Facts`

            ↓

            `Generate Embedding`

            ↓

            `Find Similar Memories`

            ↓

            `ADD / UPDATE / NOOP`

            ↓

            `MongoDB`
            """
        )


def render_memory_card(memory, score=None):
    if score is not None:
        score_text = f"Similarity: **{score:.4f}**"
    else:
        score_text = ""

    st.markdown(
        f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 0.8rem;
            background: #fafafa;
        ">
            <div style="
                font-size: 0.8rem;
                color: #777;
                margin-bottom: 0.4rem;
            ">
                Memory ID
            </div>

            <div style="
                font-size: 0.75rem;
                color: #555;
                margin-bottom: 0.7rem;
            ">
                {memory.id}
            </div>

            <div style="
                font-size: 1.05rem;
                font-weight: 500;
                margin-bottom: 0.6rem;
            ">
                {memory.text}
            </div>

            <div style="
                font-size: 0.85rem;
                color: #666;
            ">
                {score_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result(result):
    operation = result.get("operation", "NOOP")

    if operation == "ADD":
        st.success("🟢 Memory Added")
        st.write(f"**Memory ID:** `{result.get('memory_id')}`")
        st.write(result.get("fact", ""))

    elif operation == "UPDATE":
        st.warning("🟡 Memory Updated")
        st.write(f"**Memory ID:** `{result.get('memory_id')}`")
        st.write(result.get("fact", ""))

    else:
        st.info("🔵 No Memory Change")
        st.write(result.get("fact", ""))

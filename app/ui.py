from html import escape

import streamlit as st


# -----------------------------------------------------------------------------
# Design system
# -----------------------------------------------------------------------------

APP_CSS = """
<style>
    :root {
        --mf-ink: #202238;
        --mf-muted: #73768b;
        --mf-soft: #f3f1ec;
        --mf-paper: #fffdf8;
        --mf-line: #deded8;
        --mf-indigo: #4b46a8;
        --mf-indigo-dark: #302b7b;
        --mf-coral: #f26b5b;
        --mf-mint: #d8eee3;
        --mf-yellow: #f4e5ad;
    }

    .stApp {
        background: #f4f3ee;
        color: var(--mf-ink);
    }

    [data-testid="stHeader"] {
        background: rgba(244, 243, 238, 0.9);
    }

    [data-testid="stToolbar"] {
        right: 1rem;
    }

    [data-testid="stSidebar"] {
        background: #ebeae4;
        border-right: 1px solid #d8d7d0;
    }

    [data-testid="stSidebarContent"] {
        padding: 1.6rem 1.25rem 2rem 1.25rem;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1320px;
        padding-top: 3.6rem;
        padding-bottom: 4rem;
    }

    .block-container {
        max-width: 1320px;
    }

    [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid var(--mf-line);
    }

    [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1rem;
        color: var(--mf-muted);
        font-weight: 700;
    }

    [aria-selected="true"] {
        color: var(--mf-indigo) !important;
    }

    [data-baseweb="tab-highlight"] {
        background: var(--mf-indigo);
    }

    div[data-testid="stChatInput"] {
        border: 1px solid #d2d1ca;
        border-radius: 16px;
        background: var(--mf-paper);
        box-shadow: 0 8px 24px rgba(37, 38, 62, 0.08);
    }

    div[data-testid="stChatMessage"] {
        border: 1px solid #e0dfd8;
        border-radius: 16px;
        background: rgba(255, 253, 248, 0.72);
        margin: 0.65rem 0;
    }

    .mf-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.15rem 0 1.7rem 0;
    }

    .mf-mark {
        display: grid;
        place-items: center;
        width: 2.55rem;
        height: 2.55rem;
        border-radius: 12px;
        background: var(--mf-indigo);
        color: white;
        font-size: 1.25rem;
        box-shadow: 0 7px 16px rgba(75, 70, 168, 0.22);
    }

    .mf-brand-name {
        color: var(--mf-ink);
        font-size: 1.05rem;
        font-weight: 850;
        letter-spacing: -0.02em;
    }

    .mf-brand-subtitle {
        margin-top: 0.12rem;
        color: var(--mf-muted);
        font-size: 0.68rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .mf-eyebrow {
        color: var(--mf-indigo);
        font-size: 0.72rem;
        font-weight: 850;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }

    .mf-hero {
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(260px, 0.75fr);
        align-items: end;
        gap: 2.5rem;
        padding: 0.6rem 0 2.1rem 0;
    }

    .mf-hero h1 {
        max-width: 780px;
        margin: 0;
        color: var(--mf-ink);
        font-size: clamp(2.65rem, 5.2vw, 5.4rem);
        line-height: 0.96;
        letter-spacing: -0.075em;
        font-weight: 900;
    }

    .mf-hero h1 span {
        color: var(--mf-coral);
    }

    .mf-hero-copy {
        max-width: 640px;
        margin: 1.3rem 0 0;
        color: var(--mf-muted);
        font-size: 1.03rem;
        line-height: 1.65;
    }

    .mf-hero-note {
        padding: 1.2rem 1.3rem;
        border: 1px solid var(--mf-line);
        border-radius: 18px;
        background: var(--mf-paper);
        box-shadow: 0 10px 22px rgba(37, 38, 62, 0.05);
    }

    .mf-hero-note-label {
        color: var(--mf-muted);
        font-size: 0.68rem;
        font-weight: 850;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .mf-hero-note strong {
        display: block;
        margin-top: 0.65rem;
        color: var(--mf-indigo-dark);
        font-size: 1.05rem;
        line-height: 1.35;
    }

    .mf-section-label {
        color: var(--mf-muted);
        font-size: 0.7rem;
        font-weight: 850;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin: 1.5rem 0 0.75rem;
    }

    .mf-flow {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.8rem;
        margin: 1.2rem 0 1.8rem;
    }

    .mf-flow-card {
        min-height: 128px;
        padding: 1rem;
        border: 1px solid var(--mf-line);
        border-radius: 17px;
        background: var(--mf-paper);
    }

    .mf-flow-number {
        display: inline-grid;
        place-items: center;
        width: 1.7rem;
        height: 1.7rem;
        border-radius: 50%;
        background: var(--mf-mint);
        color: #27644a;
        font-size: 0.75rem;
        font-weight: 900;
    }

    .mf-flow-card h3 {
        margin: 0.9rem 0 0.3rem;
        color: var(--mf-ink);
        font-size: 0.95rem;
    }

    .mf-flow-card p {
        margin: 0;
        color: var(--mf-muted);
        font-size: 0.78rem;
        line-height: 1.45;
    }

    .mf-memory-card {
        padding: 1.1rem 1.2rem;
        border: 1px solid #deddd5;
        border-radius: 18px;
        margin: 0.7rem 0;
        background: var(--mf-paper);
        box-shadow: 0 7px 18px rgba(37, 38, 62, 0.05);
    }

    .mf-memory-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.85rem;
    }

    .mf-memory-label {
        color: var(--mf-indigo);
        font-size: 0.7rem;
        font-weight: 850;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .mf-score {
        border-radius: 999px;
        padding: 0.3rem 0.65rem;
        background: #eeeafd;
        color: var(--mf-indigo-dark);
        font-size: 0.72rem;
        font-weight: 850;
    }

    .mf-memory-text {
        margin-bottom: 1rem;
        color: var(--mf-ink);
        font-size: 1.04rem;
        line-height: 1.55;
    }

    .mf-memory-id {
        color: var(--mf-muted);
        font-family: monospace;
        font-size: 0.7rem;
        overflow-wrap: anywhere;
    }

    .mf-sidebar-heading {
        margin: 1.7rem 0 0.7rem;
        color: #84857f;
        font-size: 0.67rem;
        font-weight: 850;
        letter-spacing: 0.16em;
        text-transform: uppercase;
    }

    .mf-sidebar-copy {
        color: #73756f;
        font-size: 0.78rem;
        line-height: 1.55;
    }

    .mf-service {
        padding: 0.45rem 0;
        color: #555a59;
        font-size: 0.78rem;
    }

    .mf-service b {
        color: var(--mf-indigo-dark);
    }

    .mf-side-rule {
        height: 1px;
        margin: 1.35rem 0;
        background: #d1d0c8;
    }

    .mf-stat-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 1.5rem 0;
    }

    .mf-stat {
        padding: 1.1rem 1.2rem;
        border: 1px solid var(--mf-line);
        border-radius: 17px;
        background: var(--mf-paper);
    }

    .mf-stat-label {
        color: var(--mf-muted);
        font-size: 0.74rem;
    }

    .mf-stat-value {
        margin-top: 0.5rem;
        color: var(--mf-indigo-dark);
        font-size: 1.55rem;
        font-weight: 850;
        letter-spacing: -0.04em;
    }

    @media (max-width: 850px) {
        .mf-hero { grid-template-columns: 1fr; gap: 1.2rem; }
        .mf-flow { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .mf-stat-grid { grid-template-columns: 1fr; }
    }
</style>
"""


def _html(fragment: str):
    """Render HTML consistently across supported Streamlit versions."""
    if hasattr(st, "html"):
        st.html(fragment)
    else:
        st.markdown(fragment, unsafe_allow_html=True)


def setup_page():
    st.set_page_config(
        page_title="MemForge · Semantic Memory",
        page_icon="✦",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(APP_CSS, unsafe_allow_html=True)


def render_header():
    _html(
        """
        <div class="mf-hero">
            <div>
                <div class="mf-eyebrow">Semantic memory · quietly working in the background</div>
                <h1>Make every conversation<br><span>remembered.</span></h1>
                <p class="mf-hero-copy">
                    MemForge keeps the details that matter, finds them when they are useful,
                    and stays out of the way when they are not.
                </p>
            </div>
            <div class="mf-hero-note">
                <div class="mf-hero-note-label">Memory principle</div>
                <strong>Store meaning, not transcripts.</strong>
                <p class="mf-sidebar-copy">Facts are extracted, embedded, compared, and either added, updated, or left alone.</p>
            </div>
        </div>
        """
    )


def render_sidebar(
    memory_count: int,
    embedding_dimensions: int,
    model_name: str,
    embedding_model: str,
):
    with st.sidebar:
        _html(
            """
            <div class="mf-brand">
                <div class="mf-mark">✦</div>
                <div>
                    <div class="mf-brand-name">MemForge</div>
                    <div class="mf-brand-subtitle">Semantic memory studio</div>
                </div>
            </div>
            <div class="mf-sidebar-heading">Workspace</div>
            <div class="mf-sidebar-copy">
                Talk naturally, save useful facts, and inspect what your assistant remembers.
            </div>
            <div class="mf-side-rule"></div>
            <div class="mf-sidebar-heading">Connected services</div>
            """
        )

        _html(
            f"""
            <div class="mf-service"><b>OpenAI</b> · {escape(str(model_name))}</div>
            <div class="mf-service"><b>Embeddings</b> · {escape(str(embedding_model))}</div>
            <div class="mf-service"><b>MongoDB</b> · persistent memory</div>
            <div class="mf-side-rule"></div>
            <div class="mf-sidebar-heading">Memory index</div>
            <div class="mf-service"><b>{int(memory_count)}</b> stored memories</div>
            <div class="mf-service"><b>{int(embedding_dimensions)}</b> embedding dimensions</div>
            """
        )

        st.caption("Tip: statements become memories; questions bring them back.")


def render_flow():
    _html(
        """
        <div class="mf-section-label">How the memory loop works</div>
        <div class="mf-flow">
            <div class="mf-flow-card">
                <span class="mf-flow-number">01</span>
                <h3>Understand</h3>
                <p>Classify what you said as a statement or a question.</p>
            </div>
            <div class="mf-flow-card">
                <span class="mf-flow-number">02</span>
                <h3>Distill</h3>
                <p>Extract only durable facts worth keeping for later.</p>
            </div>
            <div class="mf-flow-card">
                <span class="mf-flow-number">03</span>
                <h3>Compare</h3>
                <p>Use semantic similarity to find nearby memories.</p>
            </div>
            <div class="mf-flow-card">
                <span class="mf-flow-number">04</span>
                <h3>Decide</h3>
                <p>Add, update, or skip without duplicating your memory.</p>
            </div>
        </div>
        """
    )


def render_architecture():
    _html(
        """
        <style>
            .arch-shell {
                padding: 1.4rem;
                border: 1px solid #deddd5;
                border-radius: 20px;
                background: #fffdf8;
                box-shadow: 0 9px 22px rgba(37, 38, 62, 0.05);
            }
            .arch-kicker {
                color: #4b46a8;
                font-size: .7rem;
                font-weight: 850;
                letter-spacing: .16em;
                text-transform: uppercase;
                margin-bottom: .5rem;
            }
            .arch-title {
                color: #202238;
                font-size: 1.8rem;
                font-weight: 900;
                letter-spacing: -.045em;
                margin-bottom: 1.35rem;
            }
            .arch-node {
                padding: .85rem 1rem;
                border: 1px solid #d9d8d0;
                border-radius: 13px;
                background: #f8f7f2;
                color: #202238;
                text-align: center;
                font-size: .9rem;
                font-weight: 800;
            }
            .arch-node.primary {
                border-color: #b8b4ed;
                background: #eeeafd;
                color: #302b7b;
            }
            .arch-node.accent {
                border-color: #f2b2a9;
                background: #fff0ed;
                color: #a74438;
            }
            .arch-arrow {
                color: #9a9aa7;
                text-align: center;
                font-size: 1.3rem;
                line-height: 1.15;
                padding: .22rem 0;
            }
            .arch-branch {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 1rem;
                position: relative;
            }
            .arch-branch:before {
                content: "";
                position: absolute;
                top: -.55rem;
                left: 25%;
                right: 25%;
                border-top: 1px dashed #bebdc6;
            }
            .arch-lane {
                padding: 1rem;
                border: 1px solid #e1e0da;
                border-radius: 16px;
                background: #fbfaf6;
            }
            .arch-lane-label {
                color: #73768b;
                font-size: .67rem;
                font-weight: 850;
                letter-spacing: .14em;
                text-transform: uppercase;
                margin-bottom: .75rem;
            }
            .arch-stack {
                display: grid;
                gap: .55rem;
            }
            .arch-foot {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: .8rem;
                margin-top: 1rem;
            }
            .arch-foot-card {
                padding: 1rem;
                border-radius: 15px;
                background: #f4f3ee;
                border: 1px solid #e0dfd8;
            }
            .arch-foot-card h4 {
                margin: 0 0 .65rem;
                color: #302b7b;
                font-size: .86rem;
            }
            .arch-foot-card p {
                margin: .28rem 0;
                color: #73768b;
                font-size: .78rem;
            }
            @media (max-width: 700px) {
                .arch-branch, .arch-foot { grid-template-columns: 1fr; }
            }
        </style>
        <div class="arch-shell">
            <div class="arch-kicker">Under the hood</div>
            <div class="arch-title">From conversation to durable memory</div>

            <div class="arch-node primary">User input</div>
            <div class="arch-arrow">↓</div>
            <div class="arch-node">Input classifier · OpenAI ChatGPT</div>
            <div class="arch-arrow">↓</div>

            <div class="arch-branch">
                <div class="arch-lane">
                    <div class="arch-lane-label">Statement lane</div>
                    <div class="arch-stack">
                        <div class="arch-node accent">Fact extraction</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">Embedding</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">Similarity search</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node primary">ChatGPT decision</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">ADD · UPDATE · NOOP</div>
                    </div>
                </div>
                <div class="arch-lane">
                    <div class="arch-lane-label">Question lane</div>
                    <div class="arch-stack">
                        <div class="arch-node accent">Embedding</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">Semantic search</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">Relevant memories</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node primary">ChatGPT answer</div>
                        <div class="arch-arrow">↓</div>
                        <div class="arch-node">Natural response</div>
                    </div>
                </div>
            </div>

            <div class="arch-arrow">↓</div>
            <div class="arch-node primary">MongoDB Atlas · persistent long-term memory</div>

            <div class="arch-foot">
                <div class="arch-foot-card">
                    <h4>✦ AI layer</h4>
                    <p>OpenAI ChatGPT</p>
                    <p>OpenAI Embeddings</p>
                </div>
                <div class="arch-foot-card">
                    <h4>◈ Memory layer</h4>
                    <p>Semantic retrieval</p>
                    <p>ADD / UPDATE / NOOP</p>
                    <p>Cosine similarity</p>
                </div>
                <div class="arch-foot-card">
                    <h4>▣ Infrastructure</h4>
                    <p>MongoDB Atlas</p>
                    <p>Streamlit</p>
                    <p>Python</p>
                </div>
            </div>
        </div>
        """
    )


def render_memory_card(memory, score=None):
    score_html = ""
    if score is not None:
        score_html = f'<span class="mf-score">Match {float(score):.1%}</span>'

    _html(
        f"""
        <div class="mf-memory-card">
            <div class="mf-memory-top">
                <div class="mf-memory-label">✦ Relevant memory</div>
                {score_html}
            </div>
            <div class="mf-memory-text">{escape(str(memory.text))}</div>
            <div class="mf-memory-id">{escape(str(memory.id))}</div>
        </div>
        """
    )


def render_stat_cards(memory_count: int, embedding_dimensions: int):
    _html(
        f"""
        <div class="mf-stat-grid">
            <div class="mf-stat">
                <div class="mf-stat-label">Stored memories</div>
                <div class="mf-stat-value">{int(memory_count)}</div>
            </div>
            <div class="mf-stat">
                <div class="mf-stat-label">Embedding width</div>
                <div class="mf-stat-value">{int(embedding_dimensions)}</div>
            </div>
            <div class="mf-stat">
                <div class="mf-stat-label">Memory mode</div>
                <div class="mf-stat-value">Semantic</div>
            </div>
        </div>
        """
    )


def render_result(result):
    operation = result.get("operation", "NOOP")

    if operation == "ADD":
        st.success("Memory added to your semantic index.")
        st.write(f"**Memory ID:** `{result.get('memory_id')}`")
        st.write(result.get("fact", ""))
    elif operation == "UPDATE":
        st.warning("An existing memory was refined.")
        st.write(f"**Memory ID:** `{result.get('memory_id')}`")
        st.write(result.get("fact", ""))
    else:
        st.info("No memory change was needed.")
        st.write(result.get("fact", ""))

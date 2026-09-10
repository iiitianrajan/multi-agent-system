import streamlit as st
import time
from agents import build_search_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind — Research Agent",
    page_icon="§",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=Inter:wght@400;500;600&display=swap');

/* ── Tokens ──
   Paper/ink palette with a single restrained navy accent. Green is reserved
   for completed states and the critique panel only. */
:root {
    --paper: #ffffff;
    --paper-subtle: #f5f6f8;
    --ink: #171a21;
    --ink-muted: #5b6270;
    --ink-faint: #8a909c;
    --border: #dfe2e8;
    --accent: #1f3d63;
    --accent-hover: #16304f;
    --accent-soft: #eef2f8;
    --success: #1d7a4c;
    --success-soft: #e9f5ee;
    --font-serif: 'Source Serif 4', Georgia, serif;
    --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

html, body, [class*="css"] {
    font-family: var(--font-sans);
    color: var(--ink);
}

.stApp {
    background: var(--paper);
}

/* Every element Streamlit renders defaults to ink on paper. */
.stApp, .stApp p, .stApp span, .stApp li, .stApp label,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] * {
    color: var(--ink);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1180px; }

/* ── Masthead ──
   A left-aligned journal nameplate rather than a centered hero — this is a
   working tool, not a landing page. */
.masthead {
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.masthead-mark {
    font-family: var(--font-serif);
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--ink) !important;
    margin: 0 0 0.4rem;
}
.masthead-tagline {
    font-size: 0.95rem;
    color: var(--ink-muted) !important;
    max-width: 560px;
    line-height: 1.6;
}

/* ── Section heading ── */
.section-heading {
    font-family: var(--font-serif);
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--ink) !important;
    margin: 0 0 1rem;
}

/* ── Input field ── */
.field-label-text {
    font-size: 0.82rem;
    color: var(--ink-muted) !important;
    margin-bottom: 0.5rem;
}
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p {
    font-family: var(--font-sans) !important;
    font-size: 0.82rem !important;
    color: var(--ink-muted) !important;
    font-weight: 500 !important;
}
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"] {
    background: var(--paper) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
}
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    caret-color: var(--ink) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 0.9rem !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: var(--ink-faint) !important;
    opacity: 1 !important;
}
[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within,
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
[data-testid="stTextInput"] input:-webkit-autofill {
    -webkit-text-fill-color: var(--ink) !important;
    -webkit-box-shadow: 0 0 0px 1000px var(--paper) inset !important;
    caret-color: var(--ink) !important;
}

/* ── Buttons ──
   Flat, solid, one color. No gradients or glow — this reads as a working
   tool, not a marketing surface. */
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"],
.stButton > button {
    background: var(--accent) !important;
    color: #ffffff !important;
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.65rem 1.4rem !important;
    cursor: pointer !important;
    transition: background 0.15s !important;
    box-shadow: none !important;
    width: 100%;
}
[data-testid="stBaseButton-secondary"] p,
[data-testid="stBaseButton-primary"] p,
.stButton > button p {
    color: #ffffff !important;
}
.stButton > button:hover {
    background: var(--accent-hover) !important;
}

[data-testid="stDownloadButton"] button {
    background: var(--paper) !important;
    border: 1px solid var(--accent) !important;
}
[data-testid="stDownloadButton"] button p {
    color: var(--accent) !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: var(--accent-soft) !important;
}

/* ── Topic panel ── */
.input-panel {
    background: var(--paper-subtle);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.2rem;
}
.topic-examples {
    font-size: 0.85rem;
    color: var(--ink-faint) !important;
    margin-top: 1rem;
}
.topic-examples b {
    color: var(--ink-muted) !important;
    font-weight: 500;
}

/* ── Pipeline stepper ──
   A vertical sequence with a connecting line. Numbers are appropriate here
   because this genuinely is a fixed order of steps. */
.stepper {
    position: relative;
    padding-left: 0.2rem;
}
.step-item {
    position: relative;
    display: flex;
    gap: 1rem;
    padding-bottom: 1.6rem;
}
.step-item:last-child { padding-bottom: 0; }
.step-item:not(:last-child)::before {
    content: '';
    position: absolute;
    left: 13px;
    top: 30px;
    bottom: -2px;
    width: 1px;
    background: var(--border);
}
.step-marker {
    flex-shrink: 0;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-sans);
    font-size: 0.78rem;
    font-weight: 600;
    border: 1.5px solid var(--border);
    color: var(--ink-faint);
    background: var(--paper);
    z-index: 1;
}
.step-item.active .step-marker {
    border-color: var(--accent);
    color: var(--accent);
    background: var(--accent-soft);
}
.step-item.done .step-marker {
    border-color: var(--success);
    background: var(--success);
    color: #ffffff;
}
.step-body { padding-top: 0.15rem; }
.step-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--ink) !important;
    margin-bottom: 0.15rem;
}
.step-desc {
    font-size: 0.83rem;
    color: var(--ink-muted) !important;
    line-height: 1.5;
}
.step-state {
    font-size: 0.76rem;
    font-weight: 500;
    margin-top: 0.25rem;
}
.step-item.waiting .step-state { color: var(--ink-faint) !important; }
.step-item.active .step-state  { color: var(--accent) !important; }
.step-item.done .step-state    { color: var(--success) !important; }

/* ── Result panels ── */
.result-panel {
    background: var(--paper-subtle);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    margin-top: 0.5rem;
}
.result-panel-title {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--ink-muted) !important;
    margin-bottom: 0.8rem;
}
.result-content {
    font-size: 0.9rem;
    line-height: 1.75;
    color: var(--ink) !important;
    white-space: pre-wrap;
}

/* ── Report & critique panels ──
   Distinguished by a top accent rule, not by wrapping every block in an
   identical bordered card. */
.report-panel, .report-panel *,
.critique-panel, .critique-panel * {
    color: var(--ink) !important;
}
.report-panel {
    background: var(--paper);
    border-top: 2px solid var(--accent);
    padding: 1.8rem 0 0.5rem;
    margin-top: 0.5rem;
}
.critique-panel {
    background: var(--paper);
    border-top: 2px solid var(--success);
    padding: 1.8rem 0 0.5rem;
    margin-top: 2rem;
}
.panel-label {
    font-family: var(--font-serif);
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 1rem;
}
.panel-label.navy { color: var(--accent) !important; }
.panel-label.green { color: var(--success) !important; }

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: var(--ink-muted) !important; font-size: 0.88rem; }

/* ── Expander ── */
details summary p {
    font-size: 0.85rem !important;
    color: var(--ink-muted) !important;
    font-weight: 500;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 2.2rem 0;
}

/* ── Footer ── */
.notice {
    font-size: 0.8rem;
    color: var(--ink-faint) !important;
    margin-top: 3rem;
}

[data-testid="stAlert"] p { color: var(--ink) !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render a stepper item ─────────────────────────────────────────────
def step_item(num: str, title: str, desc: str, state: str):
    state_label = {"waiting": "Waiting", "active": "In progress", "done": "Complete"}[state]
    marker = "✓" if state == "done" else num
    st.markdown(f"""
    <div class="step-item {state}">
        <div class="step-marker">{marker}</div>
        <div class="step-body">
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
            <div class="step-state">{state_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Masthead ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-mark">ResearchMind</div>
    <div class="masthead-tagline">
        Four agents work in sequence — searching, reading, writing, and reviewing —
        to turn a topic into a sourced research report.
    </div>
</div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.6, 4])

with col_input:
    st.markdown('<div class="section-heading">Start a report</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-panel">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    st.markdown("""
    <script>
    (function() {
        const inputs = window.parent.document.querySelectorAll('[data-testid="stTextInput"] input');
        inputs.forEach(el => {
            el.setAttribute('autocomplete', 'off');
            el.setAttribute('spellcheck', 'false');
        });
    })();
    </script>
    """, unsafe_allow_html=True)
    run_btn = st.button("Start research", use_container_width=True)
    st.markdown("""
    <div class="topic-examples"><b>Or try:</b> LLM agents in 2025, CRISPR gene editing, fusion energy progress</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "active" if k == step else "waiting"
        return "waiting"

    st.markdown('<div class="stepper">', unsafe_allow_html=True)
    step_item("1", "Search agent", "Gathers recent, relevant sources from the web.", s("search"))
    step_item("2", "Reader agent", "Opens the strongest source and extracts its detail.", s("reader"))
    step_item("3", "Writer chain", "Drafts the full report from the gathered research.", s("writer"))
    step_item("4", "Critic chain", "Reviews the draft and scores it for quality.", s("critic"))
    st.markdown('</div>', unsafe_allow_html=True)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    # ── Step 1: Search ──
    with st.spinner("Search agent is gathering sources…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 2: Reader ──
    with st.spinner("Reader agent is extracting detail from the top source…"):
        reader_agent = build_search_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # ── Step 3: Writer ──
    with st.spinner("Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    # ── Step 4: Critic ──
    with st.spinner("Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("Search results (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search agent output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("Scraped content (raw)", expanded=False):
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader agent output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    if "writer" in r:
        st.markdown('<div class="report-panel"><div class="panel-label navy">Research report</div>',
                    unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown('<div class="critique-panel"><div class="panel-label green">Critic feedback</div>',
                    unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">ResearchMind is a four-agent pipeline built with LangChain and Streamlit.</div>
""", unsafe_allow_html=True)
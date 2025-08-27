"""
RetailNext Streamlit UX Skin — drop‑in theming & layout helpers

Goal: Make your existing Streamlit app *look like* the RetailNext website
without changing your app's core logic.

How to use (minimal changes to your current app):
------------------------------------------------
1) Save this file as `ui_skin.py` next to your Streamlit app (e.g. `app.py`).
2) Add at the very top of your app:

   from ui_skin import mount_ui, render_navbar, render_footer
   mount_ui(title="RetailNext — AI Outfit Assistant", favicon="🛍️")
   render_navbar()

3) (Optional) Wrap big sections of your existing UI with the helpers below
   (hero/sections/cards/steps). If you don't, the global theme + navbar +
   footer will still give you 80–90% of the look & feel.

4) (Optional) Create `.streamlit/config.toml` with the THEME_TOML content
   included at the bottom of this file for consistent light/dark tokens.

Everything runs in vanilla Streamlit. No external libs required.
"""
from __future__ import annotations
import streamlit as st
from typing import Iterable, Optional, Dict
from streamlit.components.v1 import html as html_component

# --- Page + global CSS -------------------------------------------------------

_BASE_CSS = r"""
<style>
:root{
  --bg:#0b0b10; --text:#e6e7ee; --muted:#b6b7c3; --card:#151522; --card2:#1b1b2b;
  --accent:#7c5cff; --accent2:#5eead4; --border:rgba(255,255,255,.08); --rad:18px;
}
html,body,[data-testid="stAppViewContainer"]{background: radial-gradient(1200px 600px at 70% -10%, rgba(124,92,255,.20), transparent 60%),
                                             radial-gradient(900px 500px at 10% -10%, rgba(94,234,212,.12), transparent 60%),
                                             linear-gradient(180deg, #0a0a0f, #0b0b10 30% 70%, #0a0a0f)!important;}

/* Tighten default container width */
.block-container{max-width:1200px; padding-top:0rem;}

/* Typography */
body, .stMarkdown, .stText, .stTextInput, .stButton button{color:var(--text)!important;}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3{letter-spacing:normal}

/* Cards */
.rnx-card{background:linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
  border:1px solid var(--border); border-radius:var(--rad); padding:18px; box-shadow:0 10px 30px rgba(0,0,0,.35)}
.rnx-card h3{margin:6px 0 6px; font-size:18px}
.rnx-muted{color:var(--muted)!important}

/* Buttons */
.stButton button{background:linear-gradient(135deg, var(--accent), #8b5cf6)!important;
  color:#fff!important; border-radius:999px!important; border:1px solid rgba(255,255,255,.12)!important;}
.stButton button:hover{filter:brightness(1.03)}

/* Inputs */
.stTextInput>div>div>input, textarea, .stTextArea>div>div>textarea{
  background:#0f0f16!important; color:var(--text)!important; border:1px solid var(--border)!important;
  border-radius:12px!important;
}

/* Navbar */
.rnx-nav{position:sticky; top:0; z-index:999; backdrop-filter: blur(10px);
  background: rgba(15, 15, 24, 0.6); border-bottom: 1px solid rgba(124,92,255,.12);}
.rnx-nav-inner{max-width:1200px; margin:0 auto; display:flex; align-items:center; justify-content:space-between; height:64px; padding:0 16px}
.rnx-brand{display:inline-flex; align-items:center; gap:10px; font-weight:700; letter-spacing:.4px}
.rnx-mark{width:28px; height:28px; border-radius:8px; background:linear-gradient(135deg, var(--accent), var(--accent2)); box-shadow:0 4px 14px rgba(124,92,255,.35)}
.rnx-links{display:none; gap:22px; color:var(--muted); font-weight:500}
.rnx-cta{display:inline-flex; align-items:center; gap:10px; background:linear-gradient(135deg, var(--accent), #8b5cf6);
  color:#fff; padding:10px 16px; border-radius:999px; border:1px solid rgba(255,255,255,.12); box-shadow:0 10px 30px rgba(0,0,0,.35); text-decoration:none}
@media(min-width:900px){.rnx-links{display:flex}}

/* Footer */
.rnx-footer{color:var(--muted); border-top:1px solid var(--border); padding:32px 0 56px}
.rnx-footer-inner{max-width:1200px; margin:0 auto; display:grid; grid-template-columns:1fr auto; gap:10px; align-items:center; padding:0 16px}

/* Hero */
.rnx-hero{padding:40px 0 20px}
.rnx-hero-grid{display:grid; grid-template-columns:1.2fr; gap:30px; align-items:center}
@media(min-width:1024px){.rnx-hero-grid{grid-template-columns:1.2fr .8fr}}
.rnx-eyebrow{display:inline-flex; align-items:center; gap:8px; color:var(--accent2); font-weight:600; font-size:13px; letter-spacing:.6px; text-transform:uppercase}
.rnx-dot{width:6px; height:6px; border-radius:999px; background:var(--accent2); display:inline-block}
.rnx-lead{color:var(--muted); font-size:18px; line-height:1.6}
.rnx-media{background:linear-gradient(180deg, rgba(255,255,255,.02), rgba(255,255,255,.01)); border:1px solid var(--border); border-radius:18px; padding:10px;}
.rnx-media iframe{width:100%; aspect-ratio:16/9; border:0; border-radius:10px; background:#0f0f16}

/* Simple reveal */
.rnx-reveal{opacity:0; transform:translateY(8px); transition:all .5s ease}
.rnx-reveal.rnx-show{opacity:1; transform:none}
</style>
"""

_REVEAL_JS = r"""
<script>
  const io = new IntersectionObserver((entries)=>{
    entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('rnx-show'); } });
  }, {threshold:.1});
  document.querySelectorAll('.rnx-reveal').forEach(el=>io.observe(el));
</script>
"""

def mount_ui(title: str = "RetailNext", favicon: str | None = None):
    """Set page config and inject global CSS/JS once."""
    st.set_page_config(page_title=title, page_icon=favicon or "🛍️", layout="wide", initial_sidebar_state="collapsed")
    # Only inject once per session
    if "_rnx_css" not in st.session_state:
        st.session_state["_rnx_css"] = True
        st.markdown(_BASE_CSS, unsafe_allow_html=True)
        st.markdown(_REVEAL_JS, unsafe_allow_html=True)

# --- Navbar & Footer ---------------------------------------------------------

def render_navbar(links: Optional[Iterable[tuple[str,str]]] = None, cta: tuple[str,str] | None = ("Get in touch", "#contact")):
    links = links or []
    links_html = "".join([f'<a href="{href}">{label}</a>' for label, href in links]) if links else ""
    cta_html = f'<a class="rnx-cta" href="{cta[1]}">{cta[0]}</a>' if cta else ""
    html_component(f"""
    <nav class='rnx-nav'>
      <div class='rnx-nav-inner'>
        <div class='rnx-brand'><span class='rnx-mark' aria-hidden='true'></span></div>
        <div class='rnx-links'>{links_html}</div>
        {cta_html}
      </div>
    </nav>
    """, height=70)


def render_footer():
    html_component(f"""
      <footer class='rnx-footer' id='contact'>
        <div class='rnx-footer-inner'>
          <div>© {__import__('datetime').datetime.now().year} RetailNext • Built for demo purposes</div>
          <div><a class='rnx-cta' href='#top' style='padding:8px 14px'>Back to top ↑</a></div>
        </div>
      </footer>
    """, height=90)

# --- Building blocks (optional to use) --------------------------------------

def hero(title: str, subtitle: str = "", eyebrow: str = "AI Outfit Assistant", video_url: str | None = None):
    if video_url:
        left, right = st.columns([1.2, .9])
        with left:
            st.markdown(
                f"""
                <div class='rnx-hero'>
                  <div class='rnx-hero-grid'>
                    <div>
                      <div class='rnx-eyebrow'><span style='color: #5eead4;'>{eyebrow}</span></div>
                      <h1 style='font-size:clamp(34px,5vw,56px); line-height:1.05; margin:12px 0 10px;'>
                        Turn product images into <span style="color: #7c5cff; font-weight: bold;">personalised outfit ideas</span>
                      </h1>
                      <p class='rnx-lead'>{subtitle}</p>
                    </div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with right:
            st.markdown("<div class='rnx-media rnx-reveal'>", unsafe_allow_html=True)
            st.video(video_url)
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Full width layout when no video
        st.markdown(
            f"""
            <div class='rnx-hero'>
              <div class='rnx-hero-grid' style='grid-template-columns: 1fr;'>
                <div>
                  <div class='rnx-eyebrow'><span style='color: #5eead4;'>{eyebrow}</span></div>
                  <h1 style='font-size:clamp(34px,5vw,56px); line-height:1.05; margin:12px 0 10px; text-align: left;'>
                    Turn product images into <span style="background: linear-gradient(135deg, #7c5cff, #5eead4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;">personalised outfit ideas</span>
                  </h1>
                  <p class='rnx-lead' style='text-align: left;'>{subtitle}</p>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def section(title: str, lead: str = "", anchor: str | None = None):
    if anchor:
        st.markdown(f"<span id='{anchor}'></span>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='font-size:clamp(24px,3vw,34px); margin:0 0 16px;'>{title}</h2>", unsafe_allow_html=True)
    if lead:
        st.markdown(f"<p class='rnx-muted' style='max-width:740px'>{lead}</p>", unsafe_allow_html=True)


def cards(items: Iterable[tuple[str,str]], columns: int = 4):
    cols = st.columns(columns)
    for i, (header, text) in enumerate(items):
        with cols[i % columns]:
            st.markdown("<div class='rnx-card rnx-reveal'>", unsafe_allow_html=True)
            st.markdown(f"<h3>{header}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p class='rnx-muted'>{text}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)


def steps(step_text: Iterable[str]):
    for idx, txt in enumerate(step_text, start=1):
        st.markdown(
            f"""
            <div class='rnx-card rnx-reveal' style='display:grid; grid-template-columns:40px 1fr; gap:14px; align-items:start;'>
              <div style='width:40px; height:40px; border-radius:12px; background:linear-gradient(135deg, var(--accent), #8b5cf6); display:inline-flex; align-items:center; justify-content:center; font-weight:700'>{idx}</div>
              <div>{txt}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def architecture_svg(svg_html: str):
    st.markdown(f"<div class='rnx-card rnx-reveal' style='overflow:auto'>{svg_html}</div>", unsafe_allow_html=True)


# --- Result Box Component ---------------------------------------------------

def _inject_result_box_css():
    # Only inject once per session
    if st.session_state.get("_rnx_result_css_injected"):
        return
    st.session_state["_rnx_result_css_injected"] = True

    st.markdown(
        """
        <style>
          :root {
            --rnx-text: #e6e7ee;
            --rnx-muted: #b6b7c3;
            --rnx-card: #151522;
            --rnx-border: rgba(255,255,255,.10);
            --rnx-shadow: 0 10px 30px rgba(0,0,0,.35);
            --rnx-accent-2: #5eead4;
            --rnx-radius: 18px;
          }
          .rnx-result-box {
            background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
            border: 1px solid var(--rnx-border);
            border-radius: var(--rnx-radius);
            padding: 20px;
            margin-top: 16px;
            box-shadow: var(--rnx-shadow);
          }
          .rnx-result-box h3 {
            margin: 0 0 8px 0;
            font-size: 20px;
            color: var(--rnx-accent-2);
          }
          .rnx-kv { 
            margin: 6px 0; 
            color: var(--rnx-muted);
          }
          .rnx-kv strong { 
            color: var(--rnx-text);
          }
          .rnx-chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:8px; }
          .rnx-chip {
            padding: 6px 10px;
            border: 1px solid var(--rnx-border);
            border-radius: 999px;
            background: #0f0f16;
            color: var(--rnx-text);
            font-size: 13px;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

def result_box(
    title: str = "Item Analysis Results",
    fields: Dict[str, str] | None = None,
    matches: Iterable[str] | None = None,
):
    """
    Renders a themed results box.
    - title: heading at the top of the box
    - fields: dict of label -> value (e.g., {"Category": "Shirt", "Colour": "Black"})
    - matches: iterable of suggested match strings to render as chips
    """
    _inject_result_box_css()

    # Build the key/values HTML
    kv_html = ""
    if fields:
        for k, v in fields.items():
            kv_html += f"<p class='rnx-kv'><strong>{k}:</strong> {v}</p>"

    chips_html = ""
    if matches:
        chips = "".join([f"<span class='rnx-chip'>{m}</span>" for m in matches])
        chips_html = f"<div class='rnx-chips'>{chips}</div>"

    st.markdown(
        f"""
        <div class="rnx-result-box">
          <h3>{title}</h3>
          {kv_html}
          {'<p class="rnx-kv"><strong>Suggested Matches:</strong></p>' if matches else ''}
          {chips_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Example THEME file for .streamlit/config.toml ---------------------------
THEME_TOML = """
[theme]
base = "dark"
primaryColor = "#7c5cff"
backgroundColor = "#0b0b10"
secondaryBackgroundColor = "#151522"
textColor = "#e6e7ee"
font = "Inter, sans-serif"
"""

# --- Quick self-preview (optional) ------------------------------------------
if __name__ == "__main__":
    mount_ui()
    render_navbar()
    hero(
        title="Turn product images into personalised outfit ideas.",
        subtitle="A demo that analyses clothing images, embeds style descriptors, searches a vector DB, and suggests matching items — fast.",
        video_url="",
    )
    section("What is RetailNext?", "A compact reference implementation combining multimodal analysis, text embeddings and a custom cosine‑similarity search to power semantic product discovery and outfit matching.", anchor="about")
    cards([
        ("Image analysis", "Extract colour, style, and category details from product photos."),
        ("Semantic search", "Turn descriptors into embeddings and retrieve similar catalogue items."),
        ("Matching logic", "Apply guardrails to ensure items pair well in an outfit."),
        ("Fast demo UI", "Streamlit front end for showcasing results in seconds."),
    ], columns=4)
    section("How it works", anchor="how")
    steps([
        "<strong>Upload / select item</strong><br/><span class='rnx-muted'>User provides a reference garment image.</span>",
        "<strong>Analyse & describe</strong><br/><span class='rnx-muted'>Model generates a compact JSON description of style attributes.</span>",
        "<strong>Embed & retrieve</strong><br/><span class='rnx-muted'>Generate vectors and run k‑NN search over the catalogue.</span>",
        "<strong>Match & present</strong><br/><span class='rnx-muted'>Return 2–3 complementary items with rationale.</span>",
    ])
    section("Business value", anchor="value")
    cards([
        ("Faster discovery", "Improve product findability when text search fails; boost add‑to‑cart via visual matching."),
        ("Higher AOV", "Complementary item suggestions drive baskets (e.g., shirt → jeans + shoes)."),
        ("Low lift", "Drop‑in demo that runs locally or in your cloud; swap components later."),
    ], columns=3)
    render_footer()

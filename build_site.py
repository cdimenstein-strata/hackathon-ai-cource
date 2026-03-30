#!/usr/bin/env python3
"""
Build script: Converts course markdown files into a single-page
interactive HTML course website.
"""

import os
import re
import sys
from typing import Dict, Tuple
import mistune

# ─── Raw HTML block preservation ─────────────────────────────────────────────

def _extract_html_blocks(text: str) -> Tuple[str, Dict[str, str]]:
    """Replace raw HTML <div> blocks (including nested) with placeholders.

    Args:
        text: Markdown text containing HTML blocks

    Returns:
        Tuple of (processed text with placeholders, dictionary mapping placeholders to original HTML)
    """
    blocks = {}
    idx = 0
    result = []
    pos = 0
    n = len(text)
    while pos < n:
        start = text.find('<div', pos)
        if start == -1:
            result.append(text[pos:])
            break
        result.append(text[pos:start])
        depth = 0
        i = start
        while i < n:
            if text[i:i+4] == '<div':
                depth += 1
                end_tag = text.find('>', i + 4)
                i = (end_tag + 1) if end_tag != -1 else n
            elif text[i:i+6] == '</div>':
                depth -= 1
                i += 6
                if depth == 0:
                    break
            else:
                i += 1
        block = text[start:i]
        key = f'RAWHTML_BLOCK_{idx}_END'
        blocks[key] = block
        result.append(f'\n{key}\n')
        idx += 1
        pos = i
    return ''.join(result), blocks

def _restore_html_blocks(html: str, blocks: Dict[str, str]) -> str:
    """Put the original HTML blocks back, removing any <p> wrapper mistune added.

    Args:
        html: HTML with placeholders
        blocks: Dictionary mapping placeholders to original HTML

    Returns:
        HTML with original blocks restored
    """
    for key, block in blocks.items():
        html = html.replace(f'<p>{key}</p>', block)
        html = html.replace(key, block)
    return html
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

COURSE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ordered list of course files
COURSE_FILES = [
    ("Course Overview", "Course Summary/COURSE_OVERVIEW.md"),
    ("Module 1: Foundations of Agentic AI", "Textbook Chapters/MODULE_01_Foundations.md"),
    ("Module 2: Goals & Success Metrics", "Textbook Chapters/MODULE_02_Goals_and_Metrics.md"),
    ("Module 3: Agent System Architecture", "Textbook Chapters/MODULE_03_Architecture.md"),
    ("Module 4: Amazon Bedrock Deep Dive", "Textbook Chapters/MODULE_04_Bedrock_Deep_Dive.md"),
    ("Module 5: Knowledge Bases in Bedrock", "Textbook Chapters/MODULE_05_Knowledge_Bases.md"),
    ("Module 6: MCP Servers", "Textbook Chapters/MODULE_06_MCP_Servers.md"),
    ("Module 7: Productionizing Agent Systems", "Textbook Chapters/MODULE_07_Productionizing.md"),
    ("Answer Keys — All Modules", "Quizzes and Assessments/ANSWER_KEYS.md"),
    ("Checkpoint Quizzes & Answer Keys", "Quizzes and Assessments/CHECKPOINT_QUIZZES.md"),
    ("Practice Exercises", "Quizzes and Assessments/PRACTICE_EXERCISES.md"),
    ("PowerPoint Slide Deck Outline", "POWERPOINT_OUTLINE.md"),
    ("Capstone Project & Course Index", "Quizzes and Assessments/CAPSTONE_AND_INDEX.md"),
]

# ─── Syntax highlighting renderer ────────────────────────────────────────────

class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, **attrs):
        lang = (attrs.get("info") or "").strip().split()[0] if attrs.get("info") else ""
        try:
            lexer = get_lexer_by_name(lang, stripall=True) if lang else TextLexer()
        except Exception:
            lexer = TextLexer()
        formatter = HtmlFormatter(nowrap=True)
        highlighted = highlight(code, lexer, formatter)
        return f'<pre class="code-block"><code>{highlighted}</code></pre>\n'

    def heading(self, text, level, **_attrs):
        # Generate an anchor id from heading text
        raw = re.sub(r'<[^>]+>', '', text)
        anchor = re.sub(r'[^\w\s-]', '', raw).strip().lower()
        anchor = re.sub(r'[\s]+', '-', anchor)
        return f'<h{level} id="{anchor}">{text}</h{level}>\n'

def make_md():
    return mistune.create_markdown(
        renderer=HighlightRenderer(),
        plugins=['table', 'strikethrough', 'footnotes', 'task_lists']
    )

# ─── Pygments CSS ─────────────────────────────────────────────────────────────

PYGMENTS_CSS = HtmlFormatter(style='monokai').get_style_defs('.code-block')

# ─── HTML Template ───────────────────────────────────────────────────────────

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Designing and Deploying Agentic AI Systems with Amazon Bedrock</title>
<style>

/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
  --bg:        #0f1117;
  --surface:   #1a1d27;
  --surface2:  #222538;
  --border:    #2e3147;
  --accent:    #FF9900;
  --accent2:   #5b8dee;
  --text:      #e8eaf0;
  --text-muted:#8b90a8;
  --green:     #4caf82;
  --red:       #e05c6a;
  --sidebar-w: 300px;
  --header-h:  60px;
}}

html {{ scroll-behavior: smooth; font-size: 16px; }}

body {{
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  line-height: 1.7;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}}

/* ── Top Header ── */
.top-header {{
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 2px solid var(--accent);
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 16px;
  z-index: 1000;
}}

.top-header .logo {{
  display: flex; align-items: center; gap: 10px;
  font-weight: 700; font-size: 1rem; color: var(--text);
  text-decoration: none;
}}

.top-header .logo .badge {{
  background: var(--accent);
  color: #000;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}}

.top-header .course-title {{
  font-size: 0.85rem;
  color: var(--text-muted);
  flex: 1;
}}

.menu-toggle {{
  display: none;
  background: none; border: none;
  color: var(--text); cursor: pointer;
  font-size: 1.4rem; padding: 4px 8px;
}}

/* ── Layout ── */
.layout {{
  display: flex;
  margin-top: var(--header-h);
  min-height: calc(100vh - var(--header-h));
}}

/* ── Sidebar ── */
.sidebar {{
  width: var(--sidebar-w);
  background: var(--surface);
  border-right: 1px solid var(--border);
  position: fixed;
  top: var(--header-h);
  bottom: 0;
  left: 0;
  overflow-y: auto;
  z-index: 900;
  transition: transform 0.25s ease;
}}

.sidebar::-webkit-scrollbar {{ width: 4px; }}
.sidebar::-webkit-scrollbar-track {{ background: transparent; }}
.sidebar::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

.sidebar-search {{
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
}}

.sidebar-search input {{
  width: 100%;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 12px;
  color: var(--text);
  font-size: 0.82rem;
  outline: none;
}}

.sidebar-search input:focus {{
  border-color: var(--accent2);
}}

.sidebar nav {{ padding: 8px 0 40px; }}

.nav-section {{ margin-bottom: 4px; }}

.nav-section-title {{
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
  padding: 10px 20px 4px;
}}

.nav-link {{
  display: block;
  padding: 7px 20px;
  color: var(--text-muted);
  text-decoration: none;
  font-size: 0.82rem;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  cursor: pointer;
}}

.nav-link:hover {{
  color: var(--text);
  background: var(--surface2);
  border-left-color: var(--accent2);
}}

.nav-link.active {{
  color: var(--accent);
  background: rgba(255, 153, 0, 0.08);
  border-left-color: var(--accent);
  font-weight: 600;
}}

/* ── Main Content ── */
.main {{
  margin-left: var(--sidebar-w);
  flex: 1;
  min-width: 0;
}}

/* ── Section Panels ── */
.section-panel {{
  display: none;
  padding: 48px 56px 80px;
  max-width: 960px;
}}

.section-panel.active {{ display: block; }}

/* ── Typography ── */
.section-panel h1 {{
  font-size: 2rem;
  font-weight: 800;
  color: var(--accent);
  margin-bottom: 8px;
  line-height: 1.2;
  border-bottom: 2px solid var(--border);
  padding-bottom: 16px;
  margin-bottom: 32px;
}}

.section-panel h2 {{
  font-size: 1.45rem;
  font-weight: 700;
  color: var(--text);
  margin: 48px 0 16px;
  padding-left: 14px;
  border-left: 4px solid var(--accent);
}}

.section-panel h3 {{
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--accent2);
  margin: 32px 0 12px;
}}

.section-panel h4 {{
  font-size: 1rem;
  font-weight: 700;
  color: var(--green);
  margin: 24px 0 8px;
}}

.section-panel p {{
  margin-bottom: 16px;
  color: var(--text);
  line-height: 1.8;
}}

.section-panel ul, .section-panel ol {{
  margin: 12px 0 20px 24px;
}}

.section-panel li {{
  margin-bottom: 6px;
  line-height: 1.7;
}}

.section-panel strong {{ color: var(--accent); font-weight: 700; }}
.section-panel em {{ color: var(--text-muted); }}

/* ── Blockquotes ── */
.section-panel blockquote {{
  border-left: 4px solid var(--accent2);
  background: var(--surface2);
  padding: 16px 20px;
  margin: 24px 0;
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: var(--text-muted);
}}

/* ── Code ── */
.section-panel code:not(.code-block code) {{
  background: var(--surface2);
  color: #f4a261;
  padding: 2px 7px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, monospace;
  font-size: 0.85em;
  border: 1px solid var(--border);
}}

.section-panel pre.code-block {{
  background: #1e1e2e;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px 24px;
  overflow-x: auto;
  margin: 20px 0;
  font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', Menlo, monospace;
  font-size: 0.83rem;
  line-height: 1.65;
}}

/* Pygments styles */
{pygments_css}

/* ── Tables ── */
.section-panel table {{
  width: 100%;
  border-collapse: collapse;
  margin: 24px 0;
  font-size: 0.88rem;
  border-radius: 8px;
  overflow: hidden;
}}

.section-panel thead th {{
  background: var(--surface2);
  color: var(--accent);
  font-weight: 700;
  padding: 12px 16px;
  text-align: left;
  border-bottom: 2px solid var(--accent);
  font-size: 0.82rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}}

.section-panel tbody tr {{
  border-bottom: 1px solid var(--border);
  transition: background 0.1s;
}}

.section-panel tbody tr:hover {{
  background: var(--surface2);
}}

.section-panel td {{
  padding: 10px 16px;
  color: var(--text);
  vertical-align: top;
}}

/* ── HR ── */
.section-panel hr {{
  border: none;
  border-top: 1px solid var(--border);
  margin: 40px 0;
}}

/* ── Screenshot Placeholder Callouts ── */
.section-panel p:has(strong:first-child) {{
  /* handled via JS post-processing */
}}

/* ── Progress Bar ── */
.progress-bar {{
  position: fixed;
  top: var(--header-h);
  left: 0;
  height: 3px;
  background: var(--accent);
  transition: width 0.3s ease;
  z-index: 999;
}}

/* ── Scroll to Top ── */
.scroll-top {{
  position: fixed;
  bottom: 30px; right: 30px;
  background: var(--accent);
  color: #000;
  border: none; border-radius: 50%;
  width: 44px; height: 44px;
  font-size: 1.2rem;
  cursor: pointer;
  display: none;
  align-items: center; justify-content: center;
  z-index: 999;
  box-shadow: 0 4px 16px rgba(255,153,0,0.3);
}}

.scroll-top.visible {{ display: flex; }}

/* ── Welcome Banner ── */
.welcome-banner {{
  background: linear-gradient(135deg, var(--surface2), var(--surface));
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 32px 36px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}}

.welcome-banner::before {{
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
}}

.welcome-banner h2 {{
  border: none !important;
  padding-left: 0 !important;
  margin-top: 0 !important;
  font-size: 1.5rem !important;
  color: var(--text) !important;
}}

.welcome-banner .meta {{
  display: flex; gap: 20px; flex-wrap: wrap;
  margin-top: 16px;
}}

.welcome-banner .meta-item {{
  display: flex; align-items: center; gap: 6px;
  font-size: 0.82rem; color: var(--text-muted);
}}

.welcome-banner .meta-item span.dot {{
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--accent);
  display: inline-block;
}}

/* ── Module Cards on Overview ── */
.module-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin: 24px 0;
}}

.module-card {{
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
  border-top: 3px solid var(--accent2);
}}

.module-card:hover {{
  border-color: var(--accent);
  border-top-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}}

.module-card .card-num {{
  font-size: 0.7rem; font-weight: 700;
  color: var(--accent2); letter-spacing: 0.1em;
  text-transform: uppercase; margin-bottom: 6px;
}}

.module-card .card-title {{
  font-weight: 700; font-size: 0.95rem;
  color: var(--text); margin-bottom: 8px;
}}

.module-card .card-desc {{
  font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;
}}

/* ── Screenshot Placeholder Styling ── */
.screenshot-placeholder {{
  background: var(--surface2);
  border: 1px dashed var(--accent2);
  border-radius: 10px;
  padding: 20px 24px;
  margin: 24px 0;
  font-size: 0.85rem;
}}

.screenshot-placeholder .sp-header {{
  color: var(--accent2);
  font-weight: 700;
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 10px;
}}

.screenshot-placeholder p {{
  color: var(--text-muted); margin: 4px 0;
}}

/* ── Responsive ── */
@media (max-width: 900px) {{
  .sidebar {{
    transform: translateX(-100%);
  }}
  .sidebar.open {{
    transform: translateX(0);
  }}
  .main {{
    margin-left: 0;
  }}
  .section-panel {{
    padding: 32px 24px 60px;
  }}
  .menu-toggle {{
    display: block;
  }}
  .overlay {{
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 850;
  }}
  .overlay.active {{ display: block; }}
}}

@media (max-width: 600px) {{
  .section-panel h1 {{ font-size: 1.5rem; }}
  .section-panel h2 {{ font-size: 1.2rem; }}
  .top-header .course-title {{ display: none; }}
}}

/* ── In-page Answer Key TOC ── */
.answer-toc {{
  position: fixed;
  top: calc(var(--header-h) + 16px);
  right: 16px;
  width: 220px;
  max-height: calc(100vh - var(--header-h) - 32px);
  background: var(--surface);
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent2);
  border-radius: 10px;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 800;
  opacity: 0;
  pointer-events: none;
  transform: translateX(240px);
  transition: opacity 0.25s ease, transform 0.25s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}}

.answer-toc.visible {{
  opacity: 1;
  pointer-events: auto;
  transform: translateX(0);
}}

.answer-toc-header {{
  padding: 10px 14px 8px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent2);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}}

.answer-toc-body {{
  overflow-y: auto;
  flex: 1;
  padding: 6px 0 10px;
}}

.answer-toc-body::-webkit-scrollbar {{ width: 3px; }}
.answer-toc-body::-webkit-scrollbar-track {{ background: transparent; }}
.answer-toc-body::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}

.answer-toc-body a {{
  display: block;
  padding: 4px 14px;
  font-size: 0.75rem;
  color: var(--text-muted);
  text-decoration: none;
  line-height: 1.35;
  border-left: 2px solid transparent;
  transition: all 0.12s;
}}

.answer-toc-body a:hover {{
  color: var(--text);
  background: var(--surface2);
  border-left-color: var(--accent2);
}}

.answer-toc-body a.toc-active {{
  color: var(--accent);
  border-left-color: var(--accent);
  background: rgba(255,153,0,0.06);
}}

.answer-toc-body a.toc-h2 {{
  padding-left: 14px;
  font-weight: 600;
  font-size: 0.78rem;
  color: var(--text);
  margin-top: 4px;
}}

.answer-toc-body a.toc-h3 {{
  padding-left: 24px;
  font-size: 0.72rem;
}}

.answer-toc-toggle {{
  position: fixed;
  top: calc(var(--header-h) + 16px);
  right: 16px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 7px 10px;
  font-size: 0.75rem;
  color: var(--accent2);
  cursor: pointer;
  z-index: 801;
  display: none;
  align-items: center;
  gap: 5px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  white-space: nowrap;
}}

.answer-toc-toggle.visible {{ display: flex; }}
.answer-toc-toggle:hover {{ background: var(--surface2); }}

/* Adjust main content when TOC is visible */
@media (min-width: 1240px) {{
  .answer-toc.visible ~ .main-with-toc,
  body.toc-open .section-panel {{
    padding-right: 248px;
  }}
}}

/* ── Print ── */
@media print {{
  .sidebar, .top-header, .scroll-top, .progress-bar, .answer-toc, .answer-toc-toggle {{ display: none; }}
  .main {{ margin-left: 0; }}
  .section-panel {{ display: block !important; padding: 0; }}
  body {{ background: #fff; color: #000; }}
}}

</style>
</head>
<body>

<!-- Top Header -->
<header class="top-header">
  <button class="menu-toggle" onclick="toggleSidebar()" aria-label="Menu">☰</button>
  <a class="logo" href="#" onclick="showSection(0); return false;">
    <span class="badge">AWS</span>
    <span>Bedrock Agent Course</span>
  </a>
  <span class="course-title">Designing and Deploying Agentic AI Systems with Amazon Bedrock</span>
</header>

<!-- Progress Bar -->
<div class="progress-bar" id="progressBar" style="width:0%"></div>

<!-- Overlay for mobile sidebar -->
<div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

<!-- Layout -->
<div class="layout">

  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-search">
      <input type="text" id="searchInput" placeholder="🔍  Search course content…" oninput="filterNav(this.value)">
    </div>
    <nav id="sidebarNav">
      {nav_html}
    </nav>
  </aside>

  <!-- Main Content -->
  <main class="main" id="mainContent">
    {content_html}
  </main>
</div>

<!-- In-page Answer Key TOC -->
<div class="answer-toc" id="answerToc">
  <div class="answer-toc-header">📋 In This Section</div>
  <div class="answer-toc-body" id="answerTocBody"></div>
</div>
<button class="answer-toc-toggle" id="answerTocToggle" onclick="toggleAnswerToc()">📋 Navigation</button>

<!-- Scroll-to-top button -->
<button class="scroll-top" id="scrollTop" onclick="scrollToTop()" title="Back to top">↑</button>

<script>
// ── Section navigation ────────────────────────────────────────────────────────
const sections = document.querySelectorAll('.section-panel');
const navLinks  = document.querySelectorAll('.nav-link');

function showSection(idx) {{
  sections.forEach((s, i) => s.classList.toggle('active', i === idx));
  navLinks.forEach((l, i) => l.classList.toggle('active', i === idx));
  document.getElementById('mainContent').scrollTop = 0;
  window.scrollTo(0, 0);
  updateProgress();
  // close sidebar on mobile
  if (window.innerWidth <= 900) closeSidebar();
}}

navLinks.forEach((link, i) => {{
  link.addEventListener('click', () => showSection(i));
}});

// Show first section by default
showSection(0);

// ── Sidebar toggle ────────────────────────────────────────────────────────────
function toggleSidebar() {{
  const sb = document.getElementById('sidebar');
  const ov = document.getElementById('overlay');
  sb.classList.toggle('open');
  ov.classList.toggle('active');
}}

function closeSidebar() {{
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('active');
}}

// ── Progress bar ──────────────────────────────────────────────────────────────
function updateProgress() {{
  const active = [...sections].findIndex(s => s.classList.contains('active'));
  const pct = ((active + 1) / sections.length) * 100;
  document.getElementById('progressBar').style.width = pct + '%';
}}

// ── Scroll to top button ──────────────────────────────────────────────────────
window.addEventListener('scroll', () => {{
  const btn = document.getElementById('scrollTop');
  btn.classList.toggle('visible', window.scrollY > 400);
}});

function scrollToTop() {{
  window.scrollTo({{ top: 0, behavior: 'smooth' }});
}}

// ── Nav search / filter ───────────────────────────────────────────────────────
function filterNav(query) {{
  const q = query.toLowerCase();
  navLinks.forEach(link => {{
    const matches = link.textContent.toLowerCase().includes(q);
    link.style.display = matches ? '' : 'none';
  }});
  // Show section headers if any child is visible
  document.querySelectorAll('.nav-section').forEach(section => {{
    const hasVisible = [...section.querySelectorAll('.nav-link')]
                         .some(l => l.style.display !== 'none');
    section.style.display = hasVisible ? '' : 'none';
  }});
}}

// ── Post-process Screenshot Placeholders ─────────────────────────────────────
document.querySelectorAll('.section-panel').forEach(panel => {{
  panel.innerHTML = panel.innerHTML.replace(
    /(<p>)\s*<strong>Screenshot Placeholder:<\/strong>([\s\S]*?)(<\/p>)/g,
    (match, open, content, close) => {{
      return `<div class="screenshot-placeholder">
        <div class="sp-header">📸  Screenshot Placeholder</div>
        <p>${{content.trim()}}</p>
      </div>`;
    }}
  );
}});

// ── Keyboard nav ─────────────────────────────────────────────────────────────
document.addEventListener('keydown', e => {{
  const cur = [...sections].findIndex(s => s.classList.contains('active'));
  if (e.altKey && e.key === 'ArrowRight' && cur < sections.length - 1) showSection(cur + 1);
  if (e.altKey && e.key === 'ArrowLeft'  && cur > 0)                    showSection(cur - 1);
}});

// ── In-page Answer Key TOC ───────────────────────────────────────────────────
let tocOpen = false;
let tocBuilt = false;

function buildAnswerToc(section) {{
  const body = document.getElementById('answerTocBody');
  body.innerHTML = '';
  const headings = section.querySelectorAll('h1, h2, h3');
  let count = 0;
  headings.forEach(h => {{
    if (count > 120) return; // limit TOC length
    const a = document.createElement('a');
    // Build clean label
    let label = h.textContent.replace(/^#+\s*/, '').trim();
    if (label.length > 52) label = label.slice(0, 50) + '…';
    a.textContent = label;
    a.href = '#' + h.id;
    a.className = 'toc-' + h.tagName.toLowerCase();
    a.addEventListener('click', e => {{
      e.preventDefault();
      h.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      // Mark active
      body.querySelectorAll('a').forEach(x => x.classList.remove('toc-active'));
      a.classList.add('toc-active');
    }});
    body.appendChild(a);
    count++;
  }});
  tocBuilt = true;
}}

function showAnswerToc(section) {{
  if (!tocBuilt) buildAnswerToc(section);
  document.getElementById('answerToc').classList.add('visible');
  document.getElementById('answerTocToggle').classList.add('visible');
  tocOpen = true;
  document.body.classList.add('toc-open');
}}

function hideAnswerToc() {{
  document.getElementById('answerToc').classList.remove('visible');
  tocOpen = false;
  document.body.classList.remove('toc-open');
  // Keep toggle visible so user can re-open
}}

function toggleAnswerToc() {{
  const toc = document.getElementById('answerToc');
  if (toc.classList.contains('visible')) {{
    hideAnswerToc();
  }} else {{
    const activeSection = document.querySelector('.section-panel.active');
    if (activeSection && activeSection.dataset.toc === 'true') {{
      buildAnswerToc(activeSection);
      document.getElementById('answerToc').classList.add('visible');
      tocOpen = true;
      document.body.classList.add('toc-open');
    }}
  }}
}}

// Intercept showSection to manage TOC visibility
const _origShowSection = showSection;
showSection = function(idx) {{
  _origShowSection(idx);
  tocBuilt = false;
  const section = sections[idx];
  if (section && section.dataset.toc === 'true') {{
    buildAnswerToc(section);
    showAnswerToc(section);
  }} else {{
    hideAnswerToc();
    document.getElementById('answerToc').classList.remove('visible');
    document.getElementById('answerTocToggle').classList.remove('visible');
    document.body.classList.remove('toc-open');
  }}
}};

// Scroll spy: highlight active TOC item as user scrolls
window.addEventListener('scroll', () => {{
  const toc = document.getElementById('answerToc');
  if (!toc.classList.contains('visible')) return;
  const links = document.querySelectorAll('#answerTocBody a');
  if (!links.length) return;
  let current = links[0];
  links.forEach(link => {{
    const target = document.getElementById(link.getAttribute('href').slice(1));
    if (target && target.getBoundingClientRect().top < 120) current = link;
  }});
  links.forEach(l => l.classList.remove('toc-active'));
  current.classList.add('toc-active');
  // Auto-scroll TOC to keep active item visible
  const body = document.getElementById('answerTocBody');
  const linkRect = current.getBoundingClientRect();
  const bodyRect = body.getBoundingClientRect();
  if (linkRect.top < bodyRect.top + 40 || linkRect.bottom > bodyRect.bottom - 40) {{
    current.scrollIntoView({{ block: 'nearest' }});
  }}
}});
</script>
</body>
</html>
"""

# ─── Build ────────────────────────────────────────────────────────────────────

def load_md(filename: str) -> str:
    """Load a markdown file from the course directory.

    Args:
        filename: Name of the markdown file to load

    Returns:
        Content of the markdown file

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    path = os.path.join(COURSE_DIR, filename)
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {path}", file=sys.stderr)
        raise
    except IOError as e:
        print(f"❌ Error reading file {path}: {e}", file=sys.stderr)
        raise

def build():
    md = make_md()
    nav_parts = []
    content_parts = []

    for idx, (title, filename) in enumerate(COURSE_FILES):
        raw = load_md(filename)
        raw, html_blocks = _extract_html_blocks(raw)
        html_body = md(raw)
        html_body = _restore_html_blocks(html_body, html_blocks)

        # ── Navigation entry
        nav_parts.append(
            f'<div class="nav-section">'
            f'<a class="nav-link" data-idx="{idx}">{title}</a>'
            f'</div>'
        )

        # ── Active class on first
        active_cls = " active" if idx == 0 else ""

        # ── Mark answer keys section for in-page TOC
        toc_attr = ' data-toc="true"' if "ANSWER_KEYS.md" in filename else ""

        content_parts.append(
            f'<div class="section-panel{active_cls}"{toc_attr} id="section-{idx}">'
            f'{html_body}'
            f'</div>'
        )

    nav_html = "\n".join(nav_parts)
    content_html = "\n".join(content_parts)

    html = HTML_TEMPLATE.format(
        pygments_css=PYGMENTS_CSS,
        nav_html=nav_html,
        content_html=content_html,
    )

    out_path = os.path.join(COURSE_DIR, "index.html")
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"✅  Built: {out_path}  ({size_kb:.0f} KB)")
        return out_path
    except IOError as e:
        print(f"❌ Error writing output file {out_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    try:
        build()
    except Exception as e:
        print(f"❌ Build failed: {e}", file=sys.stderr)
        sys.exit(1)

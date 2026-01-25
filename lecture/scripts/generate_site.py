import os
import re
import shutil
from pathlib import Path

# Configuration
LECTURE_DIR = Path("lecture")
OUTPUT_DIR = Path("lecture/site")
TEMPLATE_PATH = Path("lecture/scripts/template.html")
ASSETS_DIR = Path("lecture/scripts/assets")

# HTML Template (Inline for simplicity if file missing)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - MoAI Master Class</title>
    <link rel="stylesheet" href="assets/style.css">
    <!-- Highlight.js for syntax highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    <!-- Mermaid for diagrams -->
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
    </script>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            MoAI-ADK Class 🗿
        </div>
        <div class="sidebar-content">
            {navigation}
        </div>
    </div>
    <div class="main">
        <div class="content-wrapper">
            {content}
        </div>
    </div>
</body>
</html>
"""

def simple_markdown_to_html(md_text):
    """
    A simple regex-based Markdown parser to avoid external dependencies.
    For a production tool, use 'markdown' or 'mistune' library.
    """
    html = md_text

    # Headers
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold/Italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Code Blocks (fenced)
    # Note: capturing language for highlight.js class
    def code_block_repl(match):
        lang = match.group(1) or ""
        code = match.group(2)
        # Escape HTML in code
        code = code.replace("<", "&lt;").replace(">", "&gt;")
        if lang == "mermaid":
            return f'<pre class="mermaid">{code}</pre>'
        return f'<pre><code class="language-{lang}">{code}</code></pre>'
    
    html = re.sub(r'```(\w+)?\n(.*?)```', code_block_repl, html, flags=re.DOTALL)
    
    # Inline Code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Links [text](url)
    # Fix relative links to .md to .html
    def link_repl(match):
        text = match.group(1)
        url = match.group(2)
        if url.endswith(".md"):
            url = url.replace(".md", ".html")
        return f'<a href="{url}">{text}</a>'
        
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_repl, html)
    
    # Blockquotes
    html = re.sub(r'^> (.*$)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Lists (Unordered)
    # Simple implementation: convert lines starting with - to li, wrap in ul manually roughly
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if line.strip().startswith("- "):
            if not in_list:
                new_lines.append("<ul>")
                in_list = True
            content = line.strip()[2:]
            # handle checkbox inside list item
            content = content.replace("[ ]", "☐").replace("[x]", "☑")
            new_lines.append(f"<li>{content}</li>")
        else:
            if in_list:
                new_lines.append("</ul>")
                in_list = False
            new_lines.append(line)
    if in_list:
         new_lines.append("</ul>")
    
    html = '\n'.join(new_lines)
    
    # Paragraphs (simple logic)
    # Wrap lines that are not tags in <p>
    # This is very naive, but sufficient for this demo without libraries
    
    return html

def build_navigation(current_file):
    """Generates the sidebar HTML"""
    nav = []
    
    # Core Track
    nav.append('<div class="nav-group"><div class="nav-group-title">Core Track</div>')
    core_files = sorted([f for f in LECTURE_DIR.glob("*.md") if f.name != "ROADMAP.KR.md"])
    # Put ROADMAP first
    roadmap = [f for f in core_files if f.name == "ROADMAP.md"]
    others = [f for f in core_files if f.name != "ROADMAP.md"]
    
    for f in roadmap + others:
        active_class = " active" if f.name == current_file.name else ""
        link = f.name.replace(".md", ".html")
        title = f.stem.replace("_", " ")
        nav.append(f'<a href="{link}" class="nav-link{active_class}">{title}</a>')
    
    nav.append('</div>')

    # Kotlin Track
    nav.append('<div class="nav-group"><div class="nav-group-title">Kotlin Vibe</div>')
    kotlin_dir = LECTURE_DIR / "kotlin"
    if kotlin_dir.exists():
        kotlin_files = sorted(list(kotlin_dir.glob("*.md")))
        # Put ROADMAP first
        roadmap_k = [f for f in kotlin_files if f.name == "ROADMAP.md"]
        others_k = [f for f in kotlin_files if f.name != "ROADMAP.md"]
        
        for f in roadmap_k + others_k:
            active_class = " active" if f.name == current_file.name else ""
            link = f"kotlin/{f.name.replace('.md', '.html')}"
            title = f.stem.replace("_", " ")
            nav.append(f'<a href="{link}" class="nav-link{active_class}">{title}</a>')

    nav.append('</div>')
    
    return "\n".join(nav)

def generate():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    (OUTPUT_DIR / "assets").mkdir()
    
    # Copy Assets
    shutil.copy(ASSETS_DIR / "style.css", OUTPUT_DIR / "assets/style.css")
    
    # Find all MD files
    md_files = list(LECTURE_DIR.rglob("*.md"))
    
    for md_file in md_files:
        if "site" in str(md_file.parts): continue 
        if "scripts" in str(md_file.parts): continue
        
        print(f"Processing {md_file}...")
        
        with open(md_file, "r") as f:
            content = f.read()
            
        html_content = simple_markdown_to_html(content)
        
        # Calculate relative path for navigation links fix
        # If in subfolder, links need ../
        rel_path = md_file.relative_to(LECTURE_DIR)
        depth = len(rel_path.parts) - 1
        
        # Fix navigation links based on depth (Hack for the simple nav builder)
        # Ideally nav builder should be context aware, here we just patch the output
        # For simplicity in this script, we assume flat output for assets, but subfolders for content match source
        
        output_file = OUTPUT_DIR / rel_path.with_suffix(".html")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Fix asset paths
        asset_prefix = "../" * depth
        
        nav_html = build_navigation(md_file)
        
        # Adjust links in nav for depth
        if depth > 0:
             nav_html = nav_html.replace('href="', f'href="{asset_prefix}')
             # This replacement is tricky with the mix of links. 
             # Let's just regenerate nav with robust relative paths logic if we were writing a full engine.
             # For now, let's just make the generated HTML flat for simplicity? 
             # No, file structure helps. Let's fix the asset path in template.
        
        # Simple fix for assets in template
        final_html = HTML_TEMPLATE.format(
            title=md_file.stem,
            content=html_content,
            navigation=nav_html
        )
        
        if depth > 0:
            final_html = final_html.replace('href="assets/', f'href="{asset_prefix}assets/')
            # Fix nav links that shouldn't have prefix if they are absolute relative...
            # The simple nav builder produced: "Chapter_01.html" and "kotlin/Chapter_01.html"
            # If we are in kotlin/, "Chapter_01.html" becomes "../Chapter_01.html"
            # and "kotlin/Chapter_01.html" becomes "Chapter_01.html"
            
            # Let's do a quick regex fix for links
            def fix_nav_link(match):
                url = match.group(1)
                if url.startswith("http"): return f'href="{url}"'
                return f'href="{asset_prefix}{url}"'
            
            final_html = re.sub(r'href="([^"#]+)"', fix_nav_link, final_html)

        with open(output_file, "w") as f:
            f.write(final_html)

if __name__ == "__main__":
    generate()

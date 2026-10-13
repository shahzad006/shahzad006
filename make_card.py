"""Builds light.svg and dark.svg: a terminal-style profile card."""
from html import escape
from pathlib import Path

HERE = Path(__file__).parent

# Left panel: code snippet, as (indent, [(token_class, text), ...])
CODE = [
    (0, [("kw", "class "), ("cls", "AIEngineer"), ("p", ":")]),
    (1, [("kw", "def "), ("fn", "__init__"), ("p", "(self):")]),
    (2, [("p", "self.name  = "), ("str", '"Muhammad Shahzad"')]),
    (2, [("p", "self.role  = "), ("str", '"AI Engineer"')]),
    (2, [("p", "self.stack = ["), ("str", '"Python"'), ("p", ", "), ("str", '"FastAPI"'), ("p", ",")]),
    (5, [("str", '"LangChain"'), ("p", ", "), ("str", '"LangGraph"'), ("p", "]")]),
    (2, [("p", "self.focus = ["), ("str", '"Agentic workflows"'), ("p", ",")]),
    (5, [("str", '"RAG pipelines"'), ("p", ",")]),
    (5, [("str", '"Multi-agent systems"'), ("p", "]")]),
    (0, []),
    (1, [("kw", "def "), ("fn", "build"), ("p", "(self):")]),
    (2, [("kw", "return "), ("str", '"intelligent systems"')]),
    (0, []),
    (0, [("p", "me = "), ("cls", "AIEngineer"), ("p", "()")]),
    (0, [("p", "me."), ("fn", "build"), ("p", "()")]),
    (0, [("com", "# -> 'intelligent systems'")]),
]


INFO = [
    ("head", "muhammad.shahzad"),
    ("kv", "Name", "Muhammad Shahzad"),
    ("kv", "Role", "Full-Stack Developer | AI Engineer"),
    ("kv", "Focus", "Agentic Workflows · RAG · Automation"),
    ("kv", "Currently", "Building • Learning and Shipping Projects"),
    ("gap",),
    ("sec", "Tech Stack"),
    ("kv", "Languages", "Python, JavaScript, TypeScript"),
    ("kv", "AI / Agents", "LangChain, LangGraph, Google ADK "),
    ("kv", "Frontend", "React, Next.js, TailwindCSS"),
    ("kv", "Backend", "FastAPI, REST APIs"),
    ("gap",),
    ("sec", "Contact"),
    ("kv", "GitHub", "github.com/shahzad006"),
    ("kv", "Gmail", "muhammadshahzad45435@gmail.com"),
    ("cursor", "Contribution activity below ↓"),
]

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", border2="#30363d",
                 text="#e6edf3", key="#79c0ff", dim="#6e7681", head="#d2a8ff",
                 accent="#58a6ff", green="#3fb950", title="#8b949e",
                 kw="#ff7b72", cls="#ffa657", fn="#d2a8ff", str="#a5d6ff", p="#e6edf3", com="#8b949e", ln="#484f58"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", border2="#d0d7de",
                  text="#1f2328", key="#0550ae", dim="#8c959f", head="#8250df",
                  accent="#0969da", green="#1a7f37", title="#57606a",
                  kw="#cf222e", cls="#953800", fn="#8250df", str="#0a3069", p="#1f2328", com="#6e7781", ln="#8c959f"),
}

W, H = 1000, 420
LX, LY, LW, LH = 18, 58, 440, 344
RX, RY, RW, RH = 472, 58, 510, 344


def build(theme: str) -> str:
    t = THEMES[theme]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">']
    css = "".join(f".{k}{{fill:{t[k]}}}" for k in ["kw", "cls", "fn", "str", "p", "com"])
    o.append(f"""<style>{css}
.k{{fill:{t['key']}}} .v{{fill:{t['text']}}} .d{{fill:{t['dim']}}} .h{{fill:{t['head']};font-weight:700}}
.ln{{opacity:0;animation:fade .4s ease forwards}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{50%{{opacity:.35}}}}
.cur{{animation:blink 1s step-end infinite}}
.dot{{animation:pulse 2s ease-in-out infinite}}
</style>""")
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>')
    o.append(f'<line x1="1" y1="40" x2="{W-1}" y2="40" stroke="{t["border"]}"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        o.append(f'<circle cx="{22 + i*18}" cy="21" r="5.5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="25" text-anchor="middle" font-size="12" fill="{t["title"]}">muhammad-shahzad — ~/profile</text>')
    o.append(f'<circle class="dot" cx="{W-110}" cy="21" r="4" fill="{t["green"]}"/>')
    o.append(f'<text x="{W-100}" y="25" font-size="11" fill="{t["green"]}">online</text>')

    for x, y, w, h, label in [(LX, LY, LW, LH, "about_me.py"), (RX, RY, RW, RH, "profile.json")]:
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{t["panel"]}" stroke="{t["border2"]}"/>')
        o.append(f'<text x="{x+12}" y="{y+20}" font-size="11" fill="{t["title"]}">{label}</text>')
        o.append(f'<line x1="{x}" y1="{y+30}" x2="{x+w}" y2="{y+30}" stroke="{t["border2"]}"/>')

    # code panel
    y, delay = LY + 52, 0.3
    for n, (ind, toks) in enumerate(CODE, 1):
        st = f'style="animation-delay:{delay:.2f}s"'
        parts = "".join(f'<tspan class="{c}">{escape(s)}</tspan>' for c, s in toks)
        o.append(f'<text class="ln" {st} font-size="12.5" xml:space="preserve">'
                 f'<tspan x="{LX+14}" y="{y}" fill="{t["ln"]}">{n:>2}</tspan>'
                 f'<tspan x="{LX+44 + ind*4*7.5:.1f}" y="{y}">{parts}</tspan></text>')
        y += 18
        delay += 0.12

    # info panel
    y, x = RY + 54, RX + 16
    for item in INFO:
        kind = item[0]
        if kind == "gap":
            y += 8
            continue
        st = f'style="animation-delay:{delay:.2f}s"'
        if kind == "head":
            o.append(f'<text class="ln" {st} x="{x}" y="{y}" font-size="14"><tspan class="h">{escape(item[1])}</tspan></text>')
        elif kind == "sec":
            o.append(f'<text class="ln" {st} x="{x}" y="{y}" font-size="12"><tspan class="k" font-weight="700">{escape(item[1])}</tspan>'
                     f'<tspan class="d"> {"─"*46}</tspan></text>')
        elif kind == "kv":
            k, v = item[1], item[2]
            o.append(f'<text class="ln" {st} x="{x}" y="{y}" font-size="12.5"><tspan class="k">{escape(k)}</tspan>'
                     f'<tspan class="d">{" " + "." * (13 - len(k)) + " "}</tspan><tspan class="v">{escape(v)}</tspan></text>')
        elif kind == "cursor":
            o.append(f'<g class="ln" {st}><text x="{x}" y="{y}" font-size="12.5"><tspan fill="{t["green"]}">❯ </tspan>'
                     f'<tspan class="d">{escape(item[1])}</tspan></text>'
                     f'<rect class="cur" x="{x + 18 + len(item[1])*7.5}" y="{y-11}" width="7" height="14" fill="{t["accent"]}"/></g>')
        y += 19
        delay += 0.1
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for th in THEMES:
        (HERE / f"{th}.svg").write_text(build(th), encoding="utf-8")
    print("ok")

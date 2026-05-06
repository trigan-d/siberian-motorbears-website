#!/usr/bin/env python3
"""Вставить /js/locale-redirect.js (только RU) и /js/lang-switch.js во все HTML под site/."""
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"
LOCALE = '  <script src="/js/locale-redirect.js"></script>\n'
LANGSW = '  <script src="/js/lang-switch.js" defer></script>\n'


def main() -> None:
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE)
        if rel.parts and rel.parts[0] == "en":
            is_en = True
        else:
            is_en = False
        if "yandex" in path.name.lower():
            continue
        text = path.read_text(encoding="utf-8")
        changed = False
        if LANGSW not in text and "</body>" in text:
            text = text.replace("</body>", LANGSW + "</body>", 1)
            changed = True
        if (
            not is_en
            and "/js/locale-redirect.js" not in text
            and "</head>" in text
        ):
            text = text.replace("</head>", LOCALE + "</head>", 1)
            changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
            print("OK", path.relative_to(REPO))


if __name__ == "__main__":
    main()

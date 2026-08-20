#!/usr/bin/env python3
"""Переименование бренда на русских страницах: «Siberian motorbears» → «Сибмотобер».

Трогает только русскую часть сайта: site/**/*.html кроме site/en/ и поле `text`
(русский текст поста) в site/blog/entries/*.json. Английские страницы, поле
`text_en`, домен siberian-motorbears.ru, почта и адрес сообщества VK не меняются.

Запуск из корня репозитория: python3 scripts/rename_brand_ru.py
"""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = REPO / "site"

BRAND_RU = "Сибмотобер"
BRAND_EN = "Siberian motorbears"
# Только само название: «siberian-motorbears.ru», «siberian.motorbears@…»
# и «vk.com/siberian_motorbears» под шаблон не попадают.
BRAND_RE = re.compile(r"Siberian(?:&nbsp;|\s)motorbears", re.I)

OLD_LOGO = "assets/img/f69558aa-3fbc-4609-a5e5-c1abd8dfcc50-1783828.png"
NEW_LOGO = "assets/img/logo-sibmotober-ru.png"
OLD_LOGO_SIZE = 'width="180" height="48"'
NEW_LOGO_SIZE = 'width="114" height="48"'

KEYWORDS_RE = re.compile(r'<meta name="keywords" content="[^"]*">')
LD_NAME = f'"name":"{BRAND_RU}","url":"https://siberian-motorbears.ru"'
LD_NAME_NEW = (
    f'"name":"{BRAND_RU}","alternateName":"{BRAND_EN}"'
    ',"url":"https://siberian-motorbears.ru"'
)

# Название было множественного числа («motorbears»), новое — единственного,
# поэтому в паре мест нужно поправить согласование сказуемого.
AGREEMENT = [
    (f"{BRAND_RU} успели засветиться", f"{BRAND_RU} успел засветиться"),
    (f"{BRAND_RU} обзавелись новым логотипом", f"{BRAND_RU} обзавёлся новым логотипом"),
]


def rename_in_text(text: str) -> str:
    for old, new in AGREEMENT:
        text = text.replace(old, new)
    return text


def convert_html(text: str) -> str:
    text = text.replace(OLD_LOGO, NEW_LOGO).replace(OLD_LOGO_SIZE, NEW_LOGO_SIZE)
    text = BRAND_RE.sub(BRAND_RU, text)
    # Латиницу возвращаем точечно: по ней ищут бренд, и она совпадает с доменом.
    text = text.replace(LD_NAME, LD_NAME_NEW)
    text = KEYWORDS_RE.sub(
        lambda m: m.group(0).replace(BRAND_RU, f"{BRAND_RU}, {BRAND_EN}"), text
    )
    return rename_in_text(text)


def ru_html_files():
    en = SITE / "en"
    for path in sorted(SITE.rglob("*.html")):
        if en in path.parents:
            continue
        yield path


def main() -> None:
    changed = 0
    for path in ru_html_files():
        old = path.read_text(encoding="utf-8")
        new = convert_html(old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(f"HTML: обновлено {changed} страниц")

    entries = 0
    for path in sorted((SITE / "blog" / "entries").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        text = data.get("text")
        if not isinstance(text, str):
            continue
        new = rename_in_text(BRAND_RE.sub(BRAND_RU, text))
        if new != text:
            data["text"] = new
            path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            entries += 1
    print(f"blog/entries: обновлено {entries} записей (только поле text)")


if __name__ == "__main__":
    main()

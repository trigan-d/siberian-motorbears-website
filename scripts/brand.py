"""Название бренда: русские страницы — «Сибмотобэр», английские — «Siberian motorbears».

Сборщики /en/ строят английские страницы заменами по русским, поэтому перед
заменами русский текст приводится к латинскому написанию бренда: тогда все
существующие пары «русская строка → английская» продолжают совпадать.
"""

BRAND_RU = "Сибмотобэр"
BRAND_EN = "Siberian motorbears"

LOGO_RU = "assets/img/logo-sibmotober-ru.png"
LOGO_EN = "assets/img/f69558aa-3fbc-4609-a5e5-c1abd8dfcc50-1783828.png"

LOGO_SIZE_RU = 'width="114" height="48"'
LOGO_SIZE_EN = 'width="180" height="48"'


def ru_to_en_brand(text: str) -> str:
    """Вернуть русской странице латинское имя бренда и английский логотип."""
    text = text.replace(f'"{BRAND_RU}","alternateName":"{BRAND_EN}"', f'"{BRAND_EN}"')
    text = text.replace(f"{BRAND_RU}, {BRAND_EN}", BRAND_EN)
    text = text.replace(BRAND_RU, BRAND_EN)
    text = text.replace(LOGO_RU, LOGO_EN)
    text = text.replace(LOGO_SIZE_RU, LOGO_SIZE_EN)
    return text

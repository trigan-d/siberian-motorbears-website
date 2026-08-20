#!/usr/bin/env python3
"""Собирает русский логотип «Сибмотобэр» из глифов оригинального логотипа.

Кириллических начертаний этого шрифта у нас нет, поэтому буквы строятся
из букв английского логотипа (зеркалирование N, склейка E+B, срезы O и R).
Так русская версия остаётся в том же шрифте, цвете и высоте, что и английская.

Запуск: python3 scripts/build_ru_logo.py
"""

from PIL import Image

SRC = "site/assets/img/f69558aa-3fbc-4609-a5e5-c1abd8dfcc50-1783828.png"
DST = "site/assets/img/logo-sibmotober-ru.png"

# Полоса, в которой в оригинале лежит надпись (высота прописной — 32 px).
TEXT_TOP, TEXT_BOT = 44, 76
TEXT_H = TEXT_BOT - TEXT_TOP

# Границы букв оригинала, найденные по колонкам без пикселей.
GLYPHS = {
    "S": (71, 88), "I": (90, 95), "B": (98, 114), "E": (117, 131),
    "R": (134, 151), "A": (161, 177), "N": (180, 196),
    "M": (213, 231), "O": (234, 250), "T": (253, 269),
}

TEXT_X = 71   # где начиналась надпись
GAP = 3       # межбуквенный просвет оригинала
RIGHT_MARGIN = 6


def glyph(src, name):
    x0, x1 = GLYPHS[name]
    return src.crop((x0, TEXT_TOP, x1, TEXT_BOT))


def clear(img, x0, y0, x1, y1):
    img.paste((0, 0, 0, 0), (x0, y0, x1, y1))


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def make_es(o):
    """С — «O» с вырезанной серединой правой стойки.

    Раскрыв взят из «S»: её верхний терминал обрывается на строке 8,
    нижний начинается со строки 23.
    """
    c = o.copy()
    clear(c, 11, 9, c.width, 23)
    return c


def make_be(b, e):
    """Б — верх «E» (стойка + верхняя перекладина) и чаша «B».

    Талию чаши нельзя брать у «B» как есть: там она стыкуется с верхней чашей,
    и без неё остаются выступ и щербина на правом крае. Верхнюю кромку талии
    зеркалим с нижней кромки чаши — скос получается тот же, что снизу.
    """
    be = Image.new("RGBA", (b.width, TEXT_H), (0, 0, 0, 0))
    be.paste(e.crop((0, 0, e.width, 14)), (0, 0))
    for src_y, dst_y in ((30, 14), (29, 15), (28, 16)):
        be.paste(b.crop((0, src_y, b.width, src_y + 1)), (0, dst_y))
    be.paste(b.crop((0, 17, b.width, TEXT_H)), (0, 17))
    return be


def make_e_oborotnoe(o, e):
    """Э — зеркальная «С» плюс язычок на середине.

    Язычок — зеркальная средняя перекладина «E»: её обрезанный торец
    становится левым концом язычка, а бывшая стойка сливается со спинкой.
    """
    ee = mirror(make_es(o))
    bar = mirror(e.crop((0, 13, 11, 18)))
    ee.alpha_composite(bar, (ee.width - bar.width, 13))
    return ee


def make_er(r):
    """Р — «R» без косой ноги: ниже чаши остаётся только стойка."""
    p = r.copy()
    clear(p, 4, 20, p.width, TEXT_H)
    return p


def main():
    src = Image.open(SRC).convert("RGBA")

    o, e, b, r, n, m, t = (glyph(src, k) for k in "OEBRNMT")

    letters = [
        make_es(o),            # С
        mirror(n),             # И
        make_be(b, e),         # Б
        m,                     # М
        o,                     # О
        t,                     # Т
        o,                     # О
        make_be(b, e),         # Б
        make_e_oborotnoe(o, e),  # Э
        make_er(r),            # Р
    ]

    text_w = sum(l.width for l in letters) + GAP * (len(letters) - 1)
    out_w = TEXT_X + text_w + RIGHT_MARGIN

    out = Image.new("RGBA", (out_w, src.height), (0, 0, 0, 0))
    # Дерево слева переносим целиком; старую надпись отсекаем по её полосе.
    icon = src.crop((0, 0, min(TEXT_X + text_w, src.width), src.height)).copy()
    clear(icon, TEXT_X - 3, TEXT_TOP, icon.width, TEXT_BOT)
    out.alpha_composite(icon)

    x = TEXT_X
    for l in letters:
        out.alpha_composite(l, (x, TEXT_TOP))
        x += l.width + GAP

    out.save(DST)
    print(f"{DST}: {out.size[0]}x{out.size[1]}")


if __name__ == "__main__":
    main()

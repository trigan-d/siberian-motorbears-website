"""Доп. замены для site/mia/index.html → site/en/mia/index.html."""

MIA_EXTRA: list[tuple[str, str]] = [
    (
        "<title>Аренда автодома Панда Мия от 15 000 ₽/сутки — прокат на 5 человек | Siberian motorbears</title>",
        "<title>Panda Mia motorhome rental from 15 000 ₽/day — five berths | Siberian motorbears</title>",
    ),
    (
        'content="Аренда интегрированного автодома Панда Мия на 5 человек. Маршруты: Алтай, Байкал, Сибирь. От 15 000 ₽/сутки. Кухня, санузел, полная комплектация. Звоните для брони: +7 (913) 460-20-50."',
        'content="Rent the integrated Panda Mia motorhome for five. Routes: Altai, Baikal, Siberia. From 15 000 ₽/day. Galley, bathroom, full outfit. Call to book: +7 (913) 460-20-50."',
    ),
    (
        'content="аренда Панда Мия, прокат автодома, Алтай, Байкал, Новосибирск, автодом на 5 человек"',
        'content="Panda Mia rental, motorhome hire, Altai, Baikal, Novosibirsk, five-berth motorhome"',
    ),
    (
        '<meta property="og:title" content="Аренда автодома Панда Мия от 15 000 ₽/сутки — прокат на 5 человек | Siberian motorbears">',
        '<meta property="og:title" content="Panda Mia motorhome rental from 15 000 ₽/day — five berths | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Аренда интегрированного автодома Панда Мия на 5 человек. Маршруты: Алтай, Байкал, Сибирь. От 15 000 ₽/сутки. Кухня, санузел, полная комплектация. Звоните для брони: +7 (913) 460-20-50.">',
        '<meta property="og:description" content="Rent the integrated Panda Mia motorhome for five. Routes: Altai, Baikal, Siberia. From 15 000 ₽/day. Galley, bathroom, full outfit. Call to book: +7 (913) 460-20-50.">',
    ),
    (
        '<meta name="twitter:title" content="Аренда автодома Панда Мия от 15 000 ₽/сутки — прокат на 5 человек | Siberian motorbears">',
        '<meta name="twitter:title" content="Panda Mia motorhome rental from 15 000 ₽/day — five berths | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Аренда интегрированного автодома Панда Мия на 5 человек. Маршруты: Алтай, Байкал, Сибирь. От 15 000 ₽/сутки. Кухня, санузел, полная комплектация. Звоните для брони: +7 (913) 460-20-50.">',
        '<meta name="twitter:description" content="Rent the integrated Panda Mia motorhome for five. Routes: Altai, Baikal, Siberia. From 15 000 ₽/day. Galley, bathroom, full outfit. Call to book: +7 (913) 460-20-50.">',
    ),
    (
        '{"@context":"https://schema.org","@type":"Product","name":"Аренда интегрированного автодома «Панда Мия»","description":"Аренда интегрированного автодома «Панда Мия», от 15 000 ₽."',
        '{"@context":"https://schema.org","@type":"Product","name":"Panda Mia integrated motorhome rental","description":"Panda Mia integrated motorhome rental from 15 000 ₽."',
    ),
    ('"unitText":"сутки"', '"unitText":"per day"'),
    (
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Панда Мия</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Panda Mia</span></div>',
    ),
    ('alt="Автодом Панда Мия — аренда, фото"', 'alt="Panda Mia motorhome — rental photo"'),
    (
        '<h1 style="font-size: 1.35rem;">Аренда интегрированного автодома «Панда Мия»</h1>',
        '<h1 style="font-size: 1.35rem;">Integrated motorhome «Panda Mia» rental</h1>',
    ),
    (
        "<p>Это просторный интегрированный автодом для пяти человек, с полноростовым проходом между кабиной и жилым отсеком.</p>",
        "<p>A spacious integrated motorhome for five, with full standing-height walk-through between cab and living area.</p>",
    ),
    (
        "<p>У Панды есть всё необходимое для комфортного путешествия на любой срок: полноценная кухня с раковиной, газовой плитой и вместительным холодильником, большой обеденный стол, удобный санузел с душем и туалетом, горячая и холодная вода, спальные места с качественными матрасами, много окон, кондиционер и отопитель, шторки и занавески для приватности, розеточки и зарядочки, много мест для поклажи и провизии, и даже фаркоп.</p>",
        "<p>Everything for comfortable trips of any length: full galley with sink, gas hob and large fridge, big dinette, bathroom with shower and toilet, hot and cold water, quality mattresses on every berth, plenty of windows, A/C and heater, curtains for privacy, sockets and USB, generous storage — plus a tow bar.</p>",
    ),
    (
        "<p>Спальные места: 1910*1320, 1820*600, 1560*600, 1580*900.</p>",
        "<p>Sleeping berths: 1910×1320, 1820×600, 1560×600, 1580×900.</p>",
    ),
    (
        "<p>Все сидячие места оборудованы ремнями безопасности.</p>",
        "<p>All seats have seat belts.</p>",
    ),
    (
        "<p>Водить Панду — одно удовольствие. Рулится очень легко, дорогу держит уверенно, скорость набирает бодро. А уж какой шикарный панорамный вид открывается с водительского места!</p>",
        "<p>Driving Panda is a pleasure: the steering is very light, the chassis holds the road confidently, and acceleration comes briskly. And the panoramic view from the driver's seat is superb.</p>",
    ),
    (
        """<p class="price-block"><strong>Стоимость аренды зависит от длительности:</strong><br>
              — 5-10 дней — 16000 ₽ в сутки<br>
              — от 11 дней — 15000 ₽ в сутки</p>""",
        """<p class="price-block"><strong>Rental rates by trip length:</strong><br>
              — 5–10 days — 16 000 ₽ per day<br>
              — 11+ days — 15 000 ₽ per day</p>""",
    ),
    ('<a href="../contact/" class="btn btn--primary">Забронировать</a>', '<a href="../contact/" class="btn btn--primary">Book</a>'),
]

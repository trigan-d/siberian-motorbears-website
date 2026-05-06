"""Доп. замены для site/baron/index.html → site/en/baron/index.html."""

BARON_EXTRA: list[tuple[str, str]] = [
    (
        "<title>Аренда кемпера Барибал Барон от 11 000 ₽/сутки — прокат на Алтай и Байкал | Siberian motorbears</title>",
        "<title>Baribal Baron camper rental from 11 000 ₽/day — Altai & Baikal | Siberian motorbears</title>",
    ),
    (
        'content="Аренда внедорожного кемпера Барибал Барон. Выезд из Новосибирска: Горный Алтай, Байкал, Сибирь. От 11 000 ₽/сутки. Полная комплектация, постельное бельё, посуда. Бронируйте по телефону +7 (913) 460-20-50."',
        'content="Rent the Baribal Baron off-road camper. Depart from Novosibirsk: Altai, Baikal, Siberia. From 11 000 ₽/day. Fully equipped — bedding, cookware. Book at +7 (913) 460-20-50."',
    ),
    (
        'content="аренда Барибал Барон, прокат кемпера, Алтай, Байкал, Новосибирск, внедорожный кемпер"',
        'content="Baribal Baron rental, camper hire, Altai, Baikal, Novosibirsk, off-road camper"',
    ),
    (
        '<meta property="og:title" content="Аренда кемпера Барибал Барон от 11 000 ₽/сутки — прокат на Алтай и Байкал | Siberian motorbears">',
        '<meta property="og:title" content="Baribal Baron camper rental from 11 000 ₽/day — Altai & Baikal | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Аренда внедорожного кемпера Барибал Барон. Выезд из Новосибирска: Горный Алтай, Байкал, Сибирь. От 11 000 ₽/сутки. Полная комплектация, постельное бельё, посуда. Бронируйте по телефону +7 (913) 460-20-50.">',
        '<meta property="og:description" content="Rent the Baribal Baron off-road camper. Depart from Novosibirsk: Altai, Baikal, Siberia. From 11 000 ₽/day. Fully equipped — bedding, cookware. Book at +7 (913) 460-20-50.">',
    ),
    (
        '<meta name="twitter:title" content="Аренда кемпера Барибал Барон от 11 000 ₽/сутки — прокат на Алтай и Байкал | Siberian motorbears">',
        '<meta name="twitter:title" content="Baribal Baron camper rental from 11 000 ₽/day — Altai & Baikal | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Аренда внедорожного кемпера Барибал Барон. Выезд из Новосибирска: Горный Алтай, Байкал, Сибирь. От 11 000 ₽/сутки. Полная комплектация, постельное бельё, посуда. Бронируйте по телефону +7 (913) 460-20-50.">',
        '<meta name="twitter:description" content="Rent the Baribal Baron off-road camper. Depart from Novosibirsk: Altai, Baikal, Siberia. From 11 000 ₽/day. Fully equipped — bedding, cookware. Book at +7 (913) 460-20-50.">',
    ),
    (
        '{"@context":"https://schema.org","@type":"Product","name":"Аренда внедорожного кемпера «Барибал Барон»","description":"Аренда внедорожного кемпера «Барибал Барон», от 11 000 ₽."',
        '{"@context":"https://schema.org","@type":"Product","name":"Baribal Baron off-road camper rental","description":"Baribal Baron off-road camper rental from 11 000 ₽."',
    ),
    ('"unitText":"сутки"', '"unitText":"per day"'),
    (
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Барибал Барон</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../rent/">Rental</a> → <span>Baribal Baron</span></div>',
    ),
    ('alt="Кемпер Барибал Барон — аренда, фото"', 'alt="Baribal Baron camper — rental photo"'),
    (
        '<h1 style="font-size: 1.35rem;">Аренда внедорожного кемпера «Барибал Барон»</h1>',
        '<h1 style="font-size: 1.35rem;">Off-road camper «Baribal Baron» rental</h1>',
    ),
    (
        "<p>Это маленький и юркий медведь. Он понравится путешественникам, которые любят открывать новые безлюдные маршруты и предпочитают весь день находиться на свежем воздухе, а не в тесном и душном фургоне.</p>",
        "<p>This is a small, nimble bear. It suits travellers who like to find empty backroads and would rather spend the whole day outdoors than in a cramped, stuffy van body.</p>",
    ),
    (
        "<p>Барон берёт на борт до пяти человек. В пути они могут размещаться или в кабине или в спальном отсеке. Теперь кабина и спальник соединены через проём заднего окна, так что все пассажиры могут общаться друг-с-другом, а самые маленькие и ловкие — даже перелазить туда-обратно.</p>",
        "<p>Baron takes up to five people on board. On the move they can sit in the cab or in the sleeping compartment. The cab and sleeper are now linked through the rear-window opening, so all passengers can talk to each other — and the smallest and nimblest can even climb through.</p>",
    ),
    (
        "<p>На стоянке можно разложить веерную маркизу со стенками, и получить просторную комнату вокруг машины, укрытую от дождя и ветра. В этой же комнате располагается выдвижная уличная кухня, с газовой плитой, холодильником, горячей водой, и всем необходимым. С другой стороны отдельно раскладывается уличный душ. Запас воды — 90 литров, пополняется штатной леечкой в любом ручье.</p>",
        "<p>At the campsite you can open the fan awning with walls and get a spacious room around the vehicle, sheltered from rain and wind. In that same space the slide-out outdoor kitchen sits — gas hob, fridge, hot water, everything you need. On the other side the outdoor shower folds out separately. Water capacity is 90 litres, topped up with the standard filler hose from any stream.</p>",
    ),
    (
        "<p>Весь спальный отсек — это одна большая кровать 180*210 см. Дополнительно в нём имеется подвесная кровать 180*70 см. Разумеется, в спальном отсеке есть обогрев, освещение, розеточки.</p>",
        "<p>The entire sleeping area is one large bed 180×210 cm, plus an overhead bunk 180×70 cm. Naturally the sleeping compartment has heating, lighting, and outlets.</p>",
    ),
    (
        "<p>В подвесных ящиках по периметру машины можно разместить достаточно поклажи и провизии для всей компании на несколько дней. Для тех, кому этого мало, есть фаркоп. Наш медведь умеет возить прицеп :)</p>",
        "<p>Underbody boxes around the perimeter hold gear and provisions for several days. Need more? There is a tow bar — this motorbear can pull a trailer :)</p>",
    ),
    (
        "<p>Барибал уверенно идёт по хорошей трассе с крейсерской скоростью 110 км/ч. И как дома чувствует себя на просёлочной дороге, в лесу или в грязи — благодаря подтянутой фигуре и честному приводу на все 4 лапы, с понижайкой и блокировкой.</p>",
        "<p>Baribal cruises motorways at about 110 km/h and feels at home on gravel, forest tracks, or mud — compact stance, real four-wheel drive with low range and a locker.</p>",
    ),
    (
        """<p class="price-block"><strong>Стоимость аренды зависит от длительности:</strong><br>
              — 3-7 дней — 12000 ₽ в сутки<br>
              — от 8 дней — 11000 ₽ в сутки</p>""",
        """<p class="price-block"><strong>Rental rates by trip length:</strong><br>
              — 3–7 days — 12 000 ₽ per day<br>
              — 8+ days — 11 000 ₽ per day</p>""",
    ),
    ('<a href="../contact/" class="btn btn--primary">Забронировать</a>', '<a href="../contact/" class="btn btn--primary">Book</a>'),
    ('title="Видео о Барибал Барон"', 'title="Video: Baribal Baron"'),
]

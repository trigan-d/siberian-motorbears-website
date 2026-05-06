"""Доп. замены для site/panda/index.html → site/en/panda/index.html."""

PANDA_EXTRA: list[tuple[str, str]] = [
    (
        "<title>Купить интегрированный автодом Панда от 1 300 000 ₽ — производство под заказ | Siberian motorbears</title>",
        "<title>Panda integrated motorhome from 1 300 000 ₽ — built to order | Siberian motorbears</title>",
    ),
    (
        'content="Интегрированный автодом Панда на 5 человек: кухня, санузел, полноростовый проход. Производство под заказ в Новосибирске от 1 300 000 ₽. Комплектации и цены. Узнайте сроки и условия."',
        'content="Panda integrated motorhome for five: galley, bathroom, full standing-height walk-through. Built to order in Novosibirsk from 1 300 000 ₽. Options and pricing — ask for lead time."',
    ),
    (
        'content="автодом Панда, интегрированный автодом, купить автодом, производство автодомов, Новосибирск"',
        'content="Panda motorhome, integrated motorhome, buy motorhome, motorhome manufacturing, Novosibirsk"',
    ),
    (
        '<meta property="og:title" content="Купить интегрированный автодом Панда от 1 300 000 ₽ — производство под заказ | Siberian motorbears">',
        '<meta property="og:title" content="Panda integrated motorhome from 1 300 000 ₽ — built to order | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Интегрированный автодом Панда на 5 человек: кухня, санузел, полноростовый проход. Производство под заказ в Новосибирске от 1 300 000 ₽. Комплектации и цены. Узнайте сроки и условия.">',
        '<meta property="og:description" content="Panda integrated motorhome for five: galley, bathroom, full standing-height walk-through. Built to order in Novosibirsk from 1 300 000 ₽. Options and pricing — ask for lead time.">',
    ),
    (
        '<meta name="twitter:title" content="Купить интегрированный автодом Панда от 1 300 000 ₽ — производство под заказ | Siberian motorbears">',
        '<meta name="twitter:title" content="Panda integrated motorhome from 1 300 000 ₽ — built to order | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Интегрированный автодом Панда на 5 человек: кухня, санузел, полноростовый проход. Производство под заказ в Новосибирске от 1 300 000 ₽. Комплектации и цены. Узнайте сроки и условия.">',
        '<meta name="twitter:description" content="Panda integrated motorhome for five: galley, bathroom, full standing-height walk-through. Built to order in Novosibirsk from 1 300 000 ₽. Options and pricing — ask for lead time.">',
    ),
    (
        '{"@context":"https://schema.org","@type":"Product","name":"Купить интегрированный автодом Панда","description":"Купить интегрированный автодом Панда, от 1 300 000 ₽."',
        '{"@context":"https://schema.org","@type":"Product","name":"Panda integrated motorhome","description":"Panda integrated motorhome from 1 300 000 ₽."',
    ),
    (
        '<div class="container"><a href="../">Home</a> → <a href="../order/">Manufacturing</a> → <span>Автодом Панда</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../order/">Manufacturing</a> → <span>Panda motorhome</span></div>',
    ),
    ('alt="Интегрированный автодом Панда — каталог"', 'alt="Integrated Panda motorhome — gallery"'),
    (
        '<h1 style="font-size: 1.35rem;">Интегрированный автодом «Панда»</h1>',
        '<h1 style="font-size: 1.35rem;">Integrated motorhome «Panda»</h1>',
    ),
    (
        "<p>Панды изготавливаются из специализированных автомобилей на базе Газель Next со стеклопластиковым кузовом на стальном каркасе.</p>",
        "<p>Pandas are built on Gazelle Next–based donor chassis with a fibreglass body on a steel frame.</p>",
    ),
    (
        """<p>Удачная планировка жилого отсека и комбинация классических и оригинальных инженерных решений позволила с комфортом разместить сидячие и спальные места для пяти пассажиров, полноценную кухню и санузел.<br>
              И при этом внутри получилось не тесно, а вполне просторно.</p>""",
        """<p>A practical layout of the living area, together with a mix of classic and original engineering solutions, makes comfortable room for seating and sleeping for five passengers, a full kitchen, and a bathroom.</p>
              <p>Even with all that, the interior does not feel tight — it is genuinely spacious.</p>""",
    ),
    (
        """<p><strong>КОМПЛЕКТАЦИЯ:</strong><br>
              Спальные места: 1910*1320, 1820*600, 1560*600, 1580*900.<br>
              Все сидячие места оборудованы ремнями безопасности.<br>
              Запас чистой воды 70 литров, с возможностью увеличения до 200-300 литров. Бак сточной воды примерно 70 литров. Автоматический диафрагменный насос.<br>
              Салонный аккумулятор 100 Ач, с возможностью увеличения до 300 Ач. Солнечные панели суммарно 600 Ватт. Инвертор.<br>
              Освещение, розеточки, зарядочки.<br>
              Газовый баллон 5 литров (можно поставить второй), газовая плитка настольная, газовый проточный водонагреватель.<br>
              Компрессорный холодильник 55 литров.<br>
              Раковина, душ, переносной биотуалет.<br>
              Воздушный дизельный отопитель, накрышный кондиционер.<br>
              Авторская мебель ручной работы из влагостойкой фанеры.<br>
              Двигатель дизельный, 150 л.с. Привод задний. Есть фаркоп.</p>""",
        """<p><strong>STANDARD EQUIPMENT:</strong><br>
              Sleeping berths: 1910×1320, 1820×600, 1560×600, 1580×900.<br>
              All seats have seat belts.<br>
              Fresh water 70 L, expandable to about 200–300 L. Grey water tank ~70 L. Automatic diaphragm pump.<br>
              House battery 100 Ah (expandable to 300 Ah). Solar panels 600 W total. Inverter.<br>
              Lighting, sockets, USB charging.<br>
              5 L gas cylinder (second optional), portable gas hob, instant gas water heater.<br>
              55 L compressor fridge.<br>
              Sink, shower, portable cassette toilet.<br>
              Air diesel heater, roof-mounted A/C.<br>
              Custom plywood interior furniture.<br>
              Diesel engine, 150 hp. Rear-wheel drive. Tow bar fitted.</p>""",
    ),
    (
        "<p>Изготовление Панды под заказ возможно только при наличии подходящего базового шасси. Срок производства: 6 месяцев.</p>",
        "<p>Built-to-order Panda builds require a suitable donor chassis. Lead time: about 6 months.</p>",
    ),
    (
        """<p class="price-block"><strong>Цена производства без учёта шасси: 1 300 000 ₽</strong><br>
              <strong>Цена готового образца «Панда Мия»: 3 900 000 ₽</strong></p>""",
        """<p class="price-block"><strong>Build price excluding chassis: 1 300 000 ₽</strong><br>
              <strong>Ready «Panda Mia» demo unit: 3 900 000 ₽</strong></p>""",
    ),
    ('<a href="../contact/" class="btn btn--primary">Заказать</a>', '<a href="../contact/" class="btn btn--primary">Order</a>'),
]

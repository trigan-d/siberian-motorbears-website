"""Доп. замены для site/baribal/index.html → site/en/baribal/index.html."""

BARIBAL_EXTRA: list[tuple[str, str]] = [
    (
        "<title>Купить внедорожный кемпер Барибал от 700 000 ₽ — производство под заказ | Siberian motorbears</title>",
        "<title>Baribal off-road camper from 700 000 ₽ — built to order | Siberian motorbears</title>",
    ),
    (
        'content="Внедорожный кемпер Барибал на шасси УАЗ Профи 4×4. Прицеп-капля (teardrop) на бортовой платформе. Производство в Новосибирске от 700 000 ₽. Комплектации, опции, срок 2–3 месяца. Закажите расчёт."',
        'content="Baribal off-road camper on UAZ Profi 4×4. Teardrop body on a flatbed. Built in Novosibirsk from 700 000 ₽. Options, packs, lead time about 2–3 months. Ask for a quote."',
    ),
    (
        'content="кемпер Барибал, внедорожный кемпер, купить кемпер, производство кемперов, УАЗ Профи, прицеп-капля, Новосибирск"',
        'content="Baribal camper, off-road camper, buy camper, camper manufacturing, UAZ Profi, teardrop, Novosibirsk"',
    ),
    (
        '<meta property="og:title" content="Купить внедорожный кемпер Барибал от 700 000 ₽ — производство под заказ | Siberian motorbears">',
        '<meta property="og:title" content="Baribal off-road camper from 700 000 ₽ — built to order | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Внедорожный кемпер Барибал на шасси УАЗ Профи 4×4. Прицеп-капля (teardrop) на бортовой платформе. Производство в Новосибирске от 700 000 ₽. Комплектации, опции, срок 2–3 месяца. Закажите расчёт.">',
        '<meta property="og:description" content="Baribal off-road camper on UAZ Profi 4×4. Teardrop body on a flatbed. Built in Novosibirsk from 700 000 ₽. Options, packs, lead time about 2–3 months. Ask for a quote.">',
    ),
    (
        '<meta name="twitter:title" content="Купить внедорожный кемпер Барибал от 700 000 ₽ — производство под заказ | Siberian motorbears">',
        '<meta name="twitter:title" content="Baribal off-road camper from 700 000 ₽ — built to order | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Внедорожный кемпер Барибал на шасси УАЗ Профи 4×4. Прицеп-капля (teardrop) на бортовой платформе. Производство в Новосибирске от 700 000 ₽. Комплектации, опции, срок 2–3 месяца. Закажите расчёт.">',
        '<meta name="twitter:description" content="Baribal off-road camper on UAZ Profi 4×4. Teardrop body on a flatbed. Built in Novosibirsk from 700 000 ₽. Options, packs, lead time about 2–3 months. Ask for a quote.">',
    ),
    (
        '{"@context":"https://schema.org","@type":"Product","name":"Купить внедорожный кемпер Барибал","description":"Купить внедорожный кемпер Барибал, от 700 000 ₽."',
        '{"@context":"https://schema.org","@type":"Product","name":"Baribal off-road camper","description":"Baribal off-road camper from 700 000 ₽."',
    ),
    (
        '<div class="container"><a href="../">Home</a> → <a href="../order/">Manufacturing</a> → <span>Кемпер Барибал</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../order/">Manufacturing</a> → <span>Baribal camper</span></div>',
    ),
    ('alt="Внедорожный кемпер Барибал — каталог"', 'alt="Baribal off-road camper — gallery"'),
    ('title="Видео о кемпере Барибал"', 'title="Video: Baribal camper"'),
    (
        '<h1 style="font-size: 1.35rem;">Внедорожный кемпер «Барибал»</h1>',
        '<h1 style="font-size: 1.35rem;">Off-road camper «Baribal»</h1>',
    ),
    (
        """              <p>Концепция и архитектура Барибала является результатом вдумчивого анализа нашего интенсивного опыта проката, тюнинга и обслуживания автодомов.<br>
              Мы хотели создать машину, которая имеет хороший потенциал и для проката в наших условиях, и для личных путешествий, и для мелкосерийного производства.</p>""",
        """              <p>The Baribal concept and architecture are the result of careful analysis of our intensive experience in rental, tuning, and servicing motorhomes.<br>
              We wanted to create a vehicle with strong potential for rental in our conditions, for private travel, and for small-batch production.</p>""",
    ),
    (
        """              <p>Основные идеи и цели, которые мы преследовали:<br>
              — Сохранение внедорожных качеств базового шасси, включая габариты и развесовку.<br>
              — Простота в производстве, обслуживании, доработках.<br>
              — Надёжность и прочность конструкции при эксплуатации в сложных условиях.<br>
              — Ремонтопригодность и неприхотливость, отсутствие редких импортных комплектующих.<br>
              — Простой демонтаж и хранение жилого отсека для использования шасси в других целях.<br>
              — Избежать изменений в конструкции базового ТС и сложностей при постановке на учёт.<br>
              — Эксплуатация по большей части в летнее время.<br>
              — Модульная конструкция, возможность добавлять новые компоненты после покупки базовой комплектации.</p>""",
        """              <p>Main ideas and goals we pursued:<br>
              — Preserve the base chassis off-road capability, including footprint and weight distribution.<br>
              — Simplicity in manufacturing, servicing, and upgrades.<br>
              — Structural reliability and strength in demanding conditions.<br>
              — Easy to repair and maintain; no rare imported components.<br>
              — Simple removal and storage of the living module so the chassis can be used for other tasks.<br>
              — Avoid changes to the base vehicle structure and registration headaches.<br>
              — Mostly summer-season use.<br>
              — Modular design — new components can be added after you buy the base package.</p>""",
    ),
    (
        """              <p>В итоге Барибал представляет собой аналог прицепа-капли (teardrop), смонтированный на бортовой платформе грузовика-полуторки. В качестве основного шасси выбран УАЗ Профи 4х4 с двухрядной кабиной. Однако возможно изготовление и под другие шасси с бортовой платформой. Принцип использования Барибала в путешествии описывается простой формулой: «По дороге все едут в кабине, на стоянке вся жизнь проходит на улице, жилой отсек — для сна и отдыха».</p>""",
        """              <p>In the end, Baribal is essentially a teardrop trailer analogue mounted on the flatbed of a light truck. The default base chassis is a UAZ Profi 4×4 with a double cab — but we can also build on other trucks with a flatbed. How you use it on a trip follows a simple rule: «On the road everyone rides in the cab; at camp life happens outside; the living pod is for sleep and rest».</p>""",
    ),
    (
        """              <p class="price-block"><strong>Минимальный заказ на Барибала начинается от 700.000 ₽.</strong></p>""",
        """              <p class="price-block"><strong>Minimum Baribal order starts at 700.000 ₽.</strong></p>""",
    ),
    ('<a href="#prices" class="btn btn--primary">Опции и цены</a>', '<a href="#prices" class="btn btn--primary">Options & prices</a>'),
    ('<a href="../contact/" class="btn btn--secondary">Заказать</a>', '<a href="../contact/" class="btn btn--secondary">Order</a>'),
    (
        """    <section class="section" id="prices">
      <div class="container">
        <h2 class="section-title">Примерные цены</h2>
        <p class="text-muted text-center mb-0">не является публичной офертой</p>
        <div class="price-list">
          <div class="price-item"><h4>Спальный отсек:</h4><p>— корпус утепленный из сендвич-панелей<br>— одно откидное окно, одна дверь с окном<br>— основное спальное место 177х217 см<br>— подвесное спальное место 70х175 см<br>— ремни безопасности<br>— гибкое сочленение с кабиной<br>— входная лестница</p><p class="price">Цена: 700.000 ₽</p></div>
          <div class="price-item"><h4>Электрика и отопление:</h4><p>— тяговый гелевый аккумулятор 100 А/ч<br>— автохолодильник<br>— воздушный дизельный отопитель «Планар»<br>— солнечная панель с контроллером<br>— инвертор 12-220 В<br>— розетки, осветители, проводка</p><p class="price">Цена: 130.000 ₽</p></div>
          <div class="price-item"><h4>Вода и газ:</h4><p>— нержавеющий бак для чистой воды<br>— автоматический диафрагменный насос<br>— газовый баллон 2 кг<br>— проточный газовый водонагреватель<br>— шланги, фитинги<br>— душевая ширма<br>— смеситель и душевая лейка</p><p class="price">Цена: 60.000 ₽</p></div>
          <div class="price-item"><h4>Комплект подвесных ящиков:</h4><p>— 4 ящика по бокам<br>— один центральный ящик сзади</p><p class="price">Цена: 155.000 ₽</p></div>
          <div class="price-item"><h4>Маркиза:</h4><p>— складная веерная маркиза на стальном каркасе<br>— полный комплект стенок, несъёмный</p><p class="price">Цена: 65.000 ₽</p></div>
          <div class="price-item"><h4>Пакет "Комфорт" для базового шасси:</h4><p>— подлокотники<br>— демпферные рычаги КПП и РК<br>— колесные муфты на переднюю ось<br>— пневмоподвеска на заднюю ось<br>— багажник на крышу и мягкий бокс</p><p class="price">Цена: 90.000 ₽</p></div>
          <div class="price-item"><h4>Выдвижная уличная кухня/стол</h4><p class="price">Цена: 30.000 ₽</p></div>
          <div class="price-item"><h4>Комплект домкратных опор для снятия/установки спального отсека</h4><p class="price">Цена: 60.000 ₽</p></div>
          <div class="price-item"><h4>Базовое шасси</h4><p>Машинами мы не торгуем :)<br>А Барибала можем изготовить под любой бортовой грузовик на ваш вкус.</p></div>
          <div class="price-summary">
            <p><strong>Начальная комплектация:</strong> <span class="price-summary__value">700.000 ₽</span></p>
            <p><strong>Максимальная комплектация:</strong> <span class="price-summary__value">1.290.000 ₽</span></p>
            <p><strong>Монтаж на машину заказчика:</strong> <span class="price-summary__value">110.000 ₽</span></p>
            <p><strong>Срок изготовления:</strong> <span class="price-summary__value">2-3 месяца</span></p>
          </div>
        </div>
      </div>
    </section>""",
        """    <section class="section" id="prices">
      <div class="container">
        <h2 class="section-title">Indicative prices</h2>
        <p class="text-muted text-center mb-0">not a public offer</p>
        <div class="price-list">
          <div class="price-item"><h4>Sleeping module:</h4><p>— insulated sandwich-panel shell<br>— one hopper window, one door with window<br>— main berth 177×217 cm<br>— overhead berth 70×175 cm<br>— seat belts<br>— flexible seal to the cab<br>— entry ladder</p><p class="price">Price: 700.000 ₽</p></div>
          <div class="price-item"><h4>Electrics & heating:</h4><p>— 100 Ah traction gel battery<br>— compressor fridge<br>— Planar diesel air heater<br>— solar panel & controller<br>— 12–230 V inverter<br>— outlets, lights, wiring</p><p class="price">Price: 130.000 ₽</p></div>
          <div class="price-item"><h4>Water & gas:</h4><p>— stainless fresh-water tank<br>— automatic diaphragm pump<br>— 2 kg gas cylinder<br>— instant gas water heater<br>— hoses & fittings<br>— shower curtain<br>— mixer & shower head</p><p class="price">Price: 60.000 ₽</p></div>
          <div class="price-item"><h4>Underslung box set:</h4><p>— four side boxes<br>— one rear centre box</p><p class="price">Price: 155.000 ₽</p></div>
          <div class="price-item"><h4>Awning:</h4><p>— folding fan awning on steel frame<br>— full wall kit, fixed</p><p class="price">Price: 65.000 ₽</p></div>
          <div class="price-item"><h4>Base chassis “Comfort” pack:</h4><p>— armrests<br>— damped transfer-case & gearbox levers<br>— front axle hub locks<br>— rear semi-air suspension<br>— roof rack & soft cargo box</p><p class="price">Price: 90.000 ₽</p></div>
          <div class="price-item"><h4>Slide-out outdoor galley / table</h4><p class="price">Price: 30.000 ₽</p></div>
          <div class="price-item"><h4>Jack stand kit for removing / fitting the sleeping module</h4><p class="price">Price: 60.000 ₽</p></div>
          <div class="price-item"><h4>Base chassis</h4><p>We do not sell trucks :)<br>We can build a Baribal on any flatbed you prefer.</p></div>
          <div class="price-summary">
            <p><strong>Starting build:</strong> <span class="price-summary__value">700.000 ₽</span></p>
            <p><strong>Fully loaded:</strong> <span class="price-summary__value">1.290.000 ₽</span></p>
            <p><strong>Fit to customer’s chassis:</strong> <span class="price-summary__value">110.000 ₽</span></p>
            <p><strong>Lead time:</strong> <span class="price-summary__value">2–3 months</span></p>
          </div>
        </div>
      </div>
    </section>""",
    ),
]

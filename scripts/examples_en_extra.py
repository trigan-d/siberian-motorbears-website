"""Доп. замены для site/examples/index.html → site/en/examples/index.html (build_en_site). Ручной перевод, без API."""

EXAMPLES_EXTRA: list[tuple[str, str]] = [
    (
        "<title>Примеры работ — производство и переоборудование автодомов | Siberian motorbears</title>",
        "<title>Portfolio — motorhome builds & conversions | Siberian motorbears</title>",
    ),
    (
        'content="Реальные примеры автодомов и кемперов: Панда Мия, Барибал Барон, Барибал Барни, Гризли Грин, Полярный Потап, переоборудование Фиат и Трэкол. Фото готовых работ. Новосибирск."',
        'content="Real motorhome and camper projects: Panda Mia, Baribal Baron, Baribal Barny, Grizzly Green, Polar Potap; Fiat and Trekol conversions. Photos of finished work. Novosibirsk."',
    ),
    (
        'content="примеры автодомов, переоборудование автодомов, производство кемперов, Новосибирск"',
        'content="motorhome portfolio, van conversion, camper manufacturing, Novosibirsk"',
    ),
    (
        '<meta property="og:title" content="Примеры работ — производство и переоборудование автодомов | Siberian motorbears">',
        '<meta property="og:title" content="Portfolio — motorhome builds & conversions | Siberian motorbears">',
    ),
    (
        '<meta property="og:description" content="Реальные примеры автодомов и кемперов: Панда Мия, Барибал Барон, Барибал Барни, Гризли Грин, Полярный Потап, переоборудование Фиат и Трэкол. Фото готовых работ. Новосибирск."',
        '<meta property="og:description" content="Real motorhome and camper projects: Panda Mia, Baribal Baron, Baribal Barny, Grizzly Green, Polar Potap; Fiat and Trekol conversions. Photos of finished work. Novosibirsk."',
    ),
    (
        '<meta name="twitter:title" content="Примеры работ — производство и переоборудование автодомов | Siberian motorbears">',
        '<meta name="twitter:title" content="Portfolio — motorhome builds & conversions | Siberian motorbears">',
    ),
    (
        '<meta name="twitter:description" content="Реальные примеры автодомов и кемперов: Панда Мия, Барибал Барон, Барибал Барни, Гризли Грин, Полярный Потап, переоборудование Фиат и Трэкол. Фото готовых работ. Новосибирск."',
        '<meta name="twitter:description" content="Real motorhome and camper projects: Panda Mia, Baribal Baron, Baribal Barny, Grizzly Green, Polar Potap; Fiat and Trekol conversions. Photos of finished work. Novosibirsk."',
    ),
    (
        '<div class="container"><a href="../">Главная</a> → <a href="../order/">Производство</a> → <span>Примеры работ</span></div>',
        '<div class="container"><a href="../">Home</a> → <a href="../order/">Manufacturing</a> → <span>Portfolio</span></div>',
    ),
    ('<span>Примеры работ</span>', '<span>Portfolio</span>'),
    (
        '<h1 class="section-title" style="margin-bottom: 2rem; font-size: 1.35rem;">Изготовление и тюнинг автодомов, примеры работ:</h1>',
        '<h1 class="section-title" style="margin-bottom: 2rem; font-size: 1.35rem;">Motorhome builds, upgrades, and tuning — project portfolio:</h1>',
    ),
    ('alt="Пример работы — автодом Панда Мия"', 'alt="Portfolio — Panda Mia motorhome"'),
    ('alt="Пример работы — кемпер Барибал Барон"', 'alt="Portfolio — Baribal Baron camper"'),
    ('alt="Пример работы — переоборудование Фиат из Красноярска"', 'alt="Portfolio — Fiat conversion, Krasnoyarsk"'),
    ('alt="Пример работы — кемпер Барибал Барни"', 'alt="Portfolio — Baribal Barny camper"'),
    ('alt="Пример работы — переоборудование Трэкол, скорая помощь"', 'alt="Portfolio — Trekol EMS conversion"'),
    ('alt="Пример работы — автодом Полярный Потап"', 'alt="Portfolio — Polar Potap motorhome"'),
    ('alt="Пример работы — автодом Гризли Грин"', 'alt="Portfolio — Grizzly Green motorhome"'),
    ("<h3>Панда Мия</h3>", "<h3>Panda Mia</h3>"),
    (
        '<p class="product-block__text">Первый экземпляр проекта "Панда"</p>',
        '<p class="product-block__text">The first production unit of the «Panda» project.</p>',
    ),
    (
        '<div class="product-block__text">- Полный демонтаж старого наполнения автомобиля.<br>- Проектирование новой планировки и подбор инженерных решений.<br>- Производство мебели из влагостойкой фанеры.<br>- Обустройство спальных мест с качественными матрасами.<br>- Прокладка систем водоснабжения и канализации.<br>- Ревизия и модернизация электросистем.<br>- Установка солнечных панелей с контролером.<br>- Монтаж пассажирского сидения в кабине.</div>',
        '<div class="product-block__text">- Complete strip-out of the vehicle’s old interior fit-out.<br>- New layout design and selection of engineering solutions.<br>- Furniture built from moisture-resistant plywood.<br>- Sleeping berths fitted with quality mattresses.<br>- Fresh water and waste plumbing installed.<br>- Electrical systems inspected, updated, and modernised.<br>- Solar panels with charge controller.<br>- Additional passenger seat mounted in the cab.</div>',
    ),
    ("<h3>Барибал Барон</h3>", "<h3>Baribal Baron</h3>"),
    (
        '<p class="product-block__text">Вторая версия внедорожного кемпера "Барибал".</p>',
        '<p class="product-block__text">The second generation of the «Baribal» off-road camper.</p>',
    ),
    (
        '<div class="product-block__text">- Спальный отсек новой формы, с "горбом" сзади.<br>- Удобный доступ ко всей инженерной начинке для обслуживания.<br>- Новая схема сочленения спального отсека и кабины<br>- Более простая и быстрая процедура снятия/установки спального отсека.<br>- Новые подвесные ящики и водяной бак нашей собственной конструкции.<br>- Новый выдвижной кухонный модуль на телескопических направляющих.<br>- Максимальное упрощение конструкции подвесного спального места.<br>- Большая и надёжная маркиза со стенками нашей собственной конструкции.<br>- Новое откидное окно, новая входная дверь с глухим окном.<br>- Новая удобная лестница для входа в спальный отсек и доступа на крышу.</div>',
        '<div class="product-block__text">- New sleeping-pod shape with a raised “hump” at the rear.<br>- Convenient access to all systems for servicing.<br>- Revised junction between the sleeping pod and the cab.<br>- Simpler, quicker procedure for removing and refitting the sleeping pod.<br>- New underslung storage boxes and fresh-water tank of our own design.<br>- New slide-out outdoor kitchen module on telescopic slides.<br>- Fold-down overhead berth structure simplified as far as possible.<br>- Large, sturdy awning with wall panels — our own design.<br>- New hopper window; new entry door with a fixed pane.<br>- New, easier ladder for entering the sleeping pod and reaching the roof.</div>',
    ),
    ("<h3>Фиат из Красноярска</h3>", "<h3>Fiat from Krasnoyarsk</h3>"),
    (
        '<p class="product-block__text">Самодельный кастенваген приехал к нам, чтобы навести лоску</p>',
        '<p class="product-block__text">A DIY camper van arrived with us for a professional finish.</p>',
    ),
    (
        '<div class="product-block__text">- Врезка двух окон в задние распашные двери<br>- Электропривод раздвижной двери<br>- Перетяжка дверных карт, устранение огрехов в обшивке<br>- Накрышный багажник и уличное освещение<br>- Замена всех мебельных панелей на фанеру<br>- Изготовление антресольных ящиков и полочек<br>- Новая столешница для кухни и замки на ящики<br>- Обеденный столик с быстросъёмным крепелением<br>- Переделка спального места с наращиванием его высоты<br>- Заливная горловина для бака чистой воды<br>- Переделка сливного бака, водоотведение из кухни, слив кнопкой</div>',
        '<div class="product-block__text">- Two windows fitted in the rear barn doors.<br>- Power-operated sliding side door.<br>- Door cards retrimmed; flaws in the lining corrected.<br>- Roof rack and exterior lighting.<br>- All cabinet panels replaced with plywood.<br>- Overhead lockers and shelves built.<br>- New kitchen worktop and locks on the drawers.<br>- Dining table with quick-release mounting.<br>- Sleeping area reworked with increased bed height.<br>- Fill neck for the fresh water tank.<br>- Grey water tank revised; galley drain rerouted; push-button dump valve.</div>',
    ),
    ("<h3>Барибал Барни</h3>", "<h3>Baribal Barny</h3>"),
    (
        '<p class="product-block__text">Внедорожный кемпер "Барибал" - первый самостоятельный проект Siberian motorbears.</p>',
        '<p class="product-block__text">The «Baribal» off-road camper — the first fully in-house project from Siberian motorbears.</p>',
    ),
    (
        '<div class="product-block__text">- Изготовление спального отсека в штатную бортовую платформу.<br>- Монтаж подвесных ящиков под бортовой платформой.<br>- Проектирование и монтаж систем водоснабжения, отопления, электрики.<br>- Изготовление выдвижного уличного кухонного модуля с местом крепления.<br>- Окраска бортов в цвет кабины.<br>- Усовершенствование системы охлаждения двигателя.<br>- Подбор и монтаж велобагажника.<br>- Тюнинг ходовой части, внедорожная подготовка.</div>',
        '<div class="product-block__text">- Sleeping pod built into the factory flatbed.<br>- Underslung boxes mounted beneath the flatbed.<br>- Water, heating, and electrical systems — design and installation.<br>- Slide-out outdoor kitchen module with tie-down points.<br>- Flatbed sides painted to match the cab.<br>- Engine cooling system improvements.<br>- Bike rack selected and fitted.<br>- Chassis tuning and off-road preparation.</div>',
    ),
    ("<h3>Трэкол - скорая помощь</h3>", "<h3>Trekol — ambulance</h3>"),
    (
        '<p class="product-block__text">Автомобиль скорой медицинской помощи на базе снегоболотохода Трэкол изготовлен по заказу одной из клиник для отправки на вахту на севера.</p>',
        '<p class="product-block__text">An emergency medical vehicle on a Trekol all-terrain chassis, built to order for a clinic for deployment on a northern rotation.</p>',
    ),
    (
        '<div class="product-block__text">- Демонтаж старого салона Трэкола.<br>- Изготовление нового салона из влагостойкой фанеры с покраской.<br>- Изготовление мебели и крепежа для размещения необходимого медицинского оборудования.<br>- Проектирование и монтаж сетей электроснабжения 12 и 220 вольт.<br>- Изготовление медицинских ламп с гнёздами прикуривателя и крюками для капельниц.<br>- Перетяжка салона и дверей.<br>- Монтаж и подключение "мигалки".<br>- Ремонт компрессора системы подкачки колёс.</div>',
        '<div class="product-block__text">- Old Trekol cabin trim removed.<br>- New cabin built from moisture-resistant plywood and painted.<br>- Furniture and mounts for the required medical equipment.<br>- 12 V and 230 V electrical supply — design and installation.<br>- Medical examination lamps with cigarette-lighter sockets and IV hooks.<br>- Cabin and doors retrimmed.<br>- Rotating beacon fitted and wired.<br>- Tyre inflation compressor repaired.</div>',
    ),
    ("<h3>Полярный Потап</h3>", "<h3>Polar Potap</h3>"),
    (
        '<p class="product-block__text">Пожилой медведь на базе Ford Transit отработал два сезона в нашем прокате и за это время подвергся некоторым доработкам и модернизации.</p>',
        '<p class="product-block__text">An older motorbear on a Ford Transit base: two seasons in our rental fleet, with several rounds of upgrades and modernisation.</p>',
    ),
    (
        '<div class="product-block__text">- Перетяжка всей мягкой мебели в жилом отсеке и сидений в кабине.<br>- Изготовление нового блока управления электрикой.<br>- Модернизация всей электрики и медиасистем.<br>- Организация зарядки салонного аккумулятора на ходу.<br>- Врезка уличного люка для доступа в багажный отсек.<br>- Замена потолочного люка с подключением вытяжного вентилятора.<br>- Замена сломанного кемперского окна на более качественное.<br>- Изготовление велокреплений для велобагажника.<br>- Капитальный ремонт двигателя.</div>',
        '<div class="product-block__text">- All soft furniture in the living area and cab seats retrimmed.<br>- New electrical distribution / control panel built.<br>- Full electrical and media system upgrade.<br>- House battery charging from the alternator while driving.<br>- Exterior hatch cut in for access to the storage bay.<br>- Roof hatch replaced and wired to an extractor fan.<br>- Broken camper window replaced with a higher-quality unit.<br>- Bike mounts fabricated for the roof rack.<br>- Major engine overhaul.</div>',
    ),
    ("<h3>Гризли Грин</h3>", "<h3>Grizzly Green</h3>"),
    (
        '<p class="product-block__text">Медведь на базе УАЗ Профи отработал три сезона в нашем прокате и за это время поучаствовал во множестве инженерно-конструкторских экспериментов.</p>',
        '<p class="product-block__text">A motorbear on a UAZ Profi chassis: three seasons in our rental fleet and no shortage of engineering experiments along the way.</p>',
    ),
    (
        '<div class="product-block__text">- Усиление и доработка всей подвески, в т.ч. расширение задней колеи.<br>- Обшивка стен и потолка вокруг спальных мест для дополнительного утепления.<br>- Замена несущих конструкций мебели на влагостойкую ламинированную фанеру.<br>- Монтаж дополнительного бака для воды.<br>- Монтаж и подключение проточного газового водонагревателя.<br>- Замена всех водяных шлангов и смесителей, перепроектирование системы водоснабжения.<br>- Монтаж второго отопителя салона с дополнительным топливным баком.<br>- Изготовление накрышного багажника и лестницы к нему.<br>- Новый обеденный стол с более удобным подъёмным механизмом.<br>- Изготовление обтекателя между кабиной и фургоном.<br>- Подключение дополнительного аккумулятора жилого отсека.<br>- Подбор и монтаж велобагажника.<br>- Замена сидений в кабине, демонтаж ящика между ними для удобства прохода.<br>- Пневмосистема с компрессором и ресивером для регулировки пневмоподвески и подкачки колёс.</div>',
        '<div class="product-block__text">- Entire suspension reinforced and revised, including widening the rear track.<br>- Wall and ceiling lining around the sleeping berths for extra insulation.<br>- Load-bearing furniture structures replaced with moisture-resistant laminated plywood.<br>- Additional fresh-water tank fitted.<br>- Instant gas water heater installed and connected.<br>- All water hoses and mixers replaced; water supply system redesigned.<br>- Second cabin heater fitted with an extra diesel tank.<br>- Roof cargo box and access ladder built.<br>- New dining table with a more convenient lift mechanism.<br>- Wind fairing between cab and box body fabricated.<br>- Additional house battery for the living module connected.<br>- Bike rack selected and mounted.<br>- Cab seats replaced; centre storage box removed for easier walk-through.<br>- Compressed-air system with compressor and receiver for semi-air suspension adjustment and tyre inflation.</div>',
    ),
]

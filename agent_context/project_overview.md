# Siberian Motorbears — обзор проекта

## Что это

Сайт компании из Новосибирска: **производство и прокат автодомов** («моторизированные медведи»). Две основные модели: кемпер **Барибал**, автодом **Панда**. Есть продажа и аренда.

- Сайт: https://siberian-motorbears.ru
- Контакты: +7 (913) 460-20-50, siberian.motorbears@gmail.com, VK, Telegram

---

## Структура репозитория

| Папка | Назначение |
|-------|------------|
| **website_current/** | Исходный код текущего сайта. **Не изменять** без явного указания — эталон и референс. |
| **original_photos/** | Исходные фотографии до сортировки: хаотичная разбивка по папкам (baribal, baribal2, baron, panda mia, rental_page, rv_construction, goods_15, grizzly, trekol, fiat и др.). |
| **pictures/** | Целевой каталог фотографий после сортировки. Структура: порода → медведь (автодом) → **construction** / **final**; отдельно **trip_reports**. |
| **agent_context/** | Папка для сведений, помогающих агенту ориентироваться в проекте (эта папка). |

---

## Ключевые соглашения

1. **Фото для каждого медведя:**  
   - **construction** — процесс производства  
   - **final** — готовый автодом (и фото с поездок этого автодома при необходимости)

2. **Породы и медведи в pictures/:**  
   - baribal → barney, baron  
   - panda → mia  
   - grizzly → green  
   - polar → potap  
   - others → fiat_krasnoyarsk, trekol_asmp  
   - trip_reports — общие фото с поездок (аренда, природа, шоссе)

3. Маппинг источников фото (original_photos → pictures) описан в **pictures/PHOTO_SORTING_MAP.md**.

---

## Текущий сайт (website_current)

- Статичный HTML, много CSS (assets/styles/), картинки в assets/img/.
- Шрифты: Ubuntu (заголовки), Open Sans (текст).
- Страницы: / (главная), /baribal, /panda, /rent, /baron, /mia, /contact, /examples, /order, /legal, /grizzly_green, /uaz_toolboxes.
- Меню: О нас, Производство (Барибал, Панда, Примеры работ), Аренда (Барон, Мия), Контакты (VK, Telegram, телефон, email).

Обновлено: 2025-02

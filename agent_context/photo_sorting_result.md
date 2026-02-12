# Результат сортировки фотографий

**Дата:** 2025-02

## Выполнено

1. Скрипт **scripts/sort_photos.py** — копирование из `original_photos` в `pictures` по маппингу из PHOTO_SORTING_MAP.md.
2. Дедупликация по хешу содержимого: в construction/final/others каждый снимок в одном экземпляре; в trip_reports дубликаты из final допустимы, внутри trip_reports — без дубликатов.
3. Скрипт **scripts/resize_pictures.py** — ресайз только если длинная сторона > 1920 px (соотношение сторон сохранено).
4. Исправлен маппинг: baribal/sale и baribal/site → baribal/barney/final (приоритет перед общим baribal).

## Итоги

| Метрика | Значение |
|--------|----------|
| Скопировано файлов | 721 |
| Пропущено дубликатов (по хешу) | 264 |
| Ресайзено (длинная сторона > 1920 px) | 414 |

## Количество файлов по папкам (после сортировки)

| Папка | Файлов |
|-------|--------|
| baribal/barney/construction | 95 |
| baribal/barney/final | 41 |
| baribal/baron/construction | 54 |
| baribal/baron/final | 50 |
| panda/mia/construction | 37 |
| panda/mia/final | 59 |
| grizzly/green/construction | 16 |
| grizzly/green/final | 62 |
| polar/potap/construction | 14 |
| polar/potap/final | 69 |
| others/fiat_krasnoyarsk/construction | 14 |
| others/fiat_krasnoyarsk/final | 0 |
| others/trekol_asmp/construction | 52 |
| others/trekol_asmp/final | 0 |
| others/unfinished/construction | 15 |
| others/grizzly_ng2023/final | 9 |
| trip_reports | 158 |
| **Всего** | **745** |

## Дополнительный прогон (continue)

- В маппинг добавлены: **гризли нг 2023** → others/grizzly_ng2023/final, **rv_construction/unfinished** → others/unfinished/construction.
- Запуск с `--only "гризли нг 2023,rv_construction/unfinished"`: скопировано 24 файла, 1 дубликат пропущен. Ресайз: 1 файл.

## Замечания

- **others/fiat_krasnoyarsk/final** и **others/trekol_asmp/final** пустые: по маппингу fiat и trekol отнесены к construction; при необходимости часть можно вручную перенести в final.
- **original_photos** не изменён (архив).
- Инкрементальный запуск: `python3 scripts/sort_photos.py --no-resize --only "префикс1,префикс2"` — копирует только указанные источники, учитывает уже лежащие в pictures хеши (дубликаты не создаёт).

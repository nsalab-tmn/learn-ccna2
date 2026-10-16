# Инструменты аудита упоминаний вендора

Скрипты, которыми построены `audit/vendor-mentions.csv`, `audit/vendor-mentions.md`, `audit/dictionary-hits.csv` и `audit/demarketing-tiers.csv`. Они нужны, чтобы повторить аудит после правок или провести такой же на CCNA1/CCNA3.

`audit/demarketing-plan.md` написан вручную и скриптами **не** генерируется.

## Зависимости

```bash
apt-get install tesseract-ocr tesseract-ocr-rus librsvg2-bin imagemagick poppler-utils
pip install python-docx
npm install playwright        # кадры анимаций; можно указать готовый Chromium через CHROMIUM_PATH
```

## Запуск

```bash
audit/tools/run.sh                                  # полный прогон, результаты копируются в audit/
NO_INSTALL=1 audit/tools/run.sh                     # результаты остаются в $AUDIT_WORK/audit — для сравнения
SKIP_VISUAL=1 audit/tools/run.sh                    # без рендера и OCR: переиспользовать $AUDIT_WORK
AUDIT_WORK=/path/to/scratch audit/tools/run.sh      # рабочий каталог; по умолчанию $TMPDIR/vendor-audit
```

Каталог `audit/` исключается из всех проходов: в нём сам аудит, а его CSV иначе совпадали бы со словарём.

## Конвейер

| шаг | скрипт | что делает | выход (в `$AUDIT_WORK`) |
|---|---|---|---|
| 1 | `render_svgs.sh` | рендер всех SVG (`rsvg-convert -b white -w 1600`) + OCR eng+rus (`--psm 11`, `OMP_THREAD_LIMIT=1`) | `render/svg/`, `ocr/` |
| 2 | `ocr_rasters.sh` | OCR всех растров: GIF — первый кадр, картинки уже 1200 px — увеличение ×2 | `ocr_raster/` |
| 3 | `extract_embedded.py` | извлечение встроенных `<image href="data:…">` из SVG, дедупликация по sha256 | `render/embedded/`, `out/embedded.json` |
| 4 | `anim_frames.js` | кадры анимаций SMIL на 12/32/52/72/92 % (Chromium: `pauseAnimations` + `setCurrentTime`) | `render/anim/` |
| 5 | `contact_sheets.py` | контакт-листы для просмотра глазами | `sheets/` |
| 6 | `docs_scan.py` | текст `.docx` (тело, таблицы, колонтитулы) и `.pdf` → словарь | `docs/`, `out/doc_hits.json` |
| 7 | `ocr_scan.py` | словарь по OCR-тексту SVG и растров | `out/ocr_hits.json` |
| 8 | `scan.py` | словарь по всем текстовым файлам построчно, с контекстом: код, HTML-комментарий, номер вопроса квиза | `out/hits.json` |
| 9 | `classify.py` | попадание → строка карты или исключение (синтаксис CLI, ложное совпадение); слияние соседних попаданий в фразу; категория, действие, код решения `[D…]` | `out/rows_text.json`, `out/ledger_text.json` |
| 10 | `visual_rows.py` | строки по картинкам, анимациям, документам, лабам и курсу в целом — **по результатам просмотра глазами** | `out/rows_visual.json` |
| 11 | `assemble.py` | порядок строк по курсу, `id`, журнал попаданий, сверка N = M + K | `audit/vendor-mentions.csv`, `audit/dictionary-hits.csv` |
| 12 | `report.py` | сводка с таблицами покрытия и сверки | `audit/vendor-mentions.md` |
| 13 | `plan_tiers.py` | ярус и пункт плана для каждой строки, которую видит обучающийся | `audit/demarketing-tiers.csv` |

Общие пути и список файлов курса — `common.py`. Словарь — `terms.py`: термины из issue и добавленные по ходу, с пометкой `origin`.

## Что привязано к CCNA2 и требует ручной работы на другом курсе

- **`visual_rows.py`** — вердикты по картинкам записаны вручную после просмотра контакт-листов:
  - какие растры несут иконки NetAcad, логотипы, GUI WLC или PT;
  - подписи иллюстраций, которые OCR не распознал;
  - строки по видео, лабам и курсу.

  Для другого курса этот файл пишется заново по его контакт-листам.
- **`classify.py`** — исключения для ложных совпадений (`Compensates`, `PT Mono`, адрес `C80084AEF101`) и тексты `PROTO_NOTES` с рекомендациями.
- **`report.py`** — текст решений D1–D13 и отдельные места сводки (например, «видео вне аудита»).
- **`plan_tiers.py`** — разбиение на пункты плана; повторяет логику `demarketing-plan.md`.
- **Figma.** Конвейер читает только экспортированные SVG. Если доступен токен Figma, подписи иллюстраций надёжнее собрать из узлов `TEXT` (`GET /v1/files/<file>/nodes?ids=…`) и сверить с OCR.

## Проверка

Повторный прогон на том же срезе курса даёт те же `vendor-mentions.csv`, `dictionary-hits.csv` и `demarketing-tiers.csv`. В `vendor-mentions.md` меняется только строка «Срез» (коммит и дата).

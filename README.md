# Metro Product Parser

Этот скрипт предназначен для парсинга информации о продуктах из заданной категории магазина Метро. Он собирает следующие данные о каждом продукте:

- ID продукта
- Название продукта
- Ссылка на продукт
- Регулярная цена
- Промо цена (если есть)
- Название бренда

Собранные данные сохраняются в JSON файл для дальнейшего использования.

## Пример визуализации JSON

Ниже приведен пример визуализации структуры JSON файла `products.json` с помощью сервиса https://jsonviewer.stack.hu:

![JSON Viewer Screenshot](jsonexample.jpg)

## Требования

- Python 3.12

## Настройка

1. Зарегистрируйтесь на сайте [Apollo Studio](https://studio.apollographql.com/graph).

2. Укажите `https://api.metro-cc.ru/products-api/graph` в качестве нужного API.

3. Получите ссылку на граф (Graph URL) и граф реф (Graph Ref).

4. Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:
- URL=<ваша_ссылка_на_граф>
- GRAPH_REF=<ваш_граф_реф>



Замените `<ваша_ссылка_на_граф>` и `<ваш_граф_реф>` на соответствующие значения, полученные на шаге 3.

## Установка зависимостей

Установите необходимые зависимости, выполнив следующую команду:
pip install -r requirements.txt



## Использование

1. При необходимости отредактируйте следующие переменные в файле `main.py`:

   - `STORE_ID`: ID магазина Метро (по умолчанию `13`)
   - `CATEGORY_NAME`: Название категории продуктов (по умолчанию `"Кофе"`)

2. Запустите скрипт, выполнив следующую команду:
python main.py

3. После завершения работы скрипта, данные о продуктах будут сохранены в файле `products.json` в корневой директории проекта.

## Примечания

- Скрипт собирает информацию только о первых 101 продуктах из заданной категории, но количество можно увеличить.
- При возникновении ошибок во время выполнения скрипта, они будут выведены в консоль.

Автор: [stillhappy](https://github.com/stillhappy)

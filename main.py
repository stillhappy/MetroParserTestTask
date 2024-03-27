import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from environs import Env
import logging

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Конфигурируем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

# Создаем экземпляр класса Env для загрузки переменных окружения
env = Env()
env.read_env()

# Создаем транспорт для выполнения GraphQL-запроса
transport = RequestsHTTPTransport(
    url=env('URL'),  # URL-адрес GraphQL-сервера
    headers={'apollographql-client-name': env('GRAPH_REF')},  # Заголовок с именем клиента
    use_json=True,
)

def main(transport):
    # Параметры запроса
    store_id = 13  # id магазина
    search_text = "Кофе"  # Название категории
    base_url = "online.metro-cc.ru"

    # GraphQL-запрос
    query = gql('''
    query Query($storeId: Int!, $text: String!) {
      search(storeId: $storeId, text: $text) {
        products(from: 0, size: 101) {
          products {
            id
            name
            url
            manufacturer {
                name
            }
            stocks {
              prices {
                price
                old_price
              }
            }
          }
        }
      }
    }
    ''')

    # Создаем клиент GraphQL
    client = Client(transport=transport, fetch_schema_from_transport=False)

    try:
        # Выполнение GraphQL-запроса
        result = client.execute(query, variable_values={'storeId': store_id, 'text': search_text})

        # Создание словаря для последующего сохранения в формате JSON
        res = {'JSON': []}

        # Обход JSON
        for product in result['search']['products']['products']:
            # Проверка наличия необходимых данных
            if 'id' in product and 'name' in product and 'url' in product and 'stocks' in product and len(
                    product['stocks']) > 0:
                prices = product['stocks'][0]['prices']
                regular_price = prices['old_price'] if 'old_price' in prices else prices.get('price')
                promo_price = prices['price'] if 'old_price' in prices else None

                # Добавление информации о продукте в словарь res (id, name, url, regular_price, promo_price, brand)
                res['JSON'].append({
                    'id': product['id'],
                    'name': product['name'],
                    'url': f"{base_url}{product['url']}",
                    'regular_price': regular_price,
                    'promo_price': promo_price,
                    'brand': product['manufacturer']['name'] if 'manufacturer' in product else None
                })

        # Сохранение результата в файл JSON
        with open('products.json', 'w') as file:
            json.dump(res, file, indent=2)

        logger.info("Данные успешно сохранены в файл products.json")

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    logger.info('Starting parser')
    main(transport)
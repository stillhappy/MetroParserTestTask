import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from environs import Env

# Создаем экземпляр класса Env для загрузки переменных окружения
env = Env()
env.read_env()

# Создаем транспорт для выполнения GraphQL-запроса
transport = RequestsHTTPTransport(
    url=env('URL'),  # URL-адрес GraphQL-сервера
    headers={'apollographql-client-name': env('GRAPH_REF')},  # Заголовок с именем клиента
    use_json=True,
)

# Создаем клиент GraphQL
client = Client(transport=transport, fetch_schema_from_transport=False)

# GraphQL-запрос
query = gql('''
query Query {
  search(storeId: 13, text: "Кофе") {
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
            discount
            online_levels {
                price
            }
            offline {
              price
              old_price
            }
          }
        }
      }
    }
  }
}
''')

# Выполнение GraphQL-запроса
result = client.execute(query)

# Создание словаря для последующего сохранения в формате JSON
res = {'JSON': []}

# Обход JSON
for product in result['search']['products']['products']:
    # Добавление информации о продукте в словарь res (id, name, url, regular_price, promo_price, brand)
    res['JSON'].append({'id': product['id'],
                        'name': product['name'],
                        'url': f'online.metro-cc.ru{product['url']}',
                        'regular_price': product['stocks'][0]['prices']['old_price'] if product['stocks'][0]['prices']['old_price'] else product['stocks'][0]['prices']['price'],
                        'promo_price': product['stocks'][0]['prices']['price'] if product['stocks'][0]['prices']['old_price'] else None,
                        'brand': product['manufacturer']['name']})

# Сохранение результата в файл JSON
with open('products.json', 'w') as file:
    json.dump(res, file, indent=2)


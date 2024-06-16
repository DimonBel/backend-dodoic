import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import json


def get_first_link(query):
    url = f"https://www.google.com/search?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Выполняем запрос
    response = requests.get(url, headers=headers)

    # Парсим HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Находим первый результат поиска
    search_results = soup.find_all('div', class_='yuRUbf')
    if search_results:
        first_result = search_results[0].find('a')['href']
        return first_result
    else:
        return "No results found"

with open('logic.txt', 'r') as file:
    data = json.load(file)
    if data:
        first_item = data[0]
        choose = list(first_item.keys())[0]
        catalog = first_item[choose]

        # Assign each key and its first value to a separate variable
        key = list(first_item.keys())[0]
        check = first_item[key][0]
        print(check)
    else:
        print("No data found in the file.")


first_phone = 'Xiaomi Redmi Note 13 Pro'
seconnd_phone = 'Xiaomi Redmi Note 14 Pro 4G'

query = f"site:ek.ua {first_phone} vs {seconnd_phone}"
print (query)

first_link = get_first_link(query)
print(f"The first link for the query '{query}' is: {first_link}")


def get_image_url_by_alt(alt_text):
    params = {
        "q": alt_text,
        "tbm": "isch",
        "api_key": "YOUR_SERPAPI_API_KEY"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    if "images_results" in results:
        return results["images_results"][0]["original"]
    return ""

# url = "https://e-catalog.com/cmp/97125/iphone-15-pro-128gb-vs-iphone-14-pro-128gb/"

response = requests.get(first_link)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', id='compare_table')

if table:
    # Удаляем все кнопки
    for button in table.find_all('button'):
        button.decompose()

    # Удаляем все ссылки, которые являются кнопками
    for link in table.find_all('a'):
        if 'onclick' in link.attrs:
            link.decompose()

    # Удаляем заголовки с классом "compare-model-price"
    for th in table.find_all('th', class_='compare-model-price'):
        th.decompose()

    # Удаляем все атрибуты href из ссылок
    for link in table.find_all('a'):
        if 'href' in link.attrs:
            del link['href']

    # Заменяем src у изображений
    for img in table.find_all('img'):
        alt_text = img.get('alt')
        new_src = get_image_url_by_alt(alt_text)
        if new_src:
            img['src'] = new_src
            if 'srcset' in img.attrs:
                del img['srcset']

    # Записываем результат в файл
    with open("cleaned_table.txt", "w", encoding="utf-8") as file:
        file.write(table.prettify())
else:
    print("Таблица с id='compare_table' не найдена.")

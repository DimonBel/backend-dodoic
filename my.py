import requests
from bs4 import BeautifulSoup


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

first_phone = 'Xiaomi Redmi Note 13 Pro'
seconnd_phone = 'Xiaomi Redmi Note 14 Pro 4G'

query = f"site:ek.ua {first_phone} vs {seconnd_phone}"
print (query)

first_link = get_first_link(query)
print(f"The first link for the query '{query}' is: {first_link}")
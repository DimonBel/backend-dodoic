from flask import Flask, request, jsonify, send_file, Response, send_from_directory
from flask_cors import CORS
import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json
import requests
from serpapi import GoogleSearch


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


#sadfhjasdhbjkdsabhjdfghdsfjdsghkdshjkkl

def get_link(query):
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

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base_dir, 'received_data.txt')
output = os.path.join(base_dir, 'output.txt')


# Function to read data from the file
def read_data_from_file():
    if os.path.exists(output):
        with open(output, 'r') as f:
            data = json.load(f)
        return data


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def handle_data():
    global categoryyyy
    if request.method == 'POST':
        data = request.json
        if data is not None:
            with open(filename, 'w') as f:
                json.dump(data, f)  # Use json.dump() to directly write JSON data to file
                
            # Assuming the JSON content is stored in a file called 'output.txt'
            with open('received_data.txt', 'r') as file:
                data = json.load(file)
            
            choose = list(data.keys())[1]
            catalog = data[choose]

            # Assign each key and its first value to a separate variable
            key = list(data.keys())[0]
            check = data[key][0]
            print(check)

            if check == "r": #response 
                with open('output.txt', 'r') as file:
                    data = json.load(file)
                # Assign each key and its first value to a separate variable
                key0 = list(data.keys())[0]
                key1 = list(data.keys())[1]
                key2 = list(data.keys())[2]
                key3 = list(data.keys())[3]
                
                with open('received_data.txt', 'r') as file:
                    data = json.load(file)
                    
                value1 = data['answer_sent'][0]
                value0 = data['answer_sent'][1]
                value2 = data['answer_sent'][2]
                value3 = data['answer_sent'][3]
                value4 = data['url']
                
                with open('output.txt', 'r') as file:
                    data = json.load(file)
                
                choose = list(data.keys())[1]
                catalog = categoryyyy

                client = OpenAI(api_key="sk-proj-1ynBJsNXjeztY6jsXdCDT3BlbkFJ9BTyTMtwSsyH6gcpU8EW")

                MODEL = "gpt-4o"
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": f"Find 3 real fucking names of {catalog} on {value4} site with the following parameters {key0}: {value0}, {key1}: {value1}, {key2}: {value2}, {key3}: {value3}, write them down in the following json format, strictly follow this format and do not write anything other than this without any explanation. Also do not include price."}
                    ]
                )
                response_content = completion.choices[0].message.content
                
                print(f"-----\nFind 3 real names of {catalog} on {value4} site with the following approximately parameters {key0}: {value0}, {key1}: {value1}, {key2}: {value2}, {key3}: {value3}, write them down in the following json format, strictly follow this format and do not write anything other than this without any explanation. Also do not include price.-----")
                # Write the response to a file
                
                print(f"{value4}")
                with open('logic.txt', 'w') as f:
                    lines = response_content.split('\n')
                    lines = lines[1:-1]
                    response_content = '\n'.join(lines)
                    f.write(response_content)
                    
                print("Response")
                
                file_path = 'logic.txt'
                with open(file_path, 'r') as file:
                    data_str = file.read()

                # Загрузка строки как JSON объекта
                data = json.loads(data_str)

                # Обновление названий с ссылками
                # updated_data = [{"name": item["name"], "link": get_link(f"site:{value4} {item["name"]}")} for item in data]
                updated_data = []
                for item in data:
                    if "name" in item:
                        updated_data.append({"name": item["name"], "link": get_link(f"site:{value4} {item['name']}")})
                    else:
                        # Handle the error appropriately, e.g., log it or raise an exception
                        print(f"Warning: Missing 'name' key in item: {item}")
                        # Optionally, you can append a default value or handle it otherwise
                        updated_data.append({"name": "unknown", "link": get_link(f"site:{value4} unknown")})
  
                # Запись обновленных данных обратно в файл
                with open(file_path, 'w') as file:
                    json.dump(updated_data, file, indent=4)
                
                with open('logic.txt', 'r') as f:
                    data = json.load(f)
                return data

            elif check == "c":
                client = OpenAI(api_key="sk-proj-1ynBJsNXjeztY6jsXdCDT3BlbkFJ9BTyTMtwSsyH6gcpU8EW")

                MODEL = "gpt-4o"
                
                choose = list(data.keys())[1]
                value0 = data[choose]
                print("<<<<<<"+value0+">>>>>>>>")
                categoryyyy = value0
                
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": f"""
                Write what are the main 4 criteria for choosing a {value0}, write them in the following json format, strictly follow this format and don't write anything other than this without any explanation, just the category names. Also write sub-items in the form of an array for each category which will be levels for example let's say we are choosing a phone for it will be like this json output:

                {{
                    "Battery Life": [
                        "8 hours",
                        "10 hours",
                        "12 hours",
                        "24 hours"
                    ],
                    "Camera Quality": [
                        "12 MP",
                        "48 MP",
                        "108 MP"
                    ],
                    "Performance": [
                        "Low",
                        "Medium",
                        "High"
                    ],
                    "Display": [
                        "LCD",
                        "OLED",
                        "QHD"
                    ],
                    "helpinfo": [
                        "help in 1",
                        "help in 2",
                        "help in 3",
                        "help in 4"
                    ]
                }}
                Add to "helpinfo" a short description of each criteria. Also don't include price in categorization. Write categories and subcategories in as simple language as possible, don't use complicated terminology. There should not be two subcategories everywhere, but a logical number between 2 and 5.
                
                
                """}
                    ]
                )
                response_content = completion.choices[0].message.content
                # Write the response to a file
                with open('output.txt', 'w') as f:
                    f.write(response_content)
                print("cotegory")  
                
                with open('output.txt', 'r') as f:
                    data = json.load(f)
                return data  
            
            elif check == "t": #table
                # first_phone = 'Xiaomi Redmi Note 13 Pro'
                # seconnd_phone = 'Xiaomi Redmi Note 14 Pro 4G'

                # query = f"site:ek.ua {first_phone} vs {seconnd_phone}"
                # print (query)

                # first_link = get_first_link(query)
                # print(f"The first link for the query '{query}' is: {first_link}")


                # def get_image_url_by_alt(alt_text):
                #     params = {
                #         "q": alt_text,
                #         "tbm": "isch",
                #         "api_key": "YOUR_SERPAPI_API_KEY"
                #     }

                #     search = GoogleSearch(params)
                #     results = search.get_dict()
                #     if "images_results" in results:
                #         return results["images_results"][0]["original"]
                #     return ""

                # # url = "https://e-catalog.com/cmp/97125/iphone-15-pro-128gb-vs-iphone-14-pro-128gb/"

                # response = requests.get(first_link)
                # response.raise_for_status()

                # soup = BeautifulSoup(response.text, 'html.parser')

                # table = soup.find('table', id='compare_table')

                # if table:
                #     # Удаляем все кнопки
                #     for button in table.find_all('button'):
                #         button.decompose()

                #     # Удаляем все ссылки, которые являются кнопками
                #     for link in table.find_all('a'):
                #         if 'onclick' in link.attrs:
                #             link.decompose()

                #     # Удаляем заголовки с классом "compare-model-price"
                #     for th in table.find_all('th', class_='compare-model-price'):
                #         th.decompose()

                #     # Удаляем все атрибуты href из ссылок
                #     for link in table.find_all('a'):
                #         if 'href' in link.attrs:
                #             del link['href']

                #     # Заменяем src у изображений
                #     for img in table.find_all('img'):
                #         alt_text = img.get('alt')
                #         new_src = get_image_url_by_alt(alt_text)
                #         if new_src:
                #             img['src'] = new_src
                #             if 'srcset' in img.attrs:
                #                 del img['srcset']

                #     # Записываем результат в файл
                #     with open("cleaned_table.txt", "w", encoding="utf-8") as file:
                #         file.write(table.prettify())
                # else:
                #     print("Таблица с id='compare_table' не найдена.")
                #################################
                # FILE_PATH = 'cleaned_table.html'
                # try:
                #     # Проверьте, существует ли файл
                #     if os.path.exists(FILE_PATH):
                #         with open(FILE_PATH, 'r', encoding='utf-8') as file:
                #             content = file.read()
                #         return jsonify({"content": content})
                #     else:
                #         return jsonify({"error": "File not found!"}), 404
                # except Exception as e:
                #     return jsonify({"error": str(e)}), 500
                def read_file_lines(file_path):
    # Initialize an empty list to store the lines
                    lines = []
                    
                    # Open and read the file
                    with open(file_path, 'r') as file:
                        # Read all lines
                        lines = [line for line in file.readlines()]
                    
                    return lines

                # Define the path to the text file
                file_path = 'cleaned_table.txt'

                # Call the function and get the lines
                lines = read_file_lines(file_path)

                # Print the lines without any modification
                for line in lines:
                    print(line, end='')
                    
                data = lines
                return data
            else:
                print('TI dodic')
            if data is not None:
                return data
            else:
                return jsonify({'message': 'No data available'}), 404
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
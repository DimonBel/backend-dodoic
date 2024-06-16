from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json
import requests
from serpapi import GoogleSearch

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
                
                print(f"-----\nFind 3 real fucking names of {catalog} on {value4} site with the following approximately parameters {key0}: {value0}, {key1}: {value1}, {key2}: {value2}, {key3}: {value3}, write them down in the following json format, strictly follow this format and do not write anything other than this without any explanation. Also do not include price.-----")
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
                    ]
                }}
                Also don't include price in categorization. Write categories and subcategories in as simple language as possible, don't use complicated terminology. There should not be two subcategories everywhere, but a logical number between 2 and 5.
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
            
            
            else:
                print('TI dodic')
            
            if data is not None:
                return jsonify(data)
            else:
                return jsonify({'message': 'No data available'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
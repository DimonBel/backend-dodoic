import json
from flask import Flask, jsonify
from openai import OpenAI

app = Flask(__name__)

def get_link(query):
    # Placeholder function implementation
    return f"https://example.com/search?q={query}"

@app.route('/', methods=['POST'])
def handle_data():
    try:
        check = "r"  # This value should come from your request logic
        
        if check == "r":  # response
            with open('output.txt', 'r') as file:
                data = json.load(file)
            
            # Assign each key and its first value to a separate variable
            keys = list(data.keys())
            key0, key1, key2, key3 = keys[:4]

            with open('received_data.txt', 'r') as file:
                data = json.load(file)

            value1 = data['answer_sent'][0]
            value0 = data['answer_sent'][1]
            value2 = data['answer_sent'][2]
            value3 = data['answer_sent'][3]
            value4 = data['url']

            with open('output.txt', 'r') as file:
                data = json.load(file)

            catalog = "categoryyyy"

            client = OpenAI(api_key="sk-proj-1ynBJsNXjeztY6jsXdCDT3BlbkFJ9BTyTMtwSsyH6gcpU8EW")
            MODEL = "gpt-4o"
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "content": f"Find 3 real names of {catalog} on {value4} site with the following parameters {key0}: {value0}, {key1}: {value1}, {key2}: {value2}, {key3}: {value3}, write them down in the following json format, strictly follow this format and do not write anything other than this without any explanation. Also do not include price."}
                ]
            )
            response_content = completion.choices[0].message.content

            with open('logic.txt', 'w') as f:
                f.write(response_content)

            with open('logic.txt', 'r') as file:
                data_str = file.read().strip()  # Strip any extraneous whitespace

            # Загрузка строки как JSON объекта
            try:
                data = json.loads(data_str)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return jsonify({'error': 'Invalid JSON data'}), 400

            # Обновление названий с ссылками
            updated_data = []
            for item in data:
                if "name" in item:
                    updated_data.append({"name": item["name"], "link": get_link(f"site:{value4} {item['name']}")})
                else:
                    print(f"Warning: Missing 'name' key in item: {item}")
                    updated_data.append({"name": "unknown", "link": get_link(f"site:{value4} unknown")})

            # Запись обновленных данных обратно в файл
            with open('logic.txt', 'w') as file:
                json.dump(updated_data, file, indent=4)

            return jsonify(updated_data)
        else:
            return jsonify({'message': 'Invalid check value'}), 400

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == "__main__":
    app.run(debug=True)

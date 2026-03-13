import requests

url = "http://127.0.0.1:8000/send_text"
data = {
    "token": "BOT TOKEN", 
    "chat_id": "ЧАТ АЙДИ ДОЛЖЕН БЫТЬ В формате INT", 
    "message": {"text": "Hello from Python!"}
}

response = requests.post(url, json=data)

print(f"Статус-код: {response.status_code}")
print(f"Ответ: {response.json()}")
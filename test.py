import requests

url = "http://127.0.0.1:4000/render"
data = {
  "template": "index",
  "data": {
    "name": "World"
  },
  "templates": {
    "base": "<html><body>{% block body %}{% endblock %}</body></html>",
    "index": "{% extends 'base' %}{% block body %}Привет, {{ name }}!{% endblock %}"
  }
}

response = requests.post(url, json=data, auth = ("test_user", "user"))

print(f"Статус-код: {response.status_code}")
print(f"Ответ: {response.json()}")
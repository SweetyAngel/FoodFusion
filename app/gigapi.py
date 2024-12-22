import requests
import tomllib
import json

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

GIGAPI_TOKEN = config["gigapi"]["token"]
LIMIT = config["gigapi"]["limit"]

url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {GIGAPI_TOKEN}'
}

def get_recipe(ingredients: str) -> str:
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
            "role": "system",
            "content": "Ты - профессиональный шеф-повар. Пользователь передаст тебе список продуктов. Твоя задача - предложить рецепт того, что можно приготовить, пользуясь ТОЛЬКО этими ингредиентами.\n\nФормат ответа:\n```\n<Название блюда>\n<Подробное руководство, как это блюдо приготовить>\n```.\nТочно следуй этому формату. Если ничего из этих ингредиентов приготовить нельзя или ты не понял, что это за ингредиенты, в ответ дай пустую строчку."
            },
            {
            "role": "user",
            "content": ingredients[:LIMIT]
            }
        ],
        "stream": False,
        "update_interval": 0
    })

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return response.json()["choices"][0]["message"]["content"]

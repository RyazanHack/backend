import aiohttp
import asyncio


class YAGPTService:
    async def get_reason(self, region: str):
        prompt = {
            "modelUri": "gpt://b1g2ahktcv1255vqabvd/yandexgpt",
            "completionOptions": {
                "stream": False,
                "temperature": 0.5,
                "maxTokens": "2000",
            },
            "messages": [
                {
                    "role": "system",
                    "text": "Ты должен помочь пользователю определить, зачем ему инвестировать в развитие пешего туризма"
                    "в какую-то конкретную область. В своём сообщении опиши краткую историю области."
                    "Используй примерно 200 символов.",
                },
                {
                    "role": "user",
                    "text": f"Напиши о причинах инвестиции в {region}",
                },
            ],
        }

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Api-Key AQVN2Vd-gMlDAjVPAKNMAYxb7t6JpNOag60-Mcgz",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=prompt) as resp:
                result = await resp.json()
                result = result["result"]["alternatives"][0]["message"]["text"]
                result = result.replace("#", "")
                result = result.replace("*", "")
        return result

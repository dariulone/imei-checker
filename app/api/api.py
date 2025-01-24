import aiohttp


async def get_services_from_api(api_token):
    url = "https://api.imeicheck.net/v1/services"
    headers = {
        "Authorization": f"Bearer {api_token}",
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return None
        except Exception as e:
            return None


async def check_imei(message, imei, service_id, api_token):
    url = "https://api.imeicheck.net/v1/checks"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept-Language": "en",
        "Content-Type": "application/json"
    }

    payload = {
        "deviceId": imei,
        "serviceId": service_id
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status == 200 or 201:
                    data = await response.json()

                    if "properties" in data:
                        properties = data["properties"]
                        message_text = f"Информация о устройстве: {imei}\n"
                        for key, value in properties.items():
                            message_text += f"**{key}**: {value}\n"

                        if 'image' in properties:
                            image_url = properties['image']
                            await message.answer(message_text, parse_mode="Markdown", photo=image_url)
                        else:
                            await message.answer(message_text, parse_mode="Markdown")
                    else:
                        await message.answer("Ошибка: не удалось получить информацию о устройстве.")
                else:
                    await message.answer(f"Ошибка при проверке IMEI. Статус: {response.status}")
        except Exception as e:
            await message.answer(f"Произошла ошибка при запросе к серверу: {e}")

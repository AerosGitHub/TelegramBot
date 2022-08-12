import requests
import subprocess
from datetime import date
import folderID_modul


def get_IAM_TOKEN():
    last_get_token_data = open('YandexTranslator/Last_get_Token', mode='r').read()
    today_date = str(date.today()).split('-')[2]
    if int(today_date) > int(last_get_token_data):
        token = str(subprocess.check_output('yc iam create-token'))[2:-3]
        open('YandexTranslator/IM_TOKEN', mode='w').write(token)
        open('YandexTranslator/Last_get_Token', mode='w').write(today_date)
    else:
        token = open('YandexTranslator/IM_TOKEN').read()
    return token


def do_translate(user_text: str):
    IAM_TOKEN = get_IAM_TOKEN()
    folder_id = folderID_modul.ID['folder_id']
    target_language = 'ru'
    texts = "{}".format(user_text)

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )

    return response.json()['translations'][0]['text']
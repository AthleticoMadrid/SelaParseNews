# добавление новой новости в словарь:
import json

# открытие словаря:
with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

# ID-новости:
search_id = "528346"

# условие проверки:
if search_id in news_dict:
    print("Новость уже есть в словаре, пропускаем итерацию")
else:
    print("Свежая новость, добавляем в словарь")
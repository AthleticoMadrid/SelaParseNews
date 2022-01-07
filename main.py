import json
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime


#функция парсинга (отработает лишь в самом начале):
def get_first_news():
    headers = { 
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="article-card")

    news_dict = {}
    for article in articles_cards:
        article_title = article.find("h2", class_="article-card-title").text.strip()
        article_desc = article.find("p").text.strip()
        article_url = f'https://www.securitylab.ru{article.get("href")}'
# преобразование даты публикации в компьютерную (кол-во секунд с 01.01.1970 г.):        
        article_date_time = article.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(article_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
        article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())
# заберём ID у каждой новости:
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

#      print(f"{article_title} | {article_url} | {article_date_timestamp}")           #первый промежуточный вывод

# заполним словарь:
        news_dict[article_id] = {
            "article_date_timestamp": article_date_timestamp,
            "article_title": article_title,
            "article_url": article_url,
            "article_desc": article_desc
        }


# сохраняем результат работы:
    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


# функция обновления новостей:
def check_news_update():
    with open("news_dict.json", encoding='utf-8') as file:
        news_dict = json.load(file)

#    print(news_dict)        #вывод словаря с JSON-файлом

    headers = { 
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

    url = "https://www.securitylab.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("a", class_="article-card")

    fresh_news = {}                                         #словарь для новинок
    for article in articles_cards:
        article_url = f'https://www.securitylab.ru{article.get("href")}'
        article_id = article_url.split("/")[-1]
        article_id = article_id[:-4]

        if article_id in news_dict:
            continue
        else:
            article_title = article.find("h2", class_="article-card-title").text.strip()
            article_desc = article.find("p").text.strip()
# преобразование даты публикации в компьютерную (кол-во секунд с 01.01.1970 г.):        
            article_date_time = article.find("time").get("datetime")
            date_from_iso = datetime.fromisoformat(article_date_time)
            date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")
            article_date_timestamp = time.mktime(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timetuple())

            news_dict[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc
            }

            fresh_news[article_id] = {
                "article_date_timestamp": article_date_timestamp,
                "article_title": article_title,
                "article_url": article_url,
                "article_desc": article_desc               
            }


# сохраняем новые новости в новый JSON-файл :
    with open("news_dict.json", "w", encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
#    get_first_news()
    check_news_update()


if __name__ == '__main__':
    main()

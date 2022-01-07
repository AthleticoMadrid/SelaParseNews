# заберём ID-новости:
url = "https://www.securitylab.ru/news/528231.php"

# разобьём ссылку по / и заберём последний элемент:
article_id = url.split("/")[-1]

# обрежем лишние символы, чтобы остался только номер:
article_id = article_id[:-4]
print(article_id)

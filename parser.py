import requests
import json
import os
from bs4 import BeautifulSoup

url = "https://jobs.dou.ua/vacancies/?remote&category=Python&exp=0-1"

headers = {
    "Accept": '''text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9''',
    "User-Agent": '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/98.0.4758.82 Safari/537.36'''
}

resp = requests.get(url, headers=headers).text

soup = BeautifulSoup(resp, "lxml")

vacancies_html = soup.find_all(class_="vacancy")

if os.path.exists(f"{os.getcwd()}/all_vacancies.json"):
    with open("all_vacancies.json", "r", encoding="utf-8") as file:
        all_vacancies = json.load(file)
else:
    all_vacancies = dict()

for vacancy in vacancies_html:
    vacancy_div = vacancy.find(class_="title")
    vacancy_title = vacancy_div.find("a", class_="vt").text
    vacancy_company = vacancy_div.find("a", class_="company").text.replace(u"\xa0", u"")
    vacancy_link = vacancy_div.find("a", class_="vt").get("href")

    if f"{vacancy_title} at {vacancy_company}" not in all_vacancies.keys():
        all_vacancies[f"{vacancy_title} at {vacancy_company}"] = vacancy_link

with open("all_vacancies.json", "w", encoding="utf-8") as file:
    json.dump(all_vacancies, file, indent=4, ensure_ascii=False)

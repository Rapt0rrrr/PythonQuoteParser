import requests
from bs4 import BeautifulSoup
import csv
import os
import time

def parse_quotes():
    # Базовый URL сайта
    base_url = "https://quotes.toscrape.com"
    page = 1
    all_quotes = []

    print("Начинаю парсинг...")

    while True:
        url = f"{base_url}/page/{page}/"
        print(f"Обрабатываю страницу {page}...")

        # Отправляем GET-запрос
        # Обязательно указываем User-Agent, чтобы сайт думал, что мы браузер
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        # Если страницы не существует (закончились), выходим из цикла
        if response.status_code != 200:
            break

        # Передаем HTML-код в BeautifulSoup для разбора
        soup = BeautifulSoup(response.text, "html.parser")

        # Находим все блоки с цитатами на странице
        quotes_divs = soup.find_all("div", class_="quote")

        if not quotes_divs:
            break

        for quote_div in quotes_divs:
            # Достаем текст цитаты
            text = quote_div.find("span", class_="text").get_text(strip=True)
            # Достаем автора
            author = quote_div.find("small", class_="author").get_text(strip=True)
            # Достаем теги (их может быть несколько, объединяем через запятую)
            tags = [tag.get_text(strip=True) for tag in quote_div.find_all("a", class_="tag")]
            tags_str = ", ".join(tags)

            # Сохраняем в виде словаря
            all_quotes.append({
                "text": text,
                "author": author,
                "tags": tags_str
            })

        page += 1
        # Пауза 1 секунда, чтобы не перегружать сервер сайта
        time.sleep(1)

    return all_quotes


def save_to_csv(quotes):
    if not quotes:
        print("Не удалось собрать данные.")
        return

    # Используем os для определения текущей папки, где лежит скрипт
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "quotes.csv")

    print(f"\nНайдено {len(quotes)} цитат. Сохраняю в файл...")

    # Открываем файл для записи (newline='' нужен, чтобы не было пустых строк в Windows)
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        # Указываем заголовки колонок
        fieldnames = ["text", "author", "tags"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()  # Записываем заголовки
        writer.writerows(quotes)  # Записываем все данные

    print(f"✅ Готово! Данные сохранены в файл: {file_path}")


if __name__ == "__main__":
    data = parse_quotes()
    save_to_csv(data)
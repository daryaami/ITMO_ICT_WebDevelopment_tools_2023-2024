# parse_threading.py
import threading
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

def init_db():
    conn = sqlite3.connect("pages.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    title TEXT
                 )''')
    conn.commit()
    conn.close()

def parse_and_save(url):
    try:
        response = requests.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
    except Exception as e:
        title = f"Error: {str(e)}"
    # Сохраняем результат в БД (открываем отдельное соединение)
    conn = sqlite3.connect("pages.db")
    c = conn.cursor()
    c.execute("INSERT INTO pages (url, title) VALUES (?, ?)", (url, title))
    conn.commit()
    conn.close()
    print(f"Thread: {url} -> {title}")

def main():
    init_db()
    urls = [
        "http://example.com",
        "https://www.python.org",
        "https://www.wikipedia.org",
        # Можно добавить дополнительные URL
    ]
    threads = []
    for url in urls:
        t = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"Threading: Time taken: {end - start:.2f} seconds")
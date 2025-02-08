from icrawler.builtin import GoogleImageCrawler
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(script_directory, "images")

def download_images(query, limit=10):
    crawler = GoogleImageCrawler(storage={'root_dir': directory_path})
    crawler.crawl(keyword=query, max_num=limit)

# Przykład użycia
download_images("Opieńka miodowa", limit=1000)

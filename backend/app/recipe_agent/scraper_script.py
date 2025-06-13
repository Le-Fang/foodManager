from recipe_agent import RecipeAgent
from scraper import DocumentScraper
import requests
from bs4 import BeautifulSoup
from pathlib import Path

'''
def scrape_urls(url):
    script_dir = Path(__file__).parent
    file_path = script_dir / "links.txt"
    with open(file_path, 'a') as f:
        scraper = DocumentScraper()
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        list_element = soup.find(id="mntl-taxonomysc-article-list_1-0")
        if list_element:
            items = list_element.find_all('a')
            for item in items:
                if 'href' in item.attrs:
                    href = item['href']
                    f.write(href + '\n')

urls = ["https://www.seriouseats.com/main-recipes-5117839",
        "https://www.seriouseats.com/recipes-by-course-5117906",
        "https://www.seriouseats.com/recipes-by-world-cuisine-5117277",
        "https://www.seriouseats.com/recipes-by-method-5117399",
        "https://www.seriouseats.com/recipes-by-diet-5117779",
        "https://www.seriouseats.com/recipes-by-ingredient-recipes-5117749"
        ]

for url in urls:
    scrape_urls(url)
'''


script_dir = Path(__file__).parent
with open(script_dir / "links.txt", 'r') as f:
    urls = f.readlines()

urls = [url.strip() for url in urls if url.strip()]
scraper = DocumentScraper()
for i in range(1, len(urls)+1):
    url = urls[i-1]
    print(f"Scraping {url}...")
    scraper.scrape(url)
    if i % 10 == 0:
        if i == 10:
            scraper.store_to_index()
        else:
            scraper.append_to_index()
scraper.append_to_index()



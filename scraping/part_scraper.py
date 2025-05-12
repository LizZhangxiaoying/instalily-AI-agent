# scraping/part_scraper.py

import requests
from bs4 import BeautifulSoup
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

HEADERS = {"User-Agent": "Mozilla/5.0"}


BASE_URL = "https://www.partselect.com"
CATEGORY_URL = "https://www.partselect.com/Models/GSS25SGMDBS/"

def get_part_links(category_url):
    res = requests.get(category_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []

    for a in soup.select("a.model-part-link"):
        href = a.get("href")
        if href and href.startswith("/"):
            links.append(BASE_URL + href)

    print(f"✅ Found {len(links)} part links.")
    print(links)
    return links[:10]

def get_part_info(part_url):
    res = requests.get(part_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.find("h1").get_text(strip=True)

    desc_tag = soup.find("div", class_="product-description")
    description = desc_tag.get_text(strip=True) if desc_tag else "No description"

    install_tag = soup.find("div", class_="how-to-install")
    installation = install_tag.get_text(strip=True) if install_tag else "No installation info"

    troubleshoot_tag = soup.find("div", class_="troubleshooting")
    troubleshooting = troubleshoot_tag.get_text(strip=True) if troubleshoot_tag else "No troubleshooting info"

    model_tags = soup.select("ul.compatible-models li")
    models = [tag.text.strip() for tag in model_tags] if model_tags else []

    return {
        "title": title,
        "description": description,
        "installation": installation,
        "troubleshooting": troubleshooting,
        "compatible_models": models,
        "url": part_url
        }


def get_part_links_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 不弹出浏览器窗口
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    driver.implicitly_wait(5)

    all_links = set()

    while True:
        # wait and get all the parts information
        elements = driver.find_elements(By.CLASS_NAME, "model-part-link")
        for e in elements:
            href = e.get_attribute("href")
            if href:
                full_url = BASE_URL + href if href.startswith("/") else href
                all_links.add(full_url)

        # break if there is no next
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next >")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(1)
        except:
            break

    driver.quit()
    print(f"✅ Total part links collected: {len(all_links)}")
    return list(all_links)



def main():
    part_links = get_part_links_selenium(CATEGORY_URL)
    parts = []

    for link in part_links:
        print(f"Scraping: {link}")
        info = get_part_info(link)
        parts.append(info)
        time.sleep(1)

    output_path = os.path.join(os.path.dirname(__file__), "data", "refrigerator_parts.json")
    with open(output_path, "w") as f:
        json.dump(parts, f, indent=2)

if __name__ == "__main__":
    main()

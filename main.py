from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import re
import csv
import os
import requests
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless=new")
chrome_options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

folder_path = "conan"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(os.path.join(folder_path, "chapter_links.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["chapter", "link"])

def get_chapter_link():
    driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    base_url = f"https://kenhsinhvien.vn/f/conan-reading-room.510/" 
    driver.get(base_url)
    time.sleep(2)
    pagination = driver.find_element(By.CLASS_NAME, "pageNavSimple-el").text
    match = re.search(r'/ (\d+)', pagination)
    print(match)
    if match:
        max_pages = match.group(1)
    driver.quit()

    for i in range(1, int(max_pages) + 1):
        driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
        url = f"https://kenhsinhvien.vn/f/conan-reading-room.510/page-{i}" 
        driver.get(url)
        time.sleep(5)
        list_chap = driver.find_element(By.CLASS_NAME, "structItemContainer-group")
        chaps = list_chap.find_elements(By.CLASS_NAME, "structItem--thread")
        for chap in chaps:
            title = chap.find_element(By.CLASS_NAME, "structItem-title").text
            if re.search(r'CONAN chap', title):
                print("=======================================")
                print(title)
                with open("conan/chapter_links.csv", "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([title, chap.find_element(By.CLASS_NAME, "structItem-title").find_element(By.TAG_NAME, "a").get_attribute("href")])
        driver.quit()

def get_image(url, chapter_name):
    chapter_name = "conan-1072"
    folder_path = f"conan/{chapter_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    driver.get(url)
    time.sleep(2)
    wrapper = driver.find_element(By.CLASS_NAME, "bbWrapper")
    images = wrapper.find_elements(By.CLASS_NAME, "bbImage")
    for index, image in enumerate(images, start=1):
        img_src = image.get_attribute("src")
        img_data = requests.get(img_src).content
        img_path = os.path.join(folder_path, f"{index}.jpg")

        with open(img_path, "wb") as img_file:
            img_file.write(img_data)

        print(f"Image {index} saved at {img_path}")

get_chapter_link()
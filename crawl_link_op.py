import os
import csv
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

folder_path = "onepiece"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(os.path.join(folder_path, "chapter_links.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["chapter", "link"])

def get_chapter_link():
    for i in range(1, 1104):
        title = f"One Piece chap {i}"
        href = f"https://truyenqqvn.com/truyen-tranh/one-piece-128-chap-{i}.html"
        with open(f"{folder_path}/chapter_links.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([title, href])


get_chapter_link()



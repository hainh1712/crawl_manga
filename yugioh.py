import os
import csv
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import boto3
from botocore.exceptions import NoCredentialsError
# from dotenv import load_dotenv

# load_dotenv('.env')

# s3 = boto3.client("s3", aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name=os.environ['AWS_REGION'])
# def upload_to_aws(local_file, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
#     try:
#         s3.upload_file(local_file, os.environ['AWS_BUCKET_NAME'], s3_file, ExtraArgs={
#             'ContentType': 'jpg',
#         })
#         print(f"Upload successful: {s3_file}")
#         return True
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

folder_path = "yugioh"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

with open(os.path.join(folder_path, "chapter_links.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["chapter", "link"])

def get_chapter_link():
    driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    base_url = f"https://blogtruyenvn.com/16751/yugi-oh-full-color-edition/" 
    driver.get(base_url)
    time.sleep(2)
    list_chapter = driver.find_element(By.CLASS_NAME, "list-wrap")
    chapters = list_chapter.find_elements(By.TAG_NAME, "p")
    for chapter in chapters:
        href = chapter.find_element(By.TAG_NAME, "a").get_attribute("href")
        chapter_name = chapter.find_element(By.TAG_NAME, "a").text
        with open(os.path.join(folder_path, "chapter_links.csv"), "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([chapter_name, href])
get_chapter_link()
# def get_image(url, chapter_name):
#     pattern = r"\d+"
#     result = re.search(pattern, chapter_name)
#     chapter = result.group()
    
#     folder_path = f"conan/{chapter_name}"
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)
#     driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
#     driver.get(url)
#     time.sleep(2)
#     wrapper = driver.find_element(By.CLASS_NAME, "bbWrapper")
#     images = wrapper.find_elements(By.CLASS_NAME, "bbImage")
#     for index, image in enumerate(images, start=1):
#         img_src = image.get_attribute("src")
#         img_data = requests.get(img_src).content
#         img_path = os.path.join(folder_path, f"{index}.jpg")

#         with open(img_path, "wb") as img_file:
#             img_file.write(img_data)
            
#         s3_file_path = f"conan/chap_{chapter}/{index}.jpg"
#         upload_to_aws(img_path, s3_file_path)
#         # print(f"Image {index} saved at {img_path}")
#         print(f"Image {index} uploaded to S3 at {s3_file_path}")


# def main():
#     with open(os.path.join(folder_path, "chapter_link.csv"), "r", newline="", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(reader)
#         for row in reader:
#             get_image(row[1], row[0])

# main()


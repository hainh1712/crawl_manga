from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
import re
import csv
import os
from selenium.webdriver.common.by import By
import pyautogui
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless=new")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

folder_path = "D:\\Personal\\crawl_manga\\onepiece"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def get_image(url, chapter_name):
    driver = webdriver.Chrome(service=ChromeService("./chromedriver.exe"), options=chrome_options)
    driver.get(url)
    time.sleep(2)
    wrapper = driver.find_element(By.CLASS_NAME, "chapter_content")
    images = wrapper.find_elements(By.CLASS_NAME, "page-chapter")
    path = folder_path + f"\\{chapter_name}"
    if not os.path.exists(path):
        os.makedirs(path)
    for index, image in enumerate(images, start=1):
        img_path = os.path.join(path, f"{index}.jpg")
        img = image.find_element(By.TAG_NAME, "img")
        img_src = img.get_attribute("src")
        driver.execute_script("window.open('" + img_src + "', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(2)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)
        pyautogui.write(img_path)
        pyautogui.press('enter')    
        print(f"Image {index} saved")
        driver.close()  
        driver.switch_to.window(driver.window_handles[0])

    driver.quit()

def main():
    csv_path = folder_path + f"\\chapter_links_test.csv"
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            chapter_name, link = row
            get_image(link, chapter_name)

main()





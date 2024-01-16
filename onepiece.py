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

# with open(os.path.join(folder_path, "chapter_links.csv"), "w", newline="", encoding="utf-8") as f:
#     writer = csv.writer(f)
#     writer.writerow(["chapter", "link"])

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
    # folder_path = f"onepiece/{chapter_name}"
    # if not os.path.exists(folder_path):
    #     os.makedirs(folder_path)
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

get_image("https://truyenqqvn.com/truyen-tranh/one-piece-128-chap-1103.html", "Onepiece chap 1103")
# def main():
#     with open(os.path.join(folder_path, "chapter_links.csv"), "r", newline="", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(reader)
#         for row in reader:
#             get_image(row[1], row[0])

# main()




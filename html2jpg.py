import os
from playwright.sync_api import sync_playwright

def run():

    file_path = os.path.abspath("calendar.html")  # 确保文件名拼写正确
    url = "file://" + file_path

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.screenshot(path="RGBoutput.jpg", full_page=True)
        browser.close()
    print("Screenshot saved as RGBoutput.jpg")
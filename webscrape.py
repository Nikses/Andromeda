# functions to scrape the website for the latest bill
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import time


def scrape_for_updates():
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.govtrack.us/congress/bills/browse?status=passed#sort=-introduced_date&current_status[]=28'
    driver.get(url)
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []

    time.sleep(2)  # Wait for 2 seconds to load the page
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Select the latest bill
    rows = soup.find_all('div', class_='row')
    row = str(rows[3].find('a'))

    # Splitting to get the url and the title part
    href = row.split('href="')[1].split('"')[0]
    title = row.split('title="')[1].split('"')[0]

    return title, href


def scrape_bill_text_save_txt(href, title):
    url = "https://www.govtrack.us" + href + "/text"

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the web page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    bill_text_container = soup.find_all('p')  # Assuming the bill text is in <p> tags

    log_title = title.split(' ')[1][:-1]
    with open(f'scraped_logs/{log_title}.txt', 'w') as file:
        file.write(title + '\n')  # Write the bill's title
        start_saving = False  # Flag to not save text unless it starts with "The text of the bill below"
        for paragraph in bill_text_container:
            text = paragraph.get_text()
            if "The text of the bill below" in text:
                start_saving = True  # Update the flag to start saving text
            elif "Vice President of the United States and President of the Senate." in text:
                start_saving = False  # Update the flag to stop saving text after bill finished
            if start_saving:
                file.write(text + '\n')

    file.close()

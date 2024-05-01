# functions to scrape the website for the latest bill
import requests
from bs4 import BeautifulSoup


url = 'https://www.govtrack.us/congress/bills/browse?status=passed#sort=-introduced_date&current_status[]=28'


def scrape_bill_text_save_txt():
    url = "https://www.govtrack.us/congress/bills/118/hr7888/text"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the web page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    bill_text_container = soup.find_all('p')  # Assuming the bill text is in <p> tags

    with open('test1.txt', 'w') as file:
        start_saving = False  # Flag to not save text unless it starts with "The text of the bill below"
        for paragraph in bill_text_container:
            text = paragraph.get_text()
            if "The text of the bill below" in text:
                start_saving = True  # Update the flag to start saving text
            elif "Vice President of the United States and President of the Senate." in text:
                start_saving = False  # Update the flag to stop saving text after bill finished
            if start_saving:
                file.write(text + '\n')


scrape_bill_text_save_txt()

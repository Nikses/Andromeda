# functions to scrape the website for the latest bill
import requests
from bs4 import BeautifulSoup
from docx import Document


url = 'https://www.govtrack.us/congress/bills/browse?status=passed#sort=-introduced_date&current_status[]=28'

def scrape_bill_text_save_docx():
    url = "https://www.govtrack.us/congress/bills/118/hr7888/text"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the web page")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    bill_text_container = soup.find_all('p')  # Assuming the bill text is in <p> tags, adjust as necessary

    # Create a new Document
    doc = Document()
    start_saving = False  # Flag to start saving text
    for paragraph in bill_text_container:
        text = paragraph.get_text()
        if "The text of the bill below" in text:
            start_saving = True  # Update the flag to start saving text
        if start_saving:
            doc.add_paragraph(text)  # Add paragraph to the document only after the starting point

    # Save the document to the specified path on your Google Drive
    doc.save('/content/drive/MyDrive/case_study/Legalfin.docx')  # Adjust path as needed

scrape_bill_text_save_docx()
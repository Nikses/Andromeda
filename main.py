#  This is the main function for the program, import the required modules from other files
from webscrape import scrape_for_updates, scrape_bill_text_save_txt, prepend_line
from agent import explain


def check_logs():
    """Check if there is a bill that we did not do before"""
    with open('logs', 'r', encoding='latin-1') as file:
        last_title = file.readline()
        clean_line = last_title.strip()

    file.close()

    title, url = scrape_for_updates()
    if clean_line == title:
        return False
    else:
        return [title, url]


def main():
    temp = check_logs()

    if temp:
        title, url = temp[0], temp[1]
        scrape_bill_text_save_txt(url, title)
        explain(filename='scraped_logs/' + title.split(' ')[1][:-1] + '.txt')
        prepend_line('logs', title)
    else:
        print('No new bill to explain')


main()

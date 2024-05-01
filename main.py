#main function for the program, import the required modules from other files
from webscrape import scrape_for_updates, scrape_bill_text_save_txt
from agent import explain


def prepend_line(file_name, line_to_prepend):
    """ Prepend a line to the beginning of a file. """
    # Read the existing content from the file
    with open(file_name, 'r', encoding='latin-1') as file:
        content = file.readlines()

    # Open the file in write mode and write the new line at the top with the original content below
    with open(file_name, 'w', encoding='latin-1') as file:
        file.write(line_to_prepend + '\n')
        file.writelines(content)


def check_logs():
    """Check if there is a bill that we did not do before"""
    with open('logs', 'r', encoding='latin-1') as file:
        last_title = file.readline()

    title, url = scrape_for_updates()
    if last_title == title:
        print(1)
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
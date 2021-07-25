import re
import urllib.request
import sys
from pathlib import Path
import os


from bs4 import BeautifulSoup

url = "https://www.nature.com/nature/articles"

article_list = []
h3_tags_list = []
article_type_list = []
article_url_list = []
article_p_list = []
article_tuple = [()]

h3_tags = []
article_type_tags = []
article_url_tags = []

article_list1 = []

article_p_tags = []

j = 0
z = 0

num_pages = int(input())

article_type = str(input())

for i in range(num_pages):
    article_list.clear()
    url = "https://www.nature.com/nature/articles"
    page_number = i + 1
    page = urllib.request.urlopen(url + "?searchType=journalSearch&sort=PubDate&page=" + str(page_number))
    soup = BeautifulSoup(page, "html.parser")
    url3 = "https://www.nature.com/nature/articles" + "?searchType=journalSearch&sort=PubDate&page=" + str(page_number)

    # Create directory with page number
    Path("Page_" + str(page_number)).mkdir(parents=True, exist_ok=True)

    # print("Currently getting articles of", url + "?searchType=journalSearch&sort=PubDate&page=" + str(page_number))

    # Move into the directory
    Path.cwd()
    os.chdir("Page_" + str(page_number))
    Path.cwd()

    # Get the h3 tags from the page with clas "c-card__title"
    # And append them to a list called h3_tags_list
    # html = urllib.request.urlopen(url).read()
    # soup = BeautifulSoup(html, 'html.parser')
    h3_tags_list.clear()
    h3_tags = soup.find_all("h3", class_="c-card__title")
    for tag in h3_tags:
        h3_tags_list.append(tag.text.strip("\n"))

    # Get the text from class c-meta__type
    article_type_list.clear()
    article_type_tags = soup.find_all("span", class_="c-meta__type")
    for tag in article_type_tags:
        article_type_list.append(tag.text)

    # Get the url from class c-card__link u-link-inherit
    article_url_list.clear()
    article_url_tags = soup.find_all("a", class_="c-card__link u-link-inherit")
    for url3 in article_url_tags:
        article_url_list.append(url3.get("href"))

    # Create a list of tuples with h3_tags_list and article_type_tags
    article_tuple = zip(h3_tags_list, article_type_list, article_url_list)

    # Extract tuple that contains 'News'
    for article in article_tuple:
        if article[1] == article_type:
            article_list.append(article)

    # Get all p tags from the page with url
    # And append them to a list called article_p_list
    article_p_list.clear()
    for y in range(len(article_list)):
        j = 0
        article_p_tags.clear()
        article_p_list.clear()
        url2 = "https://www.nature.com" + article_list[y][2]
        html2 = urllib.request.urlopen(url2).read()
        soup2 = BeautifulSoup(html2, 'html.parser')
        # article_p_tags = soup2.find_all("p")
        # article_p_tags = soup2.find('div', {'class': 'c-article-body'})
        if soup2.find('div', {'class': 'article-item__body'}):
            body = soup2.find('div', {'class': 'article-item__body'})
        elif soup2.find('div', {'class': 'c-article-body u-clearfix'}):
            body = soup2.find('div', {'class': 'c-article-body u-clearfix'})
        # for tag in article_p_tags:
        #     if 4 < j < 14 and j != 11:
        #         article_p_list.append(tag.text)
        #     j += 1

        # Join list of strings inside article_p_list
        # article_text = "".join(article_p_list)

        # Create a file name that replaces ':' and '?' and '-' with ''
        file_name = re.sub(r'[:?\-]', '', article_list[y][0])
        # Create a file name that replaces all blank spaces with '_'
        file_name = re.sub(r'\s+', '_', file_name + ".txt")
        # Open file_name in write binary mode
        file = open(file_name, "wb")
        file.write(body.text.encode())
        file.close()
    
    # print("Finished saving articles for", "Page_" + str(page_number))
    
    # Go back to the parent directory
    os.chdir("..")
    Path.cwd()

    # Make a list of the with the elements in position 0 of article_list
    # And append them to a list called article_list1
    for article in article_list:
        article_list1.append(article[0])

print("Saved articles:", article_list1)

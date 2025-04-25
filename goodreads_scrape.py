import requests
from bs4 import BeautifulSoup
import json

def fetch_book_details(search_by):


    search_url = f"https://www.goodreads.com/search?utf8=%E2%9C%93&q={search_by}&search_type=books"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }

    response = requests.get(search_url, headers = headers, stream = True)

    soup = BeautifulSoup(response.text, "html.parser")
    if search_by.isnumeric():
        script_tag = soup.find('script', {'type': 'application/ld+json'})
        if script_tag:
            json_content = json.loads(script_tag.string)
            title = json_content.get('name')
            pages = json_content.get('numberOfPages')
            isbn = json_content.get('isbn')
            author = json_content.get('author')[0]['name']
            picture = json_content.get('image')
            return[{'title': title, 'pages': pages, 'author' : author, 'isbn' : isbn, 'picture': picture}]

    else:
        trs = soup.find_all('tr', {'itemscope': True, 'itemtype': 'http://schema.org/Book'})
        book_urls = [tr.find('a', class_= 'bookTitle')['href'] for tr in trs]

        base_url = "https://goodreads.com"
        books_details = []
        for url in book_urls:
            single_book_response = requests.get(base_url + url, headers = headers, stream = True)
            soup = BeautifulSoup(single_book_response.text, "html.parser")
            script_tag = soup.find('script', {'type': 'application/ld+json'})
            if script_tag:
                json_content = json.loads(script_tag.string)
                title_series = json_content.get('name')
                if "(" in title_series:
                    title_series = title_series.split(' (')
                    title = title_series[0]
                    series = title_series[1][:-1]
                    series_number = series.split('#')[-1]
                    series_name = series.split('#')[0][:-2]
                    book_details = {'series': series_number, 'title': title, 'series_name': series_name}
                else:
                    title = title_series
                    series_number = 'standalone'
                    series_name = 'N/A'
                    book_details = {'title': title, 'series': series_number, 'series_name': series_name}
                pages = json_content.get('numberOfPages')
                isbn = json_content.get('isbn')
                author = json_content.get('author')[0]['name']
                picture = json_content.get('image')
                book_details.update({'pages': pages, 'author' : author, 'isbn' : isbn, 'picture': picture, 'series': series_number, 'series_name': series_name})
                books_details.append(book_details)
        return books_details

import requests
import time
from bs4 import BeautifulSoup as bs


class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

def main():
    url = "https://quotes.toscrape.com"
    r = requests.get(url)
    soup = bs(r.content, "html.parser")
    
    #scrape_quotes(soup)
    
    quotes =[]
    while True: 
        time.sleep(1)
        relative_url = get_next_url(soup)
        if relative_url is None:
            break
        next_page = url + relative_url
        
        r = requests.get(next_page)
        soup = bs(r.content, "html.parser")
        quotes.extend(scrape_quotes(soup))
    
    get_shortest_and_longest(quotes)
    get_top_tags(quotes)
    get_authors_with_multiple_quotes(quotes)
    return

def get_authors_with_multiple_quotes(quotes):
    author_count = {}
    for quote in quotes:
        author_count[quote.author] = author_count.get(quote.author, 0) + 1

    authors_with_multiple_quotes = [(author, count) for author, count in author_count.items() if count > 1]
    sorted_authors = sorted(authors_with_multiple_quotes, key=lambda x: x[1], reverse=True)

    print("Authors with multiple quotes:")
    for author, count in sorted_authors:
        print(f"{author}: {count} quotes")

    return



def get_top_tags(quotes):
    tag_count = {}
    for quote in quotes:
        for tag in quote.tags:
            tag_count[tag] = tag_count.get(tag, 0) + 1

    sorted_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)

    print("Top 10 tags:")
    for tag, count in sorted_tags[:10]:
        print(f"{tag}: {count}")

    return

def get_shortest_and_longest(quotes):

    longest = 0
    shortest = 100000
    longest_quote = ""
    shortest_quote = ""

    for quote in quotes:
        if len(quote.text) > longest:
            longest = len(quote.text)
            longest_quote = quote.text
        
        if len(quote.text) < shortest:
            shortest = len(quote.text)
            shortest_quote = quote.text
    
    print(longest_quote, longest)
    print(shortest_quote, shortest)
    return
    


def get_next_url(soup: bs):
    list_item = soup.find("li", {"class":"next"})
    if list_item is None:
        return None
    anchor = list_item.find("a")
    url = anchor["href"]

    return url

def scrape_quotes(soup: bs):
    quotes = soup.find_all("div", {"class": "quote"})

    quotes_list = []



    for quote in quotes:
        text = quote.find("span", {"class": "text"}).get_text(strip=True)
        print(text)
        author = quote.find("small", {"class":"author"}).get_text(strip=True)
        print(author)
        
        tags = quote.find_all("a", {"class":"tag"})
        tags_text = []
        for tag in tags:
            tags_text.append(tag.get_text(strip=True))
        print(tags_text)

        quotes_list.append(Quote(text, author, tags_text))

        

    return quotes_list



if __name__ == "__main__":
    main()
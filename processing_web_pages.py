#processing web pages

import urllib.request
import bs4
import re
import queue

r = re.compile("http")

class Crawl:
    def __init__(self, start_page, distance, action):
        self.start_page = start_page
        self.distance = distance
        self.action = action
        self.pages = queue.Queue()
        self.seen_pages = set()
        self.current = 0

    def __iter__(self):
        self.pages.put((self.start_page, 0))
        return self

    def search(self):
        page = self.pages.get()
        cur_dist = page[1]
        page = page[0]
        if page in self.seen_pages:
            return
        self.seen_pages.add(page)
        try:
            p = urllib.request.urlopen(page)
            soup = bs4.BeautifulSoup(p, 'html.parser')
        except:
            return
        if cur_dist < self.distance:
            for packed_link in soup.find_all('a', attrs={'href': r}):
                link = packed_link.get('href')
                self.pages.put((link, cur_dist+1))
        return page, self.action(page)

    def __next__(self):
        while True:
            if self.pages.empty():
                raise StopIteration
            p = self.search()
            if p is not None:
                return p


def find_python(page):
    page = urllib.request.urlopen(page)
    soup = bs4.BeautifulSoup(page, 'html.parser')
    sentences = re.findall("([^.\n]*?[Pp]ython[^.\n]*\.)", soup.get_text())
    return sentences


zdania = list(Crawl("https://www.ii.uni.wroc.pl/~marcinm/dyd/python", 1, find_python))
for zdanie in zdania:
    print(zdanie)

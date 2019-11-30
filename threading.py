import urllib.request
import bs4
import re
import threading

r = re.compile("http")

class Crawl:
    def __init__(self, start_page, distance, action):
        self.start_page = start_page
        self.distance = distance
        self.action = action
        self.pages = []
        self.seen_pages = set()
        self.current = 0
        self.lock = threading.Lock()

    def __iter__(self):
        self.search(self.start_page, 0)
        return self

    def search(self, page, cur_dist):
        self.lock.acquire()
        if page in self.seen_pages:
            self.lock.release()
            return
        self.seen_pages.add(page)
        self.lock.release()
        try:
            p = urllib.request.urlopen(page)
            soup = bs4.BeautifulSoup(p, 'html.parser')
            self.lock.acquire()
            self.pages.append(page)
            self.lock.release()
        except:
            return
        threads = []
        if cur_dist < self.distance:
            for packed_link in soup.find_all('a', attrs={'href': r}):
                link = packed_link.get('href')
                threads.append(threading.Thread(target=self.search, args=(link, cur_dist+1)))
                threads[-1].start()
        for t in threads:
            t.join()
        return

    def __next__(self):
        if self.current >= len(self.pages):
            raise StopIteration
        self.current += 1
        return self.pages[self.current-1], self.action(self.pages[self.current-1])


def find_python(page):
    page = urllib.request.urlopen(page)
    soup = bs4.BeautifulSoup(page, 'html.parser')
    sentences = re.findall("([^.\n]*?[Pp]ython[^.\n]*\.)", soup.get_text())
    return sentences


zdania = list(Crawl("https://www.ii.uni.wroc.pl/~marcinm/dyd/python", 1, find_python))
for zdanie in zdania:
    print(zdanie)
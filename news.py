from requests import session
import urllib.parse
from requests_html import HTMLSession
import pandas as pd

class GoogleSearchNews:
    def paginate(self, url, previous_url = None):
        if url == previous_url: return
        session = HTMLSession()
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        resp = session.get(url, headers = header)
        #print(resp)
        yield resp
        next_page = resp.html.find("a#pnnext")
        #print(next_page)
        if next_page is None: return
        try:
            next_page_url = urllib.parse.urljoin("https://www.google.com/", next_page[0].attrs["href"])
            #print(next_page_url)
            yield from self.paginate(next_page_url, url)   
        except: pass

    def scrape_articles(self):
        search = "Religions"
        pages = self.paginate(f"https://www.google.com/search?q={search}&sxsrf=ALiCzsbFF20mR8EgVYoIo_i-jOglEn3mQQ:1658986430787&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjkp5OH7pr5AhWzv2MGHdsqCV4Q_AUoAXoECAIQAw&biw=1536&bih=722&dpr=1.25")
        NewsList = []
        for page in pages:
            num_page = page.html.find("td.YyVfkd")[0].text
            #print(num_page)
            print(f"Scraping page number: {int(num_page)}\n")
            articles = page.html.find("a.WlydOe")
            #print(articles)
            for article in articles:
                title = article.find("div.mCBkyc")[0].text
                # link = article.attrs['href']
                # source = article.find("div.CEMjEf")[0].text
                # date_published = article.find("div.ZE0LJd")[0].text
                # if len(article.find("div.GI74Re")) >= 1:
                #     description_ = article.find("div.GI74Re")[0].text
                #     #print(description_) 
                # else:
                #     description_ = "NA"
                    #print("NA")
                #print(title, link)
                NewsList.append({
                    "Title":title,
                    # "Link": link,
                    # "Description": description_,
                    # "Source": source,
                    # "Date Published": date_published
                })
        #print(NewsList)  
        return NewsList

    def output_data(self, NewsList):
        data_news = pd.DataFrame(NewsList)
        data_news.to_csv("Google_News.csv", index = False)
        print("Saved to csv")         
                

news = GoogleSearchNews()
data = news.scrape_articles()
news.output_data(data)
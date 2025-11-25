import pandas as pd
from pgconn.db_conn import engine                          
from websc.webconn import BaseScraper


class FlipkartScraper(BaseScraper):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)

        #  Extract data
        names = [n.get_text(strip=True) for n in self.soup.find_all("div", class_="KzDlHZ")]
        prices = [p.get_text(strip=True) for p in self.soup.find_all("div", class_="Nx9bqj _4b5DiR")]
        # storage = [r.get_text(strip=True) for r in self.soup.find_all("div", class_="_Jigdf")]
        rating = [r.get_text(strip=True) for r in self.soup.find_all("div", class_="XQDdHH")]
        
        min_len = min(len(names), len(prices),len(rating))
        names, prices, rating= names[:min_len], prices[:min_len], rating[:min_len]

        #  Store in DataFrame
        df_filpkard= pd.DataFrame({
            "Product Name": names,
            "Price": prices,
            "rating":rating
        })

        df_filpkard.to_csv('flipkard.csv')
        print("\ndata saves to flipkard.csv file is done")
        print(df_filpkard.head(10))

class AmazonScraper(BaseScraper):
    def __init__(self, url, headers=None):
        super().__init__(url, headers)
        
        names = [n.get_text(strip=True) for n in self.soup.find_all("h2", class_="a-size-medium a-spacing-none a-color-base a-text-normal")]
        prices = [p.get_text(strip=True) for p in self.soup.find_all("span", class_="a-price-whole")]
        ratings = [r.get_text(strip=True) for r in self.soup.find_all("span", class_="a-icon-alt")]
            
        # Equalize lengths
        min_len = min(len(names), len(prices), len(ratings))
        names, prices, ratings = names[:min_len], prices[:min_len], ratings[:min_len]

        # Store in DataFrame
        df_amazon = pd.DataFrame({
            
            "Product Name": names,
            "Price (₹)": prices,
            "Rating": ratings
        })
        df_amazon.to_csv('amazom.csv')
        print("\ndata saves to amazom.csv file is done")
        print(df_amazon.head(10))



#  Run the Scraper





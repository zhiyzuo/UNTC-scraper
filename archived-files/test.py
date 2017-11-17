from SeleniumScraper import Scraper

if __name__ == '__main__':
    parser = Scraper()
    parser.set_year('01/01/1945', '01/01/1951')
    parser.search()
    print parser.df.head()
    print parser.df.shape
    #parser.close()



import sys
from UNTCScraper import UNTCScraper

if __name__ == '__main__':
    endpage = int(sys.argv[1])
    output_dir = sys.argv[2]

    parser = UNTCScraper(endpage)
    parser.scrape()
    parser.df.to_csv(output_dir, index=False, encoding='utf8')

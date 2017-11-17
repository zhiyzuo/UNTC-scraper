## UNTC-scraper
Scrape United Nations Treaty Collections: https://treaties.un.org/Pages/AdvanceSearch.aspx?tab=UNTS&clang=_en

#### Required packages:
Run the following to ensure that you have the packages to run the script.
```bash
pip install -r requirements.txt
```

#### Example usage:
```bash 
python main.py 10 output.csv
```

The above command line will scrape ___10 pages___ and save the output to ___output.csv___ in the current directory.

#### Output file format:
The output csv files have the following columns:
`title, link, reg_number, reg_date, tr_type, date_conclusion, vol`

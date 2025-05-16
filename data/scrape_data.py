from autoscraper import AutoScraper
import pandas as pd
import numpy as np
import pdfplumber
import pickle
import re

def find_event(event_list, query):
    try:
        return event_list.index(query)
    except ValueError:
        return False

#### First, we need to find the list of all countries competing.
noc_countries = set()

with pdfplumber.open("List-of-National-Olympic-Committees-in-IOC-Protocol-Order.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        matches = re.findall(r'\b[A-Z]{3}\b', text)
        noc_countries|=set(matches)

# remove non-country entries, add in Yugoslavia and USSR for interest.
noc_countries -= {"NOC","IOC","IOA","IOP","EOR"}
noc_countries |= {"URS","YUG"}
noc_countries = sorted(list(noc_countries))


### events in summer and winter to be recorded

summer_years = ['2','3','5','6','7','8','9','10','11','12','13','14','15','16','17','18',
                '19','20','21','22','23','24','25','26','53','54','59','61']

winter_years = ['29','30','31','32','33','34','35','36','37','38','39','40','41','42','43',
                '44','45','46','47','49','57','58','60','62']

summer_events = ['BK3','ARC','GAR','SWA','ATH','BDM','BBL','BKB','VBV','BOX','CSL','CSP',
                 'BMF','BMX','MTB','CRD','CTR','DIV','FEN','FBL','GLF','HBL','HOC','JUD',
                 'KTE','OWS','MPN','ROW','RU7','SAL','SKB','CLB','SRF','SWIM','TTE','TKW',
                 'TEN','GTR','TRI','VOL','WPO','WLF','WRE']

winter_events = ['ALP','BTH','BOB','CCS','CUR','FSK','FRS','IHO','LUG','NCB','STK','SKN',
                 'SJP','SBD','SSK']




### To use autoscaper, we "calibrate" it with some known values to get the scraping rules
url = 'http://www.olympedia.org/editions/53/sports/ATH'

L = ["100 metres, Men","JAM","TTO","USA"]
scraper = AutoScraper()
result_countries = scraper.build(url, L)
scraper.get_result_similar(url,grouped=True)

namerule = 'rule_kqkt'
Grule = 'rule_4frv'
Srule = 'rule_00zy'
Brule = 'rule_dbcc'

L = ["100 metres, Men","JAM","TTO","USA"]
scraper = AutoScraper()
result_countries = scraper.build(url, L)
SR = scraper.get_result_similar(url,grouped=True)

N1 = ['100 metres, Men','200 metres, Men']
N2 = ['JAM','JAM']
N3 = ['TTO','USA']
N4 = ['USA','USA']
for i in SR:
    if SR[i][:2]==N1 and len(SR[i])==47:
        namerule = i
        break
for i in SR:
    if SR[i][:2]==N2 and len(SR[i])==47:
        Grule = i
        break
for i in SR:
    if SR[i][:2]==N3 and len(SR[i])==47:
        Srule = i
        break
for i in SR:
    if SR[i][:2]==N4 and len(SR[i])==47:
        Brule = i
        break
        

url = 'http://www.olympedia.org/editions/6'
L = ["1912 Summer Olympics"]
scraper_year = AutoScraper()
result_countries = scraper_year.build(url, L)
SYR = scraper_year.get_result_similar(url,grouped=True)
year_rule = list(SYR.keys())[0]




summer_years_numeric = []
for y in summer_years:
    SYR = scraper_year.get_result_similar(f"http://www.olympedia.org/editions/{y}",grouped=True)
    summer_years_numeric.append(int(SYR[year_rule][0][:4]))

winter_years_numeric = []
for y in winter_years:
    SYR = scraper_year.get_result_similar(f"http://www.olympedia.org/editions/{y}",grouped=True)
    winter_years_numeric.append(int(SYR[year_rule][0][:4]))




summer_men_g = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
summer_men_s = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
summer_men_b = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
summer_women_g = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
summer_women_s = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
summer_women_b = pd.DataFrame(0, index=summer_years_numeric, columns=noc_countries)
winter_men_g = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)
winter_men_s = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)
winter_men_b = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)
winter_women_g = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)
winter_women_s = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)
winter_women_b = pd.DataFrame(0, index=winter_years_numeric, columns=noc_countries)

### Run main scraping code.
### First, set up the main update function.
### Importantly, this accounts for ties, which are reported, e.g. USACAN if USA and Canada both got a medal

def update_medal_counts(df, medals, year_num):
    for k in range(len(medals) // 3):
        country_triplet = medals[k*3:k*3+3]
        try:
            df.loc[year_num, country_triplet] += 1
        except:
            pass

def scrape_medal_counts(years, years_numeric, events, men_g, men_s, men_b, women_g, women_s, women_b):
    for y, y_num in zip(years, years_numeric):
        print(y_num)

        for e in events:
            try:
                url = f'http://www.olympedia.org/editions/{y}/sports/{e}'
                SR = scraper.get_result_similar(url, grouped=True)

                names = SR[namerule]
                gold = SR[Grule]
                silver = SR[Srule]
                bronze = SR[Brule]

                for i_w, name in enumerate(names):
                    if "Women" not in name:
                        continue

                    equivalent_event_men = name[:-5] + "Men"
                    i_m = find_event(names, equivalent_event_men)

                    update_medal_counts(men_g, gold[i_m], y_num)
                    update_medal_counts(men_s, silver[i_m], y_num)
                    update_medal_counts(men_b, bronze[i_m], y_num)

                    update_medal_counts(women_g, gold[i_w], y_num)
                    update_medal_counts(women_s, silver[i_w], y_num)
                    update_medal_counts(women_b, bronze[i_w], y_num)

            except:
                pass

        print()


scrape_medal_counts(
    summer_years, summer_years_numeric, summer_events,
    summer_men_g, summer_men_s, summer_men_b,
    summer_women_g, summer_women_s, summer_women_b
)

scrape_medal_counts(
    winter_years, winter_years_numeric, winter_events,
    winter_men_g, winter_men_s, winter_men_b,
    winter_women_g, winter_women_s, winter_women_b
)


pickle.dump([
    summer_men_g, summer_men_s, summer_men_b,
    summer_women_g, summer_women_s, summer_women_b,
    winter_men_g, winter_men_s, winter_men_b,
    winter_women_g, winter_women_s, winter_women_b], 
    open("medal_data.pickle", "wb")
)
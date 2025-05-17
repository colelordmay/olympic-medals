import numpy as np
import pandas as pd
import pickle
from map_code.config import *

### load data

with open("data/medal_data.pickle", "rb") as f:
    (summer_men_g, summer_men_s, summer_men_b,
     summer_women_g, summer_women_s, summer_women_b,
     winter_men_g, winter_men_s, winter_men_b,
     winter_women_g, winter_women_s, winter_women_b) = pickle.load(f)
    
with open("data/ioc_to_iso.pickle", "rb") as f:
    ioc_to_iso = pickle.load(f)



def update_medal_ratios(season='both'):
    if season == 'summer':
        men_count = (summer_men_g + summer_men_s + summer_men_b).sum()
        women_count = (summer_women_g + summer_women_s + summer_women_b).sum()
    elif season == 'winter':
        men_count = (winter_men_g + winter_men_s + winter_men_b).sum()
        women_count = (winter_women_g + winter_women_s + winter_women_b).sum()
    else:  # both
        men_count = (summer_men_g + summer_men_s + summer_men_b).sum() + (winter_men_g + winter_men_s + winter_men_b).sum()
        women_count = (summer_women_g + summer_women_s + summer_women_b).sum() + (winter_women_g + winter_women_s + winter_women_b).sum()

    medal_counts = men_count + women_count
    medal_ratios = women_count / medal_counts

    medal_ratios[medal_counts < 10] = np.NaN
    medal_counts[medal_counts < 10] = np.NaN

    medal_ratios.rename(index=ioc_to_iso, inplace=True)
    medal_counts.rename(index=ioc_to_iso, inplace=True)

    return pd.DataFrame({
        "Country": medal_ratios.index,
        "Ratio": medal_ratios.values,
        "TotalMedals": medal_counts.values
    })
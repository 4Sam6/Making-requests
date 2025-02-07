import matplotlib.pyplot as plt
import matplotlib.animation as animation
import wbdata
import requests
import pandas as pd
from datetime import datetime


country_codes_requested = ["USA", "DEU", "CHN", "AUS", "NGA", "BRA"]
all_data = []
for country in country_codes_requested:
    country_url = f"https://api.worldbank.org/v2/country/{country}/indicator/NY.GNP.PCAP.PP.CD?format=json"
    response = requests.get(country_url).json()
    if len(response) > 1 and response[1] is not None:
        all_data.extend(response[1])

df = pd.DataFrame(all_data)



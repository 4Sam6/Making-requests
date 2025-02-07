import matplotlib.pyplot as plt
import matplotlib.animation as animation
import wbdata
import requests
import pandas as pd
from datetime import datetime

# This will give you a variable that refers to the  indicator of total population of each country, 
# it is a wbdata.client.SearchResult, with this we can 
indicator = wbdata.get_indicators('SP.POP.TOTL')

# Fetch data from the World Bank API
df = wbdata.get_dataframe({"SP.POP.TOTL" : "Population, total"}, country=["NGA","USA","CHN","DEU", "BRA","AUS", ], date = ( "1960", "2025") )

# This is cleaning the data so it is ready to be used 

df = df.reset_index()
df = df.rename(columns={"date": "Years", "country": "Country", "Population, total": "Population"})
df["Years"] = df["Years"].astype(int)
df["Population"] = pd.to_numeric(df["Population"], errors="coerce")
df["Population"] = df["Population"].astype(int)
df = df.dropna()
df = df.sort_values(by=["Country", "Years"])

# This part of the code is for creating animations 

# Sort years for animation frames
years = sorted(df['Years'].unique())

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

def update(year):
    ax.clear()
    df_year = df[df['Years'] == year].sort_values(by='Population', ascending=True)  # Sort for better visualization
    
    df_year['Population'] = df_year['Population'] / 1000000  
   
    ax.barh(df_year['Country'], df_year['Population'])  # Horizontal bar chart
    ax.set_xlabel('Population (millions)')
    ax.set_ylabel('Country')
    ax.set_title(f'Population by Country in {year}')
    #ax.set_xlim(0, df['Population'].max() * 1.1000000)  # Set consistent x-axis range for clarity
       # Format x-axis to force numbers to show in millions
    ax.ticklabel_format(axis='x', style='plain')
# Create animation
ani = animation.FuncAnimation(fig, update, frames=years, interval=1000, repeat=True)

# Save as MP4 file
ani.save('Big7.mp4', writer='ffmpeg', fps=4)
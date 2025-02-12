# This script produces a graph made from data pulled from ourworldindata it shows the countries with the ten biggest  CO2 emissions  

# Importing the data sets that will be used

import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import git 
import yaml





# Create directory to store charts in, if it doesn't exist
repo_path = "/Users/Sam/Desktop/World_Development_Indicators" 
output_dir = os.path.join(repo_path, "daily_emissions") 
os.makedirs(output_dir, exist_ok=True)

# Fetching the data from the ourworldindata.org
df = pd.read_csv("https://ourworldindata.org/grapher/annual-co2-emissions-per-country.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})

# Finding the most recent year, it is important to do it this way and not just use the current year because if this is set to 
# automate then it would stay on the year it was set to and not update to the new most recent year 
most_recent_year = df["Year"].max()

# Filtering the DataFrame to only include rows from the most recent year this shapes the data so all of it is usable
df = df[df["Year"] == most_recent_year]

# Set pandas to display numbers in standard notation
pd.options.display.float_format = '{:.2f}'.format

# Cleaning the data, here we are getting ride of all the parts of the dataframe that we dont want, for example it shows data for
# the whole world but as we are just looking at countries then we dont need this 

# if the row doesnt have a code ( IS number ) the it wont be a country, using this we have got ride of all non country data
df = df.dropna(subset=["Code"])

# Removing the column "Code"
df = df.drop(columns = ["Code"])

# Removing the row for World 
df = df[df["Entity"] != "World"]

# Selecting the 10 biggest CO2 emiters, again its important to do it this way becuase these countries could change with an update
df = df.nlargest(10, "emissions_total")

# Formatting the data for the chart 
df["emissions_total"] = df["emissions_total"] / 100000000

# Creating the bar chart 
plt.bar(df["Entity"],df["emissions_total"])
# Rotate x-axis labels
plt.xticks(rotation=45)  # Rotates labels by 45 degrees
# Formating the y axis
plt.ticklabel_format(style="plain", axis="y")
# Creating the labels and Title
plt.xlabel("Country")
plt.ylabel("Total Emissions (billions,Tonnes)")
plt.title("Total Emissions by Country")

current_date = pd.Timestamp.now().strftime("%Y-%m-%d")



# Save the plot with the current date, this will save it in to its own directory
output_file = os.path.join(output_dir, f"emissions_10{current_date}.png")
plt.savefig(output_file, format="png", dpi=300)
plt.close()
# Delete old files (keeps only the previous week of charts)
files = sorted(os.listdir(output_dir))
if len(files) > 7:  # Keep only 7 days one week
    os.remove(os.path.join(output_dir, files[0]))

# making variable we will use
GITHUB_USERNAME = "4Sam6"
# read in secrets.yaml
with open("secrets.yml") as file:
    secrets = yaml.safe_load(file)
GITHUB_TOKEN = secrets["github_token"]   
REPO_NAME = "Making-requests" 

# Creating the remote repository URL using the token
REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"


# Set remote URL with authentication
repo = git.Repo(repo_path)
origin = repo.remote(name="origin")
origin.set_url(REPO_URL)


# Commit and push changes
repo.git.add(A=True)  # Add all changes
repo.index.commit(f"Updated emissions graph for {current_date}")
origin.push()

import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Step 1: Direct URL to the CSV file
url = 'https://www.opendata.nhs.scot/dataset/cff63b00-5c99-4efd-9ff7-83c4a1a95fe9/resource/a020dc7b-750d-4170-9472-9901a514912b/download/smoking_cessation_gender_age.csv'  

# Step 2: Send an HTTP request to the URL
response = requests.get(url)

if response.status_code == 200:
    print("Dataset successfully downloaded!")
    # Step 4: Write the content to a file (if it's CSV)
    with open('smoking_cessation_data.csv', 'wb') as file:
        file.write(response.content)
           # Step 5: Load the CSV into a DataFrame
    df = pd.read_csv('smoking_cessation_data.csv')
    
else:
    print(f"Failed to retrieve the dataset. Status code: {response.status_code}")


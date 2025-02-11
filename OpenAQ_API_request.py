# The following is script to show the countries that are within the API database, it has been limited to the first 100 enteres

import requests
import pandas as pd

# Creating variable for API key, this API key was found in setting once I had created an account 
API_KEY = "c3024b553e52dd4521f15b0980d5d5d0fa8ff256b4fbb5a20529392c61880384"

# Define headers with the API key, this is so the variable can be used as a parameter the way this is scripted will vary 
# but every API has a docs page that explains how authentication works.
headers = {"X-API-Key": API_KEY}

# This is the request itself it is the API's endpoint (https://api.openaq.org/v3) that is used in all requests
# plus (/countries) this is not a query so it doesnt use a ? it uses a / because it is part of the whole database    
response = requests.get("https://api.openaq.org/v3/countries", headers=headers)
# Now we have the database request saved as a variable we turn it in to a json with this 
database = response.json()
# Now we have it as a json we can go into the file and look at it, here we want to find the part in it that holds the data
# we want so we can refer it in this case it is 'results'
#print(database)
# Now that we have the data that we want to use we need to convert it into a dataframe so it is more usable when 
Countries = pd.DataFrame(database['results'])
Countries.head()
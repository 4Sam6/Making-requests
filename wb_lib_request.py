# Along with the standard libraries imported I have also imported wbdata with is used
# for requesting data from the World Bank Open Data API 

import wbdata
import requests
import pandas as pd
from datetime import datetime
import wbdata

# The following is a template for how to use the wbdata library to make a requests

# Fetch data from the World Bank API
df = wbdata.get_dataframe({"SP.POP.TOTL" : "Population, total"}, country=["FRA","USA"], date = ( "1960", "2025") ) 

# The first parameter is the indicator is the showing where the information we are referencing will come from
# The second is countries we want to focus on 
# The third is the dates or years to focus on
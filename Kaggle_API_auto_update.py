import kaggle
import pandas as pd
import requests
import matplotlib.pyplot as plt
import os
import hashlib
from datetime import datetime
import git
import yaml



# Specify Kaggle dataset
dataset = "akshaypawar7/millions-of-movies"
dataset_dir = "movies_dataset"
csv_file_path = os.path.join(dataset_dir, "movies.csv")
hash_file_path = "last_file_hash.txt"

# Function to compute SHA256 hash of a file
def compute_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Ensure dataset directory exists
os.makedirs(dataset_dir, exist_ok=True)

# Check if the CSV file exists
if os.path.exists(csv_file_path):
    old_hash = compute_file_hash(csv_file_path)
else:
    old_hash = None

# Download dataset
kaggle.api.dataset_download_files(dataset, path=dataset_dir, unzip=True)

# Compute new file hash
new_hash = compute_file_hash(csv_file_path)

# Compare hashes
if old_hash == new_hash:
    print("NO new data")
else:
    
    # Read the updated dataset
    df = pd.read_csv(csv_file_path)

    # Convert release_date to datetime format
    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")

    # Drop rows with NaT in release_date
    df = df.dropna(subset=["release_date"])

    # Get the current date
    current_date = datetime.today()

    # Filter out movies released in the future
    df = df[df["release_date"] < current_date]

    # Round vote_average to one decimal place
    df["vote_average"] = df["vote_average"].round(1)

    # Keep only the desired columns
    df = df[["runtime", "title", "release_date", "tagline", "vote_average"]]

    # Sort by release_date descending and keep the 10 most recent movies
    df = df.sort_values(by="release_date", ascending=False).head(10)

    # Creating the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["title"], df["runtime"], color="skyblue")
    plt.xticks(rotation=70)
    plt.ticklabel_format(style="plain", axis="y")

    # Labels and title
    plt.xlabel("Title")
    plt.ylabel("Runtime (minutes)") 
    plt.title("New Releases and Runtimes")

    # Save plot
    current_date_str = pd.Timestamp.now().strftime("%Y-%m-%d")
    output_filename = f'New_Releases_{current_date_str}.png'
    plt.savefig(output_filename, format='png', dpi=300)
    plt.close()

    # Save the new hash
    with open(hash_file_path, "w") as f:
        f.write(new_hash)
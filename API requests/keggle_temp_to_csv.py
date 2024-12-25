import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Set Kaggle credentials as environment variables
os.environ['KAGGLE_USERNAME'] = "tomerrudnitzky"
os.environ['KAGGLE_KEY'] = "9b51c85400acc0efd666c8c2e868ca92"

# Initialize and authenticate the Kaggle API
api = KaggleApi()
api.authenticate()

# Define the dataset path and download location
dataset_path = "swapnilbhange/average-temperature-of-cities"
output_directory = "./datasets"  # Specify your desired download location

# Download the dataset and unzip it
api.dataset_download_files(dataset_path, path=output_directory, unzip=True)

print("Dataset downloaded and unzipped in:", output_directory)

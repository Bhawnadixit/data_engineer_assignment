import requests
import json
import os
import sys
import pandas as pd

class clindata_downloader:
    def __init__(self, base_url, params, outpath):
        self.base_url = base_url   # Specify the API Base URL for ClinicalTrials.gov API
        self.params = params        # Specify the query parameters
        self.outpath = outpath
        self.data_path = None
        self.combined_studies = None
        
    def fetch_data(self):
        # Initialize an empty list to store the data
        data_list = []

        while True:
            if next_page_token:
                # Add the nextPageToken to the parameters for subsequent requests
                params["pageToken"] = next_page_token

            # Sending the request
            response = requests.get(self.base_url, params=self.params)

            # Handling the response
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                studies = data.get('studies', [])  # Extract the list of studies

                data_path = os.path.join(outpath, "rawdata")
                
                # path where all the downloaded data from API will be saved in a folder named as rawdata
                os.makedirs(self.outpath, exist_ok=True)
                # Append studies to the data list
                
                data_list.extend(studies)

                page_filename = f"studies_page_{next_page_token}.json" if next_page_token else "studies_page_1.json"
                # dump to a json file

                with open(os.path.join(data_path, page_filename), "w") as file:
                    json.dump(data, file, indent=4)

            #   Check for the nextPageToken
                next_page_token = data.get("nextPageToken")
                print(next_page_token)

                # Update the parameters with the nextPageToken
                params["pageToken"] = next_page_token

                if not next_page_token:
                    print("No more pages to fetch.")
                    break

            else:
                print(f"Error: {response.status_code} - {response.text}")
                break

        # After all pages are fetched, save all data into a single file
        with open(os.path.join(data_path, "all_studies.json"), "w") as file:
            json.dump(data_list, file, indent=4)

        print(f"Fetched a total of {len(data_list)} studies.")
        self.data_path = data_path
        return data_list
    
    def load_json(self):
        with open(os.path.join(self.data_path, "all_studies.json")) as f:
            combined_studies = json.load(f)
            self.combined_studies = combined_studies
            return self.combined_studies
        

# Define the main entry point
def main():
    try:
        # Create an instance of the data downloading pipeline
        base_url = "https://clinicaltrials.gov/api/v2/studies"

        # Parameters for the query
        params = {
            "format": "json",  # Requesting JSON format
            "query.term": "AREA[LastUpdatePostDate]RANGE[2024-10-20,2024-10-21]",  # Essie expression
        }
        outpath = os.getcwd()
        clindata_downloader(base_url, params, outpath)

    except Exception as e:
        print(f"Error: {e}")


# Check if the script is being run directly
if __name__ == "__main__":
    main()



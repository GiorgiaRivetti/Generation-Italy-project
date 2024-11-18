import os
import serpapi
from dotenv import load_dotenv
import json
import assets.params as params
import requests
import shutil
from datetime import datetime

load_dotenv()
assets_folder = os.getenv('ASSETS_FOLDER')

api_key = os.getenv('SERPAPI_KEY')
client = serpapi.Client(api_key=api_key)

url = f'https://serpapi.com/account?api_key={api_key}'
response = requests.get(url)

if response.status_code == 200:
    dati = response.json()
else:
    print('Errore nella richiesta:', response.status_code)


def fetch_all_jobs(page_limit: int, roles_list: list, cities_list: list, gl: str = 'it', hl: str = 'it') -> str:
    # Find all jobs combination of roles and cities
    """
    Make API calls to extract the data from Serpapi. The number of calls depends both on the page_limit and the
    number of elements in roles_list and cities_list

    :param page_limit: number of results page per query
    :param roles_list: list of jobs title
    :param cities_list: list of cities
    :param gl: country of jobs search
    :param hl: language of jobs search
    :return: a json file
    """
    user_input = ""

    while user_input != "y" and user_input != "n":
        user_input = input(f"This script will make {page_limit * len(roles_list) * len(cities_list)} calls to the API."
                           f"You have {dati["plan_searches_left"]} calls left. Do you want to proceed? (y/n) ")
        if user_input != "y" and user_input != "n":
            print("The only valid inputs are y for YES and n for NO")

    if user_input == "y":
        all_jobs = []  # List of the job ads (dictionaries)
        for role in roles_list:
            for city in cities_list:
                params = {
                    'engine': 'google_jobs',
                    'q': role,
                    'location': city,
                    'gl': f'{gl}',
                    'hl': f'{hl}'
                }

                results = client.search(params)
                page_count = 0

                while results and page_count < page_limit:

                    # Check if there are some results and add to the all_jobs list
                    if 'jobs_results' in results:
                        for job_result in results['jobs_results']:
                            job_data = {  # Create a dictionary for each job
                                'title': job_result.get('title'),
                                'company': job_result.get('company_name'),
                                'location': job_result.get('location'),
                                'description': job_result.get('description')
                            }
                            all_jobs.append(job_data)  # Append the job data (dict) to the list
                    page_count += 1
                    # To handle the "scrolling" of the result pages
                    if 'serpapi_pagination' in results and 'next' in results[
                        'serpapi_pagination'] and page_count < page_limit:
                        params['next_page_token'] = results['serpapi_pagination']['next_page_token']
                        results = client.search(params)
                    else:
                        break

        jobs_json = json.dumps({'jobs': all_jobs}, ensure_ascii=False)

        # Define the path to the file and the "old" folder
        file_path = os.path.join(assets_folder, 'all_jobs.json')
        old_folder = os.path.join(assets_folder, 'old')

        # Check if the file exists
        if os.path.exists(file_path):
            # Create the "old" folder if it doesn't exist
            if not os.path.exists(old_folder):
                os.makedirs(old_folder)

            # Generate a unique filename with a timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            old_file_path = os.path.join(old_folder, f'all_jobs_{timestamp}.json')

            # Move the existing file to the "old" folder with the new name
            shutil.move(file_path, old_file_path)

        # Write the new file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json_file.write(jobs_json)

        return jobs_json

    elif user_input == "n":
        print("See you soon")


fetch_all_jobs(page_limit=1, roles_list=params.roles_list, cities_list=params.cities_list)

# Fetch java developer jobs in Rome, 10 page of results
# fetch_all_jobs(page_limit=10, roles_list=params.roles_list[2], cities_list=params.cities_list[8])

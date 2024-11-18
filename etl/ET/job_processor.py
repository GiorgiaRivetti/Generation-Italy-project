import pandas as pd
from etl.ET.standardizer import Standardizer
from etl.ET.location_standardizer import LocationStandardizer
import json
import assets.params as params
from dotenv import load_dotenv
import os


load_dotenv()
assets_folder = os.getenv('ASSETS_FOLDER')


def get_final_df(jobs_json_path: str) -> pd.DataFrame:
    """
    Get the final dataframe with standard names and added columns

    :param jobs_json_path: the path of the .json file that contains the jobs
    :return: the final dataframe
    """

    with open(jobs_json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    jobs_list = data['jobs']

    # Convert json into a df and drop the duplicates
    df = pd.DataFrame(jobs_list)
    df = df.drop_duplicates(subset=['title', 'company', 'location', 'description'])

    all_cities_df = pd.read_csv(f"../{assets_folder}/comuni_italiani.csv")
    cities_list = all_cities_df["comune"].to_list()

    for index, row in df.iterrows():
        row['title'] = Standardizer.standardize_str_with_dict(input_str=row['title'], keywords=params.keywords_to_title)
        row['description'] = Standardizer.get_keywords(text=row['description'], keywords=params.hard_skills)
        row['location'] = Standardizer.standardize_str_with_list(input_str=row['location'], keywords=cities_list)

    df['province'] = LocationStandardizer(all_cities_df).list_from_dataframe(df['location'], "comune", "provincia")
    df['region'] = LocationStandardizer(all_cities_df).list_from_dataframe(df['location'], "comune", "regione")
    df['area'] = LocationStandardizer(all_cities_df).list_from_dataframe(df['location'], "comune", "zona")

    df['company'] = Standardizer.standardize_company_names(companies=df['company'].to_list())

    df = df.dropna()

    return df

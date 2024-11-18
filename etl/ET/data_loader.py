import pandas as pd
import json


class DataLoader:
    def __init__(self, assets_folder: str):
        self.assets_folder = assets_folder

    def load_csv(self, filename: str) -> pd.DataFrame:
        return pd.read_csv(f"{self.assets_folder}/{filename}")

    def load_json(self, filename: str) -> dict:
        with open(f"{self.assets_folder}/{filename}", 'r', encoding='utf-8') as json_file:
            return json.load(json_file)

import pandas as pd
import requests
from utils import constants

def load_nba_dataset(json_data):
    result_data = json_data['resultSets'][0]
    headers = result_data['headers']
    shots = result_data['rowSet']
    data_frame = pd.DataFrame(data=shots, columns=headers)
    return data_frame


def get_json_from_url(url):
    return requests.get(url, headers=constants.HEADERS).json()

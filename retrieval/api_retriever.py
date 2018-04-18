from collections import OrderedDict
import pandas as pd
import requests
from utils import constants


class ApiRetriever:

    def __init__(self, api_param):
        """
        Base class constructor which initializes data which is common to all retrievers.
        :param api_param: Api parameter for that specific use case.
        """
        self.base_url = "http://stats.nba.com/stats/"
        self.api_param = api_param
        self.param_dict = OrderedDict()

    def build_param_value_dict(self):
        """
        Needs to be implemented by each inherited retriever
        """
        pass

    def build_url_string(self):
        """
        Uses all params that are set and builds url string which can be used to retrieve data from stats.nba.com.
        :return: URL string.
        """
        url = self.base_url + self.api_param + "?"
        length = len(self.param_dict)
        for i, key in enumerate(self.param_dict):
            url += key
            value = self.param_dict[key]
            if isinstance(value, str):
                url += value
            else:
                url += str(value)
            if i != length:
                url += "&"
        return url

    def load_nba_dataset(self, index=0):
        """
        Loads the dataset from json data which is set based on API parameters.
        :param index: Often resultSets have mulitple results, but that depends on usecase so we will leave to inherited
        class to make decision of index choice.
        :return: Pandas data frame.
        """
        # Fetching json which contains data
        json_data = self.get_json_from_api_parameters()
        result_data = json_data['resultSets'][index]
        headers = result_data['headers']
        shots = result_data['rowSet']
        data_frame = pd.DataFrame(data=shots, columns=headers)
        return data_frame

    def get_json_from_api_parameters(self):
        """
        Fetches the json file from given url string.
        :return: Json object.
        """
        url = self.build_url_string()
        return requests.get(url, headers=constants.HEADERS).json()

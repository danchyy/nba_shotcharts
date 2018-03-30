from retrieval.api_retriever import ApiRetriever
from retrieval.api_retriever_factory import ApiRetrieverFactory
import unittest

class ApiRetrieverTest(unittest.TestCase):

    def westbrook_data_test(self):
        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        retriever = factory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id, season="2017-18")
        data = retriever.get_shotchart()
        self.assertIsNotNone(data)

    def get_westbrook_player_id_test(self):
        name = "Russell Westbrook"
        factory = ApiRetrieverFactory()
        retriever = factory.create_players_retriever_for_current_seasonn()
        data = retriever.get_player(name)
        self.assertEqual(len(data), 1)

if __name__=="__main__":
    unittest.main()
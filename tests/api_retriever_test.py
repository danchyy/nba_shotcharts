from retrieval.api_retriever import ApiRetriever
from retrieval.api_retriever_factory import ApiRetrieverFactory
import unittest

class ApiRetrieverTest(unittest.TestCase):

    def westbrook_data_test(self):
        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        retriever = factory.create_regular_retriever_for_player(player_id=westbrook_id, season="2017-18")
        data = retriever.retrieve_data()
        self.assertIsNotNone(data)

if __name__=="__main__":
    unittest.main()
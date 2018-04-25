from nba_stats.retrieval.api_retriever_factory import ApiRetrieverFactory
from nba_shotcharts.shotcharts.shotchart import Shotchart
import unittest


# Test for whole pipeline, retrieval of data and shotchart
class PipelineTest(unittest.TestCase):

    def plot_westbrook_shots_test(self):
        westbrook_id = "201566"
        retriever = ApiRetrieverFactory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id,
                                                                                      season="2017-18")
        data = retriever.get_shotchart()
        league_average = retriever.get_league_averages()

        shotchart = Shotchart(shotchart_data=data, league_average_data=league_average)
        shotchart.plot_shotchart("Westbrook shot chart")


if __name__ == "__main__":
    unittest.main()

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

    def westbrook_areas_test(self):
        areas = [u'Left Side Center(LC)', u'Center(C)']
        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        shotchart_retriever = factory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id,
                                                                                    season="2017-18")
        data = shotchart_retriever.get_shotchart_for_areas(areas)
        self.assertEqual(sorted(data.SHOT_ZONE_AREA.unique()), sorted(areas))

    def westbrook_zones_test(self):
        zones = [u'Above the Break 3', u'Right Corner 3']
        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        shotchart_retriever = factory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id,
                                                                                    season="2017-18")
        data = shotchart_retriever.get_shotchart_for_zones(zones)
        self.assertEqual(sorted(data.SHOT_ZONE_BASIC.unique()), sorted(zones))

    def westbrook_ranges_test(self):
        ranges = [u'Less Than 8 ft.', u'24+ ft.']
        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        shotchart_retriever = factory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id,
                                                                                    season="2017-18")
        data = shotchart_retriever.get_shotchart_for_ranges(ranges)
        self.assertEqual(sorted(data.SHOT_ZONE_RANGE.unique()), sorted(ranges))

    def westbrook_zone_area_range_test(self):
        areas = [u'Right Side(R)', u'Right Side Center(RC)']
        zones = [u'Above the Break 3', u'Right Corner 3']
        ranges = [u'24+ ft.']

        westbrook_id = "201566"
        factory = ApiRetrieverFactory()
        shotchart_retriever = factory.create_regular_shotchart_retriever_for_player(player_id=westbrook_id,
                                                                                    season="2017-18")

        data = shotchart_retriever.get_shotchart_for_zones_areas_ranges(zones=zones, areas=areas, ranges=ranges)
        self.assertEqual(sorted(data.SHOT_ZONE_BASIC.unique()), sorted(zones))
        self.assertEqual(sorted(data.SHOT_ZONE_AREA.unique()), sorted(areas))
        self.assertEqual(sorted(data.SHOT_ZONE_RANGE.unique()), sorted(ranges))

    def get_westbrook_player_id_test(self):
        name = "Russell Westbrook"
        factory = ApiRetrieverFactory()
        retriever = factory.create_players_retriever_for_season()
        data = retriever.get_player(name)
        self.assertEqual(len(data), 1)

if __name__=="__main__":
    unittest.main()
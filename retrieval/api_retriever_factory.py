from .api_retriever import ApiRetriever
from .shotchart_retriever import ShotchartRetriever
from .players_retriever import PlayersRetriever


class ApiRetrieverFactory():

    def create_regular_shotchart_retriever_for_player(self, player_id, season):
        """
        Method which creates classic retrieval class which fetches all shots and all stats in areas throughout
        one season. Simplest method of creation of ApiRetriever object.
        :param player_id: Id of a player that represents him in NBA database.
        :param season: Season from which the stats will be fetched.
        :return: ShotchartRetriever ready for retrieving data.
        """
        return ShotchartRetriever(player_id=player_id, season=season)


    def create_players_retriever_for_current_seasonn(self):
        """
        Creates the PlayersRetriever class which can retriever all players or only one of them based on further
        calls by user.
        :return: PlayersRetriever instance.
        """
        return PlayersRetriever()
from .shotchart_retriever import ShotchartRetriever
from .players_retriever import PlayersRetriever
from utils import constants


class ApiRetrieverFactory:

    @staticmethod
    def create_regular_shotchart_retriever_for_player(player_id, season):
        """
        Method which creates classic retrieval class which fetches all shots and all stats in areas throughout
        one season. Simplest method of creation of ApiRetriever object.
        :param player_id: Id of a player that represents him in NBA database.
        :param season: Season from which the stats will be fetched.
        :return: ShotchartRetriever ready for retrieving data.
        """
        return ShotchartRetriever(player_id=player_id, season=season)

    @staticmethod
    def create_players_retriever_for_season(season=constants.CURRENT_SEASON):
        """
        Creates the PlayersRetriever class which can retriever all players or only one of them based on further
        calls by user.
        :param season: Season for which the players will be retrieved, by default it is current season
        :return: PlayersRetriever instance.
        """
        return PlayersRetriever(season=season)

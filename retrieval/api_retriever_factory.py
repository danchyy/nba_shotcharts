from .api_retriever import ApiRetriever


class ApiRetrieverFactory():

    def create_regular_retriever_for_player(self, player_id, season):
        """
        Method which creates classic retrieval class which fetches all shots and all stats in areas throughout
        one season. Simplest method of creation of ApiRetriever object.
        :param player_id: Id of a player that represents him in NBA database.
        :param season: Season from which the stats will be fetched.
        :return: ApiRetriever ready for retrieving data.
        """
        return ApiRetriever(player_id=player_id, season=season)
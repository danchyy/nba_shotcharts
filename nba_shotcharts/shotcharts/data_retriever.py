from typing import Optional

from nba_api.stats.static import players
from nba_api.stats.endpoints.shotchartdetail import ShotChartDetail
from nba_shotcharts.utils.data_constants import CURRENT_SEASON


class DataRetrieverFactory:

    @staticmethod
    def get_shotchart_league_averages(
            player_name: str,
            season: str = CURRENT_SEASON,
            team_id: Optional[str] = None
    ):
        """
        Retrieves shotchart detailed data and league averages for each specific zones.


        :param player_name: Player's full name whose shotchart will be retrieved.

        :param team_id: Team id which is used only if multiple players are found

        :param season: Season for which the data will be retrieved

        :return: Shotchart for player in given season
        """
        # Let's assume that players are correctly on first index
        players_for_name = players.find_players_by_full_name(player_name)
        if not players_for_name:
            raise ValueError('Invalid player name given, no players found')
        if len(players_for_name) == 1:
            player = players_for_name[0]
        else:
            # todo dbratulic: USE TEAM ID TO FETCH PLAYER_ID
            print("Will use " + team_id + " in future, using first player for now.")
            player = players_for_name[0]

        shotchart_obj = ShotChartDetail(
            team_id=0,  # not necessary for fetching shotchart data
            player_id=player['id'],
            season_nullable=season,
            context_measure_simple='FGA'
        )
        dataset, league_averages = shotchart_obj.get_data_frames()
        dataset.LOC_X = -dataset.LOC_X  # REAL DATA IS FLIPPED
        dataset = dataset.loc[(dataset.SHOT_ZONE_AREA != "Back Court(BC)")
                              & (dataset.LOC_Y < 300)]  # drop shots that aren't close to the center
        return dataset, league_averages

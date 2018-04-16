from .api_retriever import ApiRetriever
from utils import constants
import pandas as pd
from utils import shotchart_constants

class ShotchartRetriever(ApiRetriever):
    def __init__(self, period=0, vs_conference="", league_id="00", last_n_games=0, team_id=0, location="", outcome="",
                 context_measure="FGA", date_from="", date_to="", opponent_team_id=0, range_type=0,
                 season=constants.CURRENT_SEASON, ahead_behind="", player_id=0, vs_division="", point_diff="",
                 rookie_year="", game_segment="", month=0, clutch_time="", season_type="Regular Season",
                 season_segment="",
                 game_id="", player_position=""):
        """
        Constructor for retriever of data.
        :param period: In which period shots were made (1, 2, 3, 4, 5 for OT) or 0 for all periods.
        :param vs_conference: Conference can be either 'West' or 'East' or empty.
        :param league_id: ID of the league, either 00, 20 or 10 (00 is normal NBA).
        :param last_n_games: Integer representing last N games, 0 for all games.
        :param team_id: ID of the team, 0 default.
        :param location: Location can be 'Home' or 'Road' or empty.
        :param outcome: Either 'W' or 'L'.
        :param context_measure: One of following stat measures 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT',
        'PF', 'EFG_PCT', 'TS_PCT', 'PTS_FB', 'PTS_OFF_TOV', 'PTS_2ND_CHANCE'.
        :param date_from: Date in format mm-dd-yyyy.
        :param date_to: Date in format mm-dd-yyyy.
        :param opponent_team_id: Opponent team id, to filter games only vs specific team, default 0, means don't filter.
        :param range_type: 0 for all shots, 1 and 2 for areas only, default 0.
        :param season: Format of yyyy-yy.
        :param ahead_behind: One of 'Ahead or Behind', 'Ahead or Tied', 'Behind or Tied' or empty.
        :param player_id: Player ID from NBA's database, obligatory.
        :param vs_division: One of following divisions: 'Atlantic', 'Central', 'Northwest', 'Pacific', 'Southeast',
        'Southwest', 'East', 'West'.
        :param point_diff: One or more digits, or empty.
        :param rookie_year: yyyy-yy or empty if not wanted.
        :param game_segment: One of following options: 'First Half', 'Second Half', 'Overtime' or empty.
        :param month: Integer between 1 and 12.
        :param clutch_time: Either empty or one of following options: 'Last 5 Minutes', 'Last 4 Minutes',
        'Last 3 Minutes', 'Last 2 Minutes', 'Last 1 Minutes', 'Last 30 Seconds', 'Last 10 Seconds'.
        :param season_type: Either empty or 'Regular Season', 'Pre Season', 'Playoffs', or 'All Star'.
        :param season_segment: Either empty or 'Pre All-Star' or 'Post All-Star'.
        :param game_id: Empty or 10 digit number.
        :param player_position: Empty or 'Guard', 'Forward', or 'Center'.
        """
        super().__init__(constants.SHOTCHART_PARAM)
        self.shotchart = None
        self.league_average = None
        # Period
        self.period = period
        # '^((East)|(West))?$'
        self.vs_conference = vs_conference
        # '(00)|(20)|(10)'
        self.league_id = league_id
        # int
        self.last_n_games = last_n_games
        # int
        self.team_id = team_id
        # '^((Home)|(Road))?$'
        self.location = location
        # '^((W)|(L))?$'
        self.outcome = outcome
        # '^((PTS)|(FGM)|(FGA)|(FG_PCT)|(FG3M)|(FG3A)|(FG3_PCT)|(PF)|(EFG_PCT)|(TS_PCT)|(PTS_FB)|(PTS_OFF_TOV)|
        #  (PTS_2ND_CHANCE)|(PF))?$'
        self.context_measure = context_measure
        # mm-dd-yyyy
        self.date_from = date_from
        # mm-dd-yyyy
        self.date_to = date_to
        # int
        self.opponent_team_id = opponent_team_id
        # empty, 0 -> both shots and areas, 1 and 2 -> only areas
        self.range_type = range_type
        # yyyy-yy
        self.season = season
        # '^((Ahead or Behind)|(Ahead or Tied)|(Behind or Tied))?$'
        self.ahead_behind = ahead_behind
        # int, OBLIGATORY
        self.player_id = player_id
        # '^((Atlantic)|(Central)|(Northwest)|(Pacific)|(Southeast)|(Southwest)|(East)|(West))?$'
        self.vs_division = vs_division
        # '^\d*$'
        self.point_diff = point_diff
        # '^(\d{4}-\d{2})?$'
        self.rookie_year = rookie_year
        # '^((First Half)|(Overtime)|(Second Half))?$'
        self.game_segment = game_segment
        # int, 1-12
        self.month = month
        # '^((Last 5 Minutes)|(Last 4 Minutes)|(Last 3 Minutes)|(Last 2 Minutes)|(Last 1 Minute)|(Last 30 Seconds)|
        # (Last 10 Seconds))?$'
        self.clutch_time = clutch_time
        # '^(Regular Season)|(Pre Season)|(Playoffs)|(All Star)$'
        self.season_type = season_type
        # '^((Post All-Star)|(Pre All-Star))?$'
        self.season_segment = season_segment
        # '^(\d{10})?$'
        self.game_id = game_id
        # '^((Guard)|(Center)|(Forward))?$'
        self.player_position = player_position
        self.build_param_value_dict()

        self.decorate = False
        self.decoration_dataset = None

    def build_param_value_dict(self):
        """
        Builds parameter dictionary for retrieval of shotchart data.
        """
        self.param_dict["Period="] = self.period
        self.param_dict["VsConference="] = self.vs_conference
        self.param_dict["LeagueID="] = self.league_id
        self.param_dict["LastNGames="] = self.last_n_games
        self.param_dict["TeamID="] = self.team_id
        self.param_dict["Location="] = self.location
        self.param_dict["Outcome="] = self.outcome
        self.param_dict["ContextMeasure="] = self.context_measure
        self.param_dict["DateFrom="] = self.date_from
        self.param_dict["DateTo="] = self.date_to
        self.param_dict["OpponentTeamID="] = self.opponent_team_id
        self.param_dict["RangeType="] = self.range_type
        self.param_dict["Season="] = self.season
        self.param_dict["AheadBehind="] = self.ahead_behind
        self.param_dict["PlayerID="] = self.player_id
        self.param_dict["VsDivision="] = self.vs_division
        self.param_dict["PointDiff="] = self.point_diff
        self.param_dict["RookieYear="] = self.rookie_year
        self.param_dict["GameSegment="] = self.game_segment
        self.param_dict["Month="] = self.month
        self.param_dict["ClutchTime="] = self.clutch_time
        self.param_dict["SeasonType="] = self.season_type
        self.param_dict["SeasonSegment="] = self.season_segment
        self.param_dict["GameID="] = self.game_id
        self.param_dict["PlayerPosition="] = self.player_position

    def get_shotchart(self):
        """
        Returns shotchart data for parameters that are set.
        :return: Shotchart data in Pandas DataFrame object.
        """
        # Returning pandas data frame
        if self.shotchart is not None:
            return self.shotchart
        dataset = self.load_nba_dataset(index=0)
        dataset.LOC_X = -dataset.LOC_X  # REAL DATA IS FLIPPED
        dataset = dataset.loc[(dataset.SHOT_ZONE_AREA != "Back Court(BC)")
                              & (dataset.LOC_Y < 300)]  # drop shots that aren't close to the center
        # To cache the data
        self.shotchart = dataset
        return dataset

    def get_league_averages(self):
        """
        Returns the league averages data for some spots on the court.
        :return: League averages data in Pandas DataFrame object.
        """
        return self.load_nba_dataset(index=1)

    def get_shotchart_for_zones(self, zones):
        """
        Creates shotchart data only for zones which are given as argument. Available zones are 'Mid-Range',
        'Restricted Area', 'Left Corner 3', 'In The Paint (Non-RA)', 'Above the Break 3', 'Right Corner 3'.
        :param zones: Zones upon which the shots will be filtered.
        :return: Zone filtered shotchart data.
        """
        shotchart_data = self.decoration_dataset if self.decorate else self.get_shotchart()

        assert isinstance(shotchart_data, pd.DataFrame)
        return shotchart_data.loc[shotchart_data.SHOT_ZONE_BASIC.isin(zones)]

    def get_shotchart_for_areas(self, areas):
        """
        Creates shotchart data only for areas which are given as argument. Available areas are 'Right Side Center(RC)',
        'Left Side Center(LC)', 'Center(C)', 'Left Side(L)', 'Right Side(R)'.
        :param areas: Areas upon which the shots will be filtered.
        :return: Area filtered shotchart data.
        """
        shotchart_data = self.decoration_dataset if self.decorate else self.get_shotchart()

        assert isinstance(shotchart_data, pd.DataFrame)
        return shotchart_data.loc[shotchart_data.SHOT_ZONE_AREA.isin(areas)]

    def get_shotchart_for_ranges(self, ranges):
        """
        Creates shotchart data only for ranges which are given as argument. Available ranges are '16-24 ft.',
        'Less Than 8 ft.', '24+ ft.', '8-16 ft.'.
        :param ranges: Ranges upon which the shots will be filtered.
        :return: Ranges filtered shotchart data.
        """
        shotchart_data = self.decoration_dataset if self.decorate else self.get_shotchart()

        assert isinstance(shotchart_data, pd.DataFrame)
        return shotchart_data.loc[shotchart_data.SHOT_ZONE_RANGE.isin(ranges)]

    def get_shotchart_for_zones_areas_ranges(self, zones=None, areas=None, ranges=None):
        """
        Retrieves shotchart data for combination of zones, areas and ranges. If None or empty array
        is given for any of the arguments that argument will be excluded from combination.
        :param zones: Zones which will be used for filtering data.
        :param areas: Areas which will be used for filtering data.
        :param ranges: Ranges which will be used for filtering data.
        :return: Data with filtered data.
        """
        self.decorate = True
        self.decoration_dataset = self.get_shotchart()
        if len(zones) > 0:
            self.decoration_dataset = self.get_shotchart_for_zones(zones)
        if len(areas) > 0:
            self.decoration_dataset = self.get_shotchart_for_areas(areas)
        if len(ranges) > 0:
            self.decoration_dataset = self.get_shotchart_for_ranges(ranges)

        self.decorate = False

        return self.decoration_dataset


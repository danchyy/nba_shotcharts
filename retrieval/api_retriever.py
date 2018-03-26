from utils import constants
from collections import OrderedDict
import pandas as pd
import requests
from utils import constants


class ApiRetriever:

    def __init__(self, period=0, vs_conference="", league_ID="00", last_n_games=0, team_id=0, location="", outcome="",
                 context_measure="FGA", date_from="", date_to="", opponent_team_id=0, range_type=0,
                 season=constants.CURRENT_SEASON, ahead_behind="", player_id=0, vs_division="", point_diff="",
                 rookie_year="", game_segment="", month=0, clutch_time="", season_type="Regular Season", season_segment="",
                 game_id="", player_position=""):
        """
        Constructor for retriever of data.
        :param period: In which period shots were made (1, 2, 3, 4, 5 for OT) or 0 for all periods.
        :param vs_conference: Conference can be either 'West' or 'East' or empty.
        :param league_ID: ID of the league, either 00, 20 or 10 (00 is normal NBA).
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
        self.base_url = "http://stats.nba.com/stats/"
        self.shot_chart_param = "shotchartdetail?"
        self.period = period
        # '^((East)|(West))?$'
        self.vs_conference = vs_conference
        # '(00)|(20)|(10)'
        self.league_ID = league_ID
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
        self.param_dict = OrderedDict()
        self.build_param_value_dict()

    def build_param_value_dict(self):
        """
        Builds dictionary which has string keys mapped to values of parameters which are assigned to it.
        :return:
        """
        self.param_dict["Period="] = self.period
        self.param_dict["VsConference="] = self.vs_conference
        self.param_dict["LeagueID="] = self.league_ID
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

    def build_url_string(self):
        """
        Method uses all params that are set and builds url string which can be used to retrieve data from stats.nba.com
        :return: URL string
        """
        url = self.base_url + self.shot_chart_param
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


    def load_nba_dataset(self, json_data):
        """
        Loads the dataset from given json data, here the data which is extracted is based on range type parameter.
        If it's set to zero then the shots from player will be extracted, otherwise the league averages will be extracted.
        :param json_data: Json data from where the shots will be extracted only
        :return: Pandas data frame
        """
        index = 0 if self.range_type == 0 else 1
        result_data = json_data['resultSets'][index]
        headers = result_data['headers']
        shots = result_data['rowSet']
        data_frame = pd.DataFrame(data=shots, columns=headers)
        return data_frame

    def get_json_from_url(self, url):
        """
        Fetches the json file from given url string
        :param url: URL string for shots
        :return: Json object
        """
        print(requests.get(url, headers=constants.HEADERS))
        return requests.get(url, headers=constants.HEADERS).json()

    def retrieve_data(self):
        """
        Method which gathers all the steps and retrieves the json for parameters that were set up for URL string
        :return: Pandas data frame
        """
        # Getting url string
        url = self.build_url_string()
        # Retrieving json
        json = self.get_json_from_url(url)
        # Returning pandas data frame
        return self.load_nba_dataset(json_data=json)
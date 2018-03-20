

class ApiRetriever:

    def __init__(self, period=0, vs_conference="", league_ID=00, last_n_games=0, team_id=0, location="", outcome="",
                 context_measure="FGA", date_from="", date_to="", opponent_team_id=0, range_type="", season="2017-18",
                 ahead_behind="", player_id=0, vs_division="", point_diff="", rookie_year="", game_segment="",
                 month=0, clutch_time="", season_type="", season_segment="", game_id="", player_position=""):
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


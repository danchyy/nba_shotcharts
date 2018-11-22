from shotcharts.data_retriever import DataRetrieverFactory
from shotcharts.shotchart import Shotchart

if __name__ == '__main__':
    player_name = input("Input player name which you want to retrieve shotchart: ")
    data, league_averages = DataRetrieverFactory.get_shotchart_league_averages(player_name)
    shotchart = Shotchart(
        shotchart_data=data,
        league_average_data=league_averages,
        should_save_image=True
    )
    shotchart.plot_shotchart(player_name + " Shotchart for 2018-19")
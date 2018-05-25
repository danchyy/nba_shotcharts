# nba_shotcharts

This is a project which can plot a shot chart for any player from NBA. 
Currently the only basic functionality is available, meaning that all shots will be plotted
in binned way. 

This project was written for Python 3.

Table of contents:

* [Dependencies](#dependencies)

* [Installation](#installation)

* [Usage Instructions](#usage-instructions)


### Dependencies

There are some usual dependencies on python packages that are well known:

* docutils >= 0.3

* pandas >= 0.20.3

* matplotlib >= 2.2.2

* numpy >= 1.14.2

* seaborn >= 0.8.1

Also, there is a dependency on my package, which can be viewed [here](https://github.com/danchyy/nba_stats). 
It is a package which is used for retrieval of data which will later on be visualized here using this package.
That package is available on PyPi and can be installed with `pip install nba_stats` 


### Installation

This project isn't available at PyPi yet as I need to work on several things to improve usability, but 
it can be easily set up and installed using following commands:

```
git clone git@github.com:danchyy/nba_shotcharts.git
cd nba_shotcharts
pip install .
``` 


### Usage Instructions

As mentioned before, the usage will be simplified in near future, but as of right the following template can be followed
to obtain a shotchart for any player.

```python
from nba_shotcharts.shotcharts.shotchart import Shotchart
from nba_stats.retriever_factories.api_retriever_factory import ApiRetrieverFactory
from nba_stats.retrieval.players_retriever import PlayersRetriever

pl_ret = PlayersRetriever()
player_id = pl_ret.get_player_id("Russell Westbrook")
factory = ApiRetrieverFactory()
retriever = factory.create_regular_shotchart_retriever_for_player(player_id=player_id, season="2017-18")
data = retriever.get_shotchart()
league_average = retriever.get_league_averages()
shotchart = Shotchart(shotchart_data=data, league_average_data=league_average)
shotchart.plot_shotchart("Westbrook shot chart")
```

Which produces the following image:

![alt text](https://raw.githubusercontent.com/danchyy/nba_shotcharts/master/images/westbrook.png "Shot chart for Russell Westbrook")


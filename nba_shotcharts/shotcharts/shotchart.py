import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc
import operator
import io
from nba_shotcharts.utils.custom_marker import get_smooth_square


class Shotchart:

    def __init__(self, shotchart_data, league_average_data, lines_color="black", lw=2,
                 outer_lines=True, marker="ss", number_of_markers="medium", image_size="large", court_color="dark",
                 should_save_image=False):
        """
        Constructor of Shotchart object. It takes several arguments which will be used later to modify the
        look of final plot.

        :param shotchart_data: Data frame object
        :param league_average_data: Data frame object which contains league average percentages per zone.
        :param lines_color: Color of the court lines.
        :param lw: Widht of the court lines.
        :param outer_lines: Whether outer lines of the court should be plotted
        :param marker: Marker which will be used, standard notation of Matplotlib's library or 'ss' for Smooth Square (default value).
        :param number_of_markers: Whether there will be small, medium or large number of markers (this variable controls the number of bins).
        :param image_size: Size of image, can be small, medium and large.
        :param court_color: Color of the court, can be dark or light.
        :param should_save_image: If shotchart wants to be saved or created for web interface, this flag must be set to True so that image can be properly processed.
        """
        self.shotchart_data = shotchart_data
        self.league_average = league_average_data
        self.should_save_image = should_save_image
        self.lines_color = lines_color
        self.outer_lines = outer_lines
        self.bin_number_x = 30.0
        if number_of_markers == "small":
            self.bin_number_x = 20.0
        elif number_of_markers == "large":
            self.bin_number_x = 40.0
        self.width = 500.0  # Width of the area that will be binned
        self.height = 470.0  # Height of the area that will be binned, these numbers are equivalent to plot range
        self.bin_number_y = self.height / (self.width / self.bin_number_x)
        self.norm_x = 250  # Shots can go left and right of basket at most to -250 and +250
        self.norm_y = 48.5  # Minimal range of shots is -48.5
        self.lw = lw  # Width of the lines on the court
        self.outer_lines = outer_lines  # Whether the outer lines will be plotted

        # Color map for comparing percentages of shots
        self.cmap = sns.blend_palette(colors=["#4159E1", "#B0E0E6", "#FFFF99", "#EF3330", "#AB2020"], as_cmap=True)

        # Combination for dark court color
        self.court_color = '#36383F'
        self.text_color = "#E8E8FF"

        # Combination for dark court color
        if court_color == "light":
            self.court_color = '#AEAEAE'
            self.text_color = '#353638'

        self.marker = marker  # Marker for plot
        if self.marker == "ss":
            self.marker = get_smooth_square()

        self.base_figure_size = 8  # size of figure in inches, DPI is set to 80
        self.figure_size = self.base_figure_size
        self.font_size = 8.5  # font for text that depicts legend
        self.multiplier = 1  # Multiplier for markers
        self.title_font = 16  # Font of title is a bit bigger than regular text font
        if self.should_save_image:
            self.font_size = 7
            self.multiplier = 0.75
        if image_size == "medium":  # Based on image size, the parameters are increased accordingly to the size
            self.figure_size = 12
            self.font_size = self.figure_size + 1
            self.multiplier = 2.5
            self.title_font = 24
            if self.should_save_image:
                self.font_size = self.figure_size - 2
                self.multiplier = 1.75
        elif image_size == "large":
            self.figure_size = 16
            self.font_size = self.figure_size + 1
            self.multiplier = 5
            self.title_font = 32
            if self.should_save_image:
                self.font_size = self.figure_size - 2
                self.multiplier = 3.25

        # List for markers which will display legend for marker size that explains shot frequency
        # List contains tuple that represent (x, y, marker_size_modifier)
        self.marker_size_legend = 20
        self.size_legend = [
            (-218, 374, 1),
            (-205, 377, 3),
            (-190, 380, 6),
            (-171, 383, 9),
            (-151, 386, 12)
        ]

        # List for markers which will display legend for color of markers that explains shot percentage
        # List contains tuple that represent (x, y, color_of_marker)
        self.marker_color_legend = 300
        self.color_legend = [
            (114, 368, "#4159E1"),
            (133, 371, "#B0E0E6"),
            (153, 374, "#FFFF99"),
            (172, 377, "#EF3330"),
            (191, 380, "#AB2020")
        ]

        # Parameters needed for calling the plt.text command for frequency legend
        self.less_frequent_string = (-240, 360, "Less\nFrequent", -5)
        self.more_frequent_string = (-143, 395, "More\nFrequent", -5)

        # Parameters needed for calling the plt.text command for shot percentage legend
        self.comparison_string = (70, 410, "Comparison with league average percentage")
        self.below_average_string = (75, 345, "Below\nAverage\n  (-10%)", 0)
        self.above_average_string = (205, 375, "Above\nAverage\n  (+10%)", 0)

    # Amazing function by Bradley Fay for plotting the nba court
    # source: https://github.com/bradleyfay/py-Goldsberry/blob/master/docs/
    # Visualizing%20NBA%20Shots%20with%20py-Goldsberry.ipynb
    def draw_court(self, ax=None):
        """
        Method which is used for drawing the court lines on shotchart image.

        :param ax: Ax of the plot, not necessary
        :return: axes
        """
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()

        # Create the various parts of an NBA basketball court

        # Create the basketball hoop
        # Diameter of a hoop is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        hoop = Circle((0, 0), radius=7.5, linewidth=self.lw, color=self.lines_color, fill=False)

        # Create backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=self.lw, color=self.lines_color)

        # The paint
        # Create the outer box 0f the paint, width=16ft, height=19ft
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=self.lw, color=self.lines_color, zorder=0,
                              fill=False)
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=self.lw, color=self.lines_color, zorder=0,
                              fill=False)

        # Create free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                             linewidth=self.lw, color=self.lines_color, fill=False, zorder=0)
        # Create free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, zorder=0,
                                linewidth=self.lw, color=self.lines_color, linestyle='dashed')
        # Restricted Zone, it is an arc with 4ft radius from center of the hoop
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=self.lw, zorder=0,
                         color=self.lines_color)

        # Three point line
        # Create the side 3pt lines, they are 14ft long before they begin to arc
        corner_three_a = Rectangle((-220, -47.5), 0, 138, linewidth=self.lw, zorder=0,
                                   color=self.lines_color)
        corner_three_b = Rectangle((220, -47.5), 0, 138, linewidth=self.lw, color=self.lines_color, zorder=0)
        # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
        # I just played around with the theta values until they lined up with the
        # threes
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=self.lw, zorder=0,
                        color=self.lines_color)

        # Center Court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, zorder=0,
                               linewidth=self.lw, color=self.lines_color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, zorder=0,
                               linewidth=self.lw, color=self.lines_color)

        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]

        if self.outer_lines:
            # Draw the half court line, baseline and side out bound lines
            outer_lines = Rectangle((-250, -48), 500, 470, linewidth=self.lw,
                                    color=self.lines_color, fill=False)
            court_elements.append(outer_lines)

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax

    def create_bins(self):
        """
        Method which creates bins the dataset into squared grid. This is used so that plot looks nicer than the raw
        locations plot. Along with binning the data, the percentages per zones and for each bin are calculated here
        and added to the copy of self.shotchart_data object so they can be used for plotting later.

        :return: Returns the copied  self.shotchart_data pandas DataFrame object with additional info about the shots.
        """
        # Binned x and y coordinates
        x_bins, y_bins = [], []
        # Copying the dataset to add more data
        copied_df = self.shotchart_data.copy()
        # Keys are basically x_bin and y_bin
        keys = []
        # Counter of shots and shots made per locations
        location_counts, location_made = Counter(), Counter()
        # be found

        # Size of elements in bin, they should be the same
        bin_size_x = float(self.width) / float(self.bin_number_x)
        bin_size_y = float(self.height) / float(self.bin_number_y)
        # List for locations of shots
        locations_annotated = []
        # Counter of shots and shots made per zone
        zones_counts, zones_made = Counter(), Counter()

        # Maximum size of an element in one bin
        max_size = int((int(bin_size_x) - 1) * (int(bin_size_y) - 1))

        # Keys that are in restricted area will be stored here, this will be used for finding maximum number of shots
        restricted_area_keys = []

        # Dictionary which will determine the color of marker in bin
        percentage_color_dict = {}

        for i in range(len(self.shotchart_data)):

            # Row from data frame
            row = self.shotchart_data.iloc[i]

            x_shot_orig, y_shot_orig = row.LOC_X, row.LOC_Y

            # Normalize
            x_shot = x_shot_orig + self.norm_x  # to put minimum to zero
            y_shot = y_shot_orig + self.norm_y  # to put minimum to zero

            # bin_index = (x_shot / w) * bin_size
            curr_x_bin = 0 if x_shot == 0 else int((x_shot / float(self.width)) * self.bin_number_x)
            curr_y_bin = 0 if y_shot == 0 else int((y_shot / float(self.height)) * self.bin_number_y)

            # Key for dicts
            key = (curr_x_bin, curr_y_bin)

            if row.SHOT_ZONE_BASIC == "Restricted Area":
                restricted_area_keys.append(key)

            # Counting number of shots made and shots shot
            keys.append(key)
            location_counts[key] += 1
            location_made[key] += row.SHOT_MADE_FLAG

            basic_shot_zone, shot_zone_area = row.SHOT_ZONE_BASIC, row.SHOT_ZONE_AREA
            zone_dist = row.SHOT_ZONE_RANGE

            area_code = shot_zone_area.split("(")[1].split(")")[0]
            if "3" in basic_shot_zone:
                locations_annotated.append("3" + area_code)
            elif "Paint" in basic_shot_zone:
                locations_annotated.append("P" + area_code + zone_dist[0])
            elif "Mid" in basic_shot_zone:
                locations_annotated.append("M" + area_code + zone_dist[0])
            else:
                locations_annotated.append("R" + area_code)

            # Creating key for zones
            zone_key = (basic_shot_zone, shot_zone_area, zone_dist)

            # Counting the occurences based on both bin_key and zone_key, because of that we have dict in dict
            if key in percentage_color_dict:
                if zone_key in percentage_color_dict[key]:
                    percentage_color_dict[key][zone_key] = percentage_color_dict[key][zone_key] + 1
                else:
                    percentage_color_dict[key][zone_key] = 1
            else:
                percentage_color_dict[key] = {}
                percentage_color_dict[key][zone_key] = 1

            zones_counts[zone_key] += 1

            if row.SHOT_MADE_FLAG:
                zones_made[zone_key] += 1

        shot_locations_percentage = []  # percentage in given bin
        shot_locations_counts = []
        raw_counts = []
        # List which contains comparison for each shot with league average in that zone
        shot_comparison = []
        # List which contains comparison of player's shooting in zone vs league average
        per_zone_comparison = []
        per_zone_percentage = []

        # Finding the maximal number of shots from data
        non_ra = []
        for key in location_counts:
            if key not in restricted_area_keys:
                if location_counts[key] not in non_ra:
                    non_ra.append(location_counts[key])

        sorted_non_ra = sorted(non_ra)
        max_out_of_restricted = float(sorted_non_ra[-1])

        for j in range(len(self.shotchart_data)):
            key = keys[j]
            x_bin, y_bin = key[0], key[1]
            shot_percent = float(location_made[key]) / location_counts[key]
            # shot_percent = np.clip(shot_percent, 0.3, 0.7)
            shot_locations_percentage.append(shot_percent * 100)
            if self.league_average is not None:
                # Getting info about zone
                # We are getting that info from
                per_zone_counter_from_percentage_color_dict = percentage_color_dict[key]
                zone_key = max(per_zone_counter_from_percentage_color_dict.items(),
                               key=operator.itemgetter(1))[0]

                shot_zone_basic = zone_key[0]
                shot_zone_area = zone_key[1]
                distance = zone_key[2]

                # Calculating the percentage in current zone
                zone_percent = 0.0 if zone_key not in zones_made else float(zones_made[zone_key]) / \
                    float(zones_counts[zone_key])

                # Retrieving league average percentage for current zone
                avg_percentage = self.league_average.loc[(self.league_average.SHOT_ZONE_BASIC == shot_zone_basic) &
                                                         (self.league_average.SHOT_ZONE_AREA == shot_zone_area) &
                                                         (self.league_average.SHOT_ZONE_RANGE == distance)].FG_PCT.iloc[
                    0]  # PEPe
                # Comparison of league average and each shot
                shot_comparison.append(np.clip((shot_percent - avg_percentage) * 100, -10, 10))
                # Comparison of zone and league average
                per_zone_comparison.append(np.clip((zone_percent - avg_percentage) * 100, -10, 10))
                # Percentage of shot in current zone, kinda inaccurate info, good for some other type of plot
                per_zone_percentage.append(np.clip(zone_percent * 100, 35, 65))

            # Calculating value to which the markers will be scaled later on
            # The data in restricted is scaled to maximum out of restricted area, because players usually have a lot
            # more shots in restricted area
            value_to_scale = max_out_of_restricted if location_counts[key] > max_out_of_restricted else \
                location_counts[key]
            # Storing the data into a list
            shot_locations_counts.append((float(value_to_scale) / max_out_of_restricted) * max_size)

            # Count of shots per bin
            raw_counts.append(location_counts[key])

            # Middle of current and next bin is where we will place the marker in real coordinates
            unbinned_x = ((x_bin * float(self.width)) / self.bin_number_x + (
                    (x_bin + 1) * float(self.width)) / self.bin_number_x) / 2 - self.norm_x
            unbinned_y = ((y_bin * float(self.height)) / self.bin_number_y + (
                    (y_bin + 1) * float(self.height)) / self.bin_number_y) / 2 - self.norm_y

            # Adding binned locations
            x_bins.append(unbinned_x)
            y_bins.append(unbinned_y)

        # Binned locations
        copied_df['BIN_LOC_X'] = x_bins
        copied_df['BIN_LOC_Y'] = y_bins
        # Percentage comparison with league averages
        if self.league_average is not None:
            # Comparison of each shot with league average for that zone
            copied_df['PCT_LEAGUE_AVG_COMPARISON'] = shot_comparison
            # Comparison of each zone with league average for that zone
            copied_df['PCT_LEAGUE_COMPARISON_ZONE'] = per_zone_comparison
        # Percentage of shots for that location
        copied_df['LOC_PERCENTAGE'] = shot_locations_percentage
        # Percentage of whole zone (not in comparison with league average)
        copied_df['LOC_ZONE_PERCENTAGE'] = per_zone_percentage
        # Scaled count of shots and count of shots per bin
        copied_df['LOC_COUNTS'] = shot_locations_counts
        copied_df['LOC_RAW_COUNTS'] = raw_counts

        return copied_df

    def plot_frequency_legend(self):
        """
        Method which is in charge of plotting the frequency
        """
        # Frequency
        plt.text(x=self.less_frequent_string[0], y=self.less_frequent_string[1], s=self.less_frequent_string[2],
                 rotation=self.less_frequent_string[3], color=self.text_color, fontsize=self.font_size)
        for size_item in self.size_legend:
            plt.scatter(x=size_item[0], y=size_item[1], s=self.marker_size_legend * self.multiplier *
                        size_item[2], c=self.text_color, marker=self.marker)
        plt.text(x=self.more_frequent_string[0], y=self.more_frequent_string[1], s=self.more_frequent_string[2],
                 rotation=self.more_frequent_string[3], color=self.text_color, fontsize=self.font_size)

    def plot_efficiency_legend(self):
        """
        Method which is in charge of plotting the efficiency legend on the shotchart for some NBA player.
        """
        # Efficiency
        plt.text(x=self.comparison_string[0], y=self.comparison_string[1], s=self.comparison_string[2],
                 color=self.text_color, fontsize=self.font_size)
        plt.text(x=self.below_average_string[0], y=self.below_average_string[1], s=self.below_average_string[2],
                 rotation=self.below_average_string[3], color=self.text_color, fontsize=self.font_size)
        for color_item in self.color_legend:
            plt.scatter(x=color_item[0], y=color_item[1], s=self.marker_color_legend * self.multiplier,
                        c=color_item[2], marker=self.marker)
        plt.text(x=self.above_average_string[0], y=self.above_average_string[1], s=self.above_average_string[2],
                 rotation=self.above_average_string[3], color=self.text_color, fontsize=self.font_size)

    def plot_shotchart(self, title, image_path=None, is_plot_for_response=False):
        """
        Method which is in charge of plotting the shotchart. It creates the binned data first and plots that data.

        :param title: Title of the chart.
        :param image_path: Path of the file, used to save the shot chart.
        :param is_plot_for_response: If image should be plotted to response then the buffer is returned.
        :return Returns nothing, but if is_plot_for_response set to True returns buffer with plot which can be used
        for plotting to response
        """
        binned_df = self.create_bins()
        plt.figure(figsize=(self.figure_size, self.figure_size), dpi=80)
        # colors_dict = {0:'red', 1:'green'}

        # LOC_PERCENTAGE -> total perc
        # PCT_LEAGUE_AVG_COMPARISON -> comparison per bins
        # PCT_LEAGUE_COMPARISON_ZONE -> comparison per zones only
        # LOC_X, LOC_Y -> real locs
        # BIN_LOC_X, BIN_LOC_Y -> binned locations
        plt.scatter(x=binned_df.BIN_LOC_X, y=binned_df.BIN_LOC_Y, marker=self.marker,
                    s=binned_df.LOC_COUNTS * self.multiplier, c=binned_df.PCT_LEAGUE_COMPARISON_ZONE,
                    cmap=self.cmap, linewidths=1.0)
        # Plotting frequency
        self.plot_frequency_legend()

        # Plotting efficiency
        self.plot_efficiency_legend()

        # Changing court color
        plt.gca().set_facecolor(self.court_color)
        self.draw_court()

        # plt.xticks(np.arange(-250, 252, 16.6667))  # for sanity check
        # plt.yticks(np.arange(-48.5, 490, 16.6667))
        # Removing ticks
        plt.xticks([])
        plt.yticks([])

        # Title
        plt.title(title, size=self.title_font)

        # Drawing court

        plt.xlim(-252, 252)
        plt.ylim(-65, 424)

        # Plotting bragging rights
        plt.text(x=-220, y=-58, s="github.com/danchyy/nba_shotcharts", color=self.text_color, fontsize=self.font_size)
        # Plotting the data owner
        plt.text(x=170, y=-58, s="Data: nba.com", color=self.text_color, fontsize=self.font_size)

        plt.draw()
        # Saving figure
        if image_path is not None and self.should_save_image:
            # Bbox_inches removes things that make image ugly
            plt.savefig(image_path, dpi=80, bbox_inches='tight')

        if is_plot_for_response:
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches="tight")
            return buf

        plt.show()


if __name__ == '__main__':
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

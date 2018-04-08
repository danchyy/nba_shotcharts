import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
from matplotlib.patches import Circle, Rectangle, Arc

class Shotchart:

    def __init__(self, shotchart_data, league_average_data, line_colors="black", lw=3, outer_lines=True):
        # df, bin_number_x = 30, bin_number_y = 300 / (500.0 / 30.0), max_size_given = None, league_average = None,
        # width = 500, height = 300, norm_x = 250, norm_y = 48
        self.shotchart_data = shotchart_data
        self.league_average = league_average_data
        self.line_colors = line_colors
        self.outer_lines = outer_lines
        self.bin_number_x = 30.0
        self.width = 500.0
        self.height = 300.0
        self.bin_number_y = self.height / (self.width/ self.bin_number_x)
        self.max_size_given = None
        self.norm_x = 250
        self.norm_y = 48
        self.color = line_colors
        self.lw = lw
        self.outer_lines = outer_lines

        self.cmap = sns.blend_palette(colors=["#4159E1", "#B0E0E6", "#FFFF99", "#EF3330", "#AB2020"], as_cmap=True)
        self.court_color = '#363F48'

    # Amazing function by Bradley Fay for plotting the nba court
    # source: https://github.com/bradleyfay/py-Goldsberry/blob/master/docs/Visualizing%20NBA%20Shots%20with%20py-Goldsberry.ipynb
    def draw_court(self, ax=None, color=self.color, lw=2, outer_lines=False):
        """
        Method which is used for drawing the court lines on shotchart image.
        :param color: Color of the lines
        :param lw: Width of the lines
        :param outer_lines: Whether outer lines should be plotted
        :return: axes
        """
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()

        # Create the various parts of an NBA basketball court

        # Create the basketball hoop
        # Diameter of a hoop is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

        # Create backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

        # The paint
        # Create the outer box 0f the paint, width=16ft, height=19ft
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                              fill=False)
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                              fill=False)

        # Create free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                             linewidth=lw, color=color, fill=False)
        # Create free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                                linewidth=lw, color=color, linestyle='dashed')
        # Restricted Zone, it is an arc with 4ft radius from center of the hoop
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                         color=color)

        # Three point line
        # Create the side 3pt lines, they are 14ft long before they begin to arc
        corner_three_a = Rectangle((-220, -47.5), 0, 138, linewidth=lw,
                                   color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 138, linewidth=lw, color=color)
        # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
        # I just played around with the theta values until they lined up with the
        # threes
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                        color=color)

        # Center Court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                               linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                               linewidth=lw, color=color)

        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                          bottom_free_throw, restricted, corner_three_a,
                          corner_three_b, three_arc, center_outer_arc,
                          center_inner_arc]

        if outer_lines:
            # Draw the half court line, baseline and side out bound lines
            outer_lines = Rectangle((-250, -48), 500, 470, linewidth=lw,
                                    color=color, fill=False)
            court_elements.append(outer_lines)

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax


    def create_bins(self, df, bin_number_x=30, bin_number_y=300 / (500.0 / 30.0), max_size_given=None, league_average=None,
                    width=500, height=300, norm_x=250, norm_y=48):
        x_bins, y_bins = [], []
        copied_df = df.copy()
        keys = []
        location_counts, location_made = {}, {}
        locations_shots = {}  # real locations of shots which will be connected to bins and later arithmetic middle will
        # be found
        bin_size_x = width / float(bin_number_x)
        bin_size_y = height / float(bin_number_y)
        locations_annotated = []
        zones_counts, zones_made = {}, {}

        if bin_number_x < 20:
            multiplier = 1
        elif bin_number_x <= 25:
            multiplier = 1.5
        elif bin_number_x <= 30:
            multiplier = 2
        elif bin_number_x <= 45:
            multiplier = 3
        else:
            multiplier = 4
        if max_size_given is None:
            max_size = float(multiplier * bin_size_x * bin_size_y)
        else:
            max_size = float(max_size_given)

        restricted_area_keys = []

        for i in range(len(df)):
            x_shot_orig, y_shot_orig = df.iloc[i].LOC_X, df.iloc[i].LOC_Y
            x_shot = x_shot_orig + norm_x  # to put minimum to zero
            y_shot = y_shot_orig + norm_y  # to put minimum to zero (.5 is lacking, but just so i can be working with integers)

            # bin_index = (x_shot / w) * bin_size
            curr_x_bin = 0 if x_shot == 0 else int((x_shot / float(width)) * bin_number_x)
            curr_y_bin = 0 if y_shot == 0 else int((y_shot / float(height)) * bin_number_y)

            # x_bins.append(curr_bin_x_coord)
            # y_bins.append(curr_bin_y_coord)

            key = (curr_x_bin, curr_y_bin)

            if df.iloc[i].SHOT_ZONE_BASIC == "Restricted Area":
                restricted_area_keys.append(key)

            keys.append(key)
            if key in location_counts:
                location_counts[key] = location_counts[key] + 1
            else:
                location_counts[key] = 1

            if key in location_made:
                location_made[key] = location_made[key] + df.iloc[i].SHOT_MADE_FLAG
            else:
                location_made[key] = df.iloc[i].SHOT_MADE_FLAG

            if key in locations_shots:
                locations_shots[key].append((x_shot_orig, y_shot_orig))
            else:
                locations_shots[key] = [(x_shot_orig, y_shot_orig)]

            basic_shot_zone, shot_zone_area = df.iloc[i].SHOT_ZONE_BASIC, df.iloc[i].SHOT_ZONE_AREA
            zone_dist = df.iloc[i].SHOT_ZONE_RANGE
            area_code = shot_zone_area.split("(")[1].split(")")[0]
            if "3" in basic_shot_zone:
                locations_annotated.append("3" + area_code)
            elif "Paint" in basic_shot_zone:
                locations_annotated.append("P" + area_code + zone_dist[0])
            elif "Mid" in basic_shot_zone:
                locations_annotated.append("M" + area_code + zone_dist[0])
            else:
                locations_annotated.append("R" + area_code)

            zone_key = (basic_shot_zone, shot_zone_area, zone_dist)
            if zone_key not in zones_counts:
                zones_counts[zone_key] = 1
            else:
                zones_counts[zone_key] = zones_counts[zone_key] + 1

            if df.iloc[i].SHOT_MADE_FLAG:
                if zone_key not in zones_made:
                    zones_made[zone_key] = 1
                else:
                    zones_made[zone_key] = zones_made[zone_key] + 1

        shot_locations_percentage = []  # percentage in given bin
        shot_locations_counts = []
        raw_counts = []
        key_x, key_y = [], []
        league_avg_comp = []
        plot_x, plot_y = [], []
        per_zone_percentage = []

        restricted_area, non_ra = [], []
        # Finding maximum occurrence out of restricted area
        for key in location_counts:
            if key not in restricted_area_keys:
                if location_counts[key] not in non_ra:
                    non_ra.append(location_counts[key])
            else:
                restricted_area.append((location_counts[key], key))

        sorted_non_ra = sorted(non_ra)
        max_out_of_restricted, second_biggest = float(sorted_non_ra[-1]), float(sorted_non_ra[-2])
        found_pairs = []
        binned_found = []

        for j in range(len(df)):
            key = keys[j]
            shot_percent = float(location_made[key]) / location_counts[key]
            # shot_percent = np.clip(shot_percent, 0.3, 0.7)
            shot_locations_percentage.append(shot_percent * 100)
            is_restricted = df.iloc[j].SHOT_ZONE_BASIC == "Restricted Area"
            if league_average is not None:
                shot_zone_basic, shot_zone_area = df.iloc[j].SHOT_ZONE_BASIC, df.iloc[j].SHOT_ZONE_AREA
                distance = df.iloc[j].SHOT_ZONE_RANGE
                zone_key = (shot_zone_basic, shot_zone_area, distance)
                if zone_key not in zones_made:
                    zone_percent = 0.0
                else:
                    zone_percent = float(zones_made[zone_key]) / float(zones_counts[zone_key])
                avg_percentage = league_average.loc[(league_average.SHOT_ZONE_BASIC == shot_zone_basic) & \
                                                    (league_average.SHOT_ZONE_AREA == shot_zone_area) & \
                                                    (league_average.SHOT_ZONE_RANGE == distance)].FG_PCT.iloc[0]
                league_avg_comp.append(np.clip((shot_percent - avg_percentage) * 100, -20, 20))
                if is_restricted:
                    per_zone_percentage.append(np.clip((shot_percent - avg_percentage) * 100, -20, 20))
                else:
                    per_zone_percentage.append(np.clip((zone_percent - avg_percentage) * 100, -20, 20))

            if is_restricted:
                # Debug it
                value_to_scale = max_out_of_restricted
                if location_counts[key] < max_out_of_restricted:
                    value_to_scale = second_biggest
                shot_locations_counts.append(float(value_to_scale) / max_out_of_restricted * max_size)
            else:
                value_to_scale = location_counts[key]
                if value_to_scale >= second_biggest:
                    value_to_scale = second_biggest
                shot_locations_counts.append(float(value_to_scale) / second_biggest * max_size)

            # shot_locations_counts.append( location_counts[key] / max_shots_at_location * max_size )
            raw_counts.append(location_counts[key])

            all_x_locs = [x_loc for x_loc, y_loc in locations_shots[key]]
            all_y_locs = [y_loc for x_loc, y_loc in locations_shots[key]]

            # binned_x, binned_y = np.mean(all_x_locs), np.mean(all_y_locs)

            x_bin, y_bin = key[0], key[1]
            binned_x = ((x_bin * float(width)) / bin_number_x + ((x_bin + 1) * float(width)) / bin_number_x) / 2 - norm_x
            binned_y = ((y_bin * float(height)) / bin_number_y + ((y_bin + 1) * float(height)) / bin_number_y) / 2 - norm_y

            if (binned_x, binned_y) not in binned_found:
                x_bins.append(binned_x)
                y_bins.append(binned_y)
                binned_found.append((binned_x, binned_y))
            else:
                x_bins.append(0)
                y_bins.append(-100)

            if location_counts[key] > 1:
                if (binned_x, binned_y) not in found_pairs:
                    plot_x.append(binned_x)
                    plot_y.append(binned_y)
                    found_pairs.append((binned_x, binned_y))
                else:
                    plot_x.append(0)
                    plot_y.append(-100)
            else:
                plot_x.append(df.iloc[j].LOC_X)
                plot_y.append(df.iloc[j].LOC_Y)

            key_x.append(key[0])
            key_y.append(key[1])

        copied_df['BIN_LOC_X'] = x_bins
        copied_df['BIN_LOC_Y'] = y_bins
        if league_average is not None:
            copied_df['PCT_LEAGUE_AVG_COMPARISON'] = league_avg_comp
            copied_df['PCT_LEAGUE_COMPARISON_ZONE'] = per_zone_percentage
        copied_df['LOC_PERCENTAGE'] = shot_locations_percentage
        copied_df['LOC_COUNTS'] = shot_locations_counts
        copied_df['LOC_RAW_COUNTS'] = raw_counts
        copied_df['BIN_X'] = key_x
        copied_df['BIN_Y'] = key_y
        copied_df['PLOT_X'] = plot_x
        copied_df['PLOT_Y'] = plot_y
        copied_df['LOCATION_CODE'] = locations_annotated

        return copied_df

    def plot_shotchart(self, title="Random title"):
        binned_df = self.create_bins(self.shotchart_data, league_average=self.league_average)
        fig = plt.figure(figsize=(16, 16))
        # colors_dict = {0:'red', 1:'green'}


        # LOC_PERCENTAGE -> total perc
        # PCT_LEAGUE_AVG_COMPARISON -> comparison per bins
        # PCT_LEAGUE_COMPARISON_ZONE -> comparison per zones only
        # LOC_X, LOC_Y -> real locs
        # BIN_LOC_X, BIN_LOC_Y -> binned locations
        marker = 'H'
        paths = plt.scatter(x=binned_df.BIN_LOC_X, y=binned_df.BIN_LOC_Y, marker=marker, s=binned_df.LOC_COUNTS,
                            c=binned_df.PCT_LEAGUE_COMPARISON_ZONE, cmap=self.cmap)


        # Frequency

        plt.text(x=-240, y=395, s="Less\nFrequent", rotation=-5, color="#E8E8FF")
        plt.scatter(x=-230, y=380, s=100, marker=marker, c="#E8E8FF")
        plt.scatter(x=-222, y=383, s=300, marker=marker, c="#E8E8FF")
        plt.scatter(x=-211, y=380, s=600, marker=marker, c="#E8E8FF")
        plt.scatter(x=-197, y=377, s=900, marker=marker, c="#E8E8FF")
        plt.scatter(x=-180, y=380, s=1400, marker=marker, c="#E8E8FF")
        plt.scatter(x=-158, y=375, s=2200, marker=marker, c="#E8E8FF")
        plt.scatter(x=-132, y=380, s=3200, marker=marker, c="#E8E8FF")
        plt.text(x=-140, y=350, s="More\nFrequent", rotation=5, color="#E8E8FF")

        # Efficiency

        plt.text(x=80, y=410, s="Comparison with league average percentage", color="#E8E8FF")
        plt.text(x=95, y=360, s="Below\nAverage", rotation=10, color="#E8E8FF")
        plt.scatter(x=130, y=377, s=900, marker=marker, c="#4159E1")
        plt.scatter(x=147, y=380, s=900, marker=marker, c="#B0E0E6")
        plt.scatter(x=163, y=377, s=900, marker=marker, c="#FFFF99")
        plt.scatter(x=180, y=380, s=900, marker=marker, c="#EF3330")
        plt.scatter(x=197, y=377, s=900, marker=marker, c="#AB2020")
        plt.text(x=195, y=390, s="Above\nAverage", rotation=-10, color="#E8E8FF")

        # Changing court color
        plt.gca().set_facecolor(self.court_color)
        curr_ax = plt.gca()

        # plt.xticks(np.arange(-250, 251, 20))
        # plt.yticks(np.arange(-50, 490, 20))
        # Removing ticks
        plt.xticks([])
        plt.yticks([])

        # Title
        plt.title(title, size=20)

        # Drawing court
        self.draw_court(outer_lines=self.outer_lines, lw=self.lw)
        plt.xlim(-251, 251)
        plt.ylim(-65, 423)

        plt.text(x=-220, y=-58, s="instagram.com/bballytics", color="#E8E8FF")
        plt.text(x=170, y=-58, s="Data: nba.com", color="#E8E8FF")

        # Colorbar
        """cax = fig.add_axes([0.7, 0.82, 0.2, 0.025])
        colorbar = plt.colorbar(mappable=paths, cax=cax, orientation='horizontal', format='%d%%')
        #colorbar = plt.colorbar(cax=cax, orientation='horizontal', format='%+d%%') # + is for positive percentage
        cax.set_xlabel("Comparison to league average percentages",
                    fontsize=12, labelpad=-60, color="#E2E2FF")
        colorbar.outline.set_visible(False)
        plt.setp(plt.getp(colorbar.ax.axes, 'xticklabels'), color="#E2E2FF", fontsize=10)
        """

        # Saving figure
        # plt.savefig('lebron.png', bbox_inches='tight')
        # colorbar.set_label('Comparison to league average percentages', color='#E2E2FF', size=16, coords=(1.5, 1.5))
        plt.show()
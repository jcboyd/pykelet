#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir, path
from pylab import *
import re


class Scenarios:

    # baseline
    H_H = {'name': 'Base. HEP', 'path': '../logs/baseline/H_H/'}
    H_HappC333 = {'name': 'Base. HEP app. 1/3CORA', 'path': '../logs/baseline/H_HappC333/'}
    H_HappC666 = {'name': 'Base. HEP app. 2/3CORA', 'path': '../logs/baseline/H_HappC666/'}
    H_HappC = {'name': 'Base. HEP app. CORA', 'path': '../logs/baseline/H_HappC/'}
    H_C = {'name': 'Base. CORA', 'path': '../logs/baseline/H_C/'}
    H_CH = {'name': 'Base. CORA + HEP', 'path': '../logs/baseline/H_CH/'}
    H_CappH = {'name': 'Base. CORA app. HEP', 'path': '../logs/baseline/H_CappH/'}
    S_H = {'name': 'Base. HEP', 'path': '../logs/baseline/S_H/'}
    S_HappC = {'name': 'Base. HEP app. C', 'path': '../logs/baseline/S_HappC/'}
    S_C = {'name': 'Base. CORA', 'path': '../logs/baseline/S_C/'}
    S_CH = {'name': 'Base. CORA + HEP', 'path': '../logs/baseline/S_CH/'}
    S_CappH = {'name': 'Base. CORA app. HEP', 'path': '../logs/baseline/S_CappH/'}

    # block
    H_H_area = {'name': 'Area', 'path': '../logs/block_shape/H_H_area/'}
    H_H_height = {'name': 'Height', 'path': '../logs/block_shape/H_H_height/'}
    H_H_width = {'name': 'Width', 'path': '../logs/block_shape/H_H_width/'}
    H_H_width_height = {'name': 'Height + Width', 'path': '../logs/block_shape/H_H_width+height/'}

    # dicts
    H_H_dicts = {'name': 'Dicts', 'path': '../logs/dicts/H_H_dicts/'}
    H_HappC_dicts = {'name': 'Dicts', 'path': '../logs/dicts/H_HappC_dicts/'}
    S_H_dicts = {'name': 'Dicts', 'path': '../logs/dicts/S_H_dicts/'}
    S_HappC_dicts = {'name': 'Dicts', 'path': '../logs/dicts/S_HappC_dicts/'}

    H_H_dicts_2 = {'name': 'Dicts +- 2', 'path': '../logs/dicts/H_H_dicts+-2/'}
    H_HappC_dicts_2 = {'name': 'Dicts +- 2', 'path': '../logs/dicts/H_HappC_dicts+-2/'}
    H_H_dicts_3 = {'name': 'Dicts +- 3', 'path': '../logs/dicts/H_H_dicts+-3/'}
    H_HappC_dicts_3 = {'name': 'Dicts +- 3', 'path': '../logs/dicts/H_HappC_dicts+-3/'}

    S_H_dicts_2 = {'name': 'Dicts  +- 2', 'path': '../logs/dicts/S_H_dicts+-2/'}
    S_HappC_dicts_2 = {'name': 'Dicts  +- 2', 'path': '../logs/dicts/S_HappC_dicts+-2/'}
    S_H_dicts_3 = {'name': 'Dicts  +- 3', 'path': '../logs/dicts/S_H_dicts+-3/'}
    S_HappC_dicts_3 = {'name': 'Dicts  +- 3', 'path': '../logs/dicts/S_HappC_dicts+-3/'}

    # dicts_stops
    H_H_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/H_H_dicts_stops/'}
    H_HappC_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/H_HappC_dicts_stops/'}
    S_H_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/S_H_dicts_stops/'}
    S_HappC_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/S_HappC_dicts_stops/'}

    H_H_dicts_stops_2 = {'name': 'Dicts + Stops +- 2', 'path': '../logs/dicts_stops/H_H_dicts_stops+-2/'}
    H_HappC_dicts_stops_2 = {'name': 'Dicts + Stops +- 2', 'path': '../logs/dicts_stops/H_HappC_dicts_stops+-2/'}
    H_H_dicts_stops_3 = {'name': 'Dicts + Stops +- 3', 'path': '../logs/dicts_stops/H_H_dicts_stops+-3/'}
    H_HappC_dicts_stops_3 = {'name': 'Dicts + Stops +- 3', 'path': '../logs/dicts_stops/H_HappC_dicts_stops+-3/'}

    S_H_dicts_stops_2 = {'name': 'Dicts +- 2', 'path': '../logs/dicts_stops/S_H_dicts_stops+-2/'}
    S_HappC_dicts_stops_2 = {'name': 'Dicts +- 2', 'path': '../logs/dicts_stops/S_HappC_dicts_stops+-2/'}
    S_H_dicts_stops_3 = {'name': 'Dicts +- 3', 'path': '../logs/dicts_stops/S_H_dicts_stops+-3/'}
    S_HappC_dicts_stops_3 = {'name': 'Dicts +- 3', 'path': '../logs/dicts_stops/S_HappC_dicts_stops+-3/'}

    # regularisation
    H_H_L20 = {'name': '$\sigma^2 = 0$', 'path': '../logs/regularisation/H_H_L2=0/'}
    H_H_L2em6 = {'name': '$\sigma^2 = \exp\{-6\}$', 'path': '../logs/regularisation/H_H_L2=e-6/'}
    H_H_L2em5 = {'name': '$\sigma^2 = \exp\{-5\}$', 'path': '../logs/regularisation/H_H_L2=e-5/'}
    H_H_L2em4 = {'name': '$\sigma^2 = \exp\{-4\}$', 'path': '../logs/regularisation/H_H_L2=e-4/'}
    H_H_L2em3 = {'name': '$\sigma^2 = \exp\{-3\}$', 'path': '../logs/regularisation/H_H_L2=e-3/'}

    # levenshtein
    S_H_Lev01 = {'name': 'Lev. (0.1)', 'path': '../logs/levenshtein/S_H_Lev0.1/'}
    S_H_Lev0104 = {'name': 'Lev. (0.1, 0.4)', 'path': '../logs/levenshtein/S_H_Lev0.1+0.4/'}
    S_H_Lev02 = {'name': 'Lev. (0.2)', 'path': '../logs/levenshtein/S_H_Lev0.2/'}
    S_H_Lev04 = {'name': 'Lev. (0.4)', 'path': '../logs/levenshtein/S_H_Lev0.4/'}
    S_H_Lev005 = {'name': 'Lev. (0.05)', 'path': '../logs/levenshtein/S_H_Lev0.05/'}
    S_H_Lev08 = {'name': 'Lev. (0.8)', 'path': '../logs/levenshtein/S_H_Lev0.8/'}
    S_H_LevAll = {'name': 'Lev. (All)', 'path': '../logs/levenshtein/S_H_LevAll/'}

    # classes
    S_H_class_binary = {'name': 'Bin.', 'path': '../logs/classes/S_H_class_binary/'}
    S_H_class_decimal = {'name': 'Dec. (round down)', 'path': '../logs/classes/S_H_class_decimal/'}
    S_H_class_decimal_round = {'name': 'Dec. (round nearest)', 'path': '../logs/classes/S_H_class_decimal_round/'}
    S_H_class_20_point = {'name': 'Dec. (20 point)', 'path': '../logs/classes/S_H_class_20_point/'}

    S_H_class_binary_only = {'name': 'Bin. only', 'path': '../logs/classes/S_H_class_binary_only/'}
    S_H_class_decimal_only = {'name': 'Dec. only', 'path': '../logs/classes/S_H_class_decimal_only/'}
    S_H_class_baseline_none = {'name': 'Baseline none', 'path': '../logs/classes/S_H_baseline_no_classes/'}

    S_H_5 = {'name': '+5', 'path': '../logs/extension/S_H+5/'}
    S_H_10 = {'name': '+10', 'path': '../logs/extension/S_H+10/'}
    S_H_15 = {'name': '+15', 'path': '../logs/extension/S_H+15/'}
    S_H_20 = {'name': '+20', 'path': '../logs/extension/S_H+20/'}


class Category:

    TOKEN = 0
    FIELD = 1
    INSTANCE = 2
    CONFUSION = 3
    CONFUSION_AVE = 4


class Stat:

    ACCURACY = 0
    PRECISION = 1
    RECALL = 2
    F1 = 3


class Scenario:

    def __init__(self, name):
        self.name = name
        self.iterations = {}

    def add_iteration(self, iteration):
        self.iterations[iteration.id] = iteration


class Iteration:

    def __init__(self, id):
        self.id = id
        self.fields = {}

    def add_field(self, field):
        self.fields[field.name] = field


class Field:

    def __init__(self, name, accuracy, recall, precision, f1):
        self.name = name
        self.accuracy = accuracy
        self.recall = recall
        self.precision = precision
        self.f1 = f1


def plotBoxPlot(data, scenarios, field, theme):
    """
    Adapted http://matplotlib.org/examples/pylab_examples/boxplot_demo2.html
    """
    numDists = len(data)
    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.set_window_title('A Boxplot Example')
    plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)

    bp = plt.boxplot(data, notch=0, sym='+', vert=1, whis=1.5)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                   alpha=0.5)

    # Hide these grid behind plot objects
    ax1.set_axisbelow(True)
    ax1.set_title('%s: 5-Fold Cross Validation of %s (F1)' % (theme,
                  field.capitalize()), fontsize=16)
    ax1.set_xlabel('Scenario', fontsize=14)
    ax1.set_ylabel('F1', fontsize=14)

    # Now fill the boxes with desired colors
    boxColors = ['royalblue', 'royalblue']
    numBoxes = numDists
    medians = range(numBoxes)
    for i in range(numBoxes):
        box = bp['boxes'][i]
        boxX = []
        boxY = []
        for j in range(5):
            boxX.append(box.get_xdata()[j])
            boxY.append(box.get_ydata()[j])
        boxCoords = zip(boxX, boxY)
        # Alternate between Dark Khaki and Royal Blue
        k = i % 2
        boxPolygon = Polygon(boxCoords, facecolor=boxColors[k])
        ax1.add_patch(boxPolygon)
        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        medianX = []
        medianY = []
        for j in range(2):
            medianX.append(med.get_xdata()[j])
            medianY.append(med.get_ydata()[j])
            plt.plot(medianX, medianY, 'k')
            medians[i] = medianY[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        plt.plot([np.average(med.get_xdata())], [np.average(data[i])],
                 color='w', marker='o', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes+0.5)
    top = min(100, max([max(x) for x in data])*1.05)
    bottom = min([min(x) for x in data])*0.99
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=scenarios)
    plt.setp(xtickNames, rotation=0, fontsize=12)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    means = ['$\mu$: %s' % np.round(np.average(data[i]), 2)
             for i in range(len(data))]
    stds = ['$\sigma$: %s' % np.round(np.std(data[i]), 2)
            for i in range(len(data))]

    plt.plot(np.arange(numBoxes) + 1,
             [np.round(np.average(data[i]), 2) for i in range(len(data))],
             marker='o', linestyle='--', color='darkgrey')

    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top-((top-bottom)*0.05), means[tick],
                 horizontalalignment='center',
                 size=12,
                 color='black')  # boxColors[k])

        ax1.text(pos[tick], top-((top-bottom)*0.1), stds[tick],
                 horizontalalignment='center',
                 size=12,
                 color='black')  # boxColors[k])

    # Finally, add a basic legend
    # plt.figtext(0.80, 0.08,  str(N) + ' Random Numbers',
    #             backgroundcolor=boxColors[0], color='black', weight='roman',
    #             size='x-small')
    # plt.figtext(0.80, 0.045, 'IID Bootstrap Resample',
    #             backgroundcolor=boxColors[1],
    #             color='white', weight='roman', size='x-small')
    # plt.figtext(0.80, 0.015, '*', color='white', backgroundcolor='silver',
    #             weight='roman', size='medium')
    # plt.figtext(0.815, 0.013, ' Average Value', color='black', weight='roman',
    #             size='x-small')
    # plt.show()
    # ax1.set_axis_bgcolor((0.98, 0.98, 0.98))
    # fig.patch.set_facecolor((0.9, 0.9, 0.9))

    # ax1.minorticks_on()
    # ax1.yaxis.grid(True)
    # ax1.yaxis.grid(True, 'minor')
    # grid(b=True, which='minor', linestyle='--')

    plt.tight_layout()
    plt.savefig('/home/joseph/Desktop/%s.pdf' % (field))


if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))
    n_folds = 5
    scenarios = []

    theme = 'Levenshtein'

    directories = [Scenarios.S_H_Lev02['path'],
                   Scenarios.S_H_Lev08['path'],
                   Scenarios.S_H_Lev005['path'],
                   Scenarios.S_H_Lev04['path'],
                   Scenarios.S_H_Lev01['path'],
                   Scenarios.S_H_Lev0104['path'],
                   Scenarios.S_H_LevAll['path']]

    names = [Scenarios.S_H_Lev02['name'],
             Scenarios.S_H_Lev08['name'],
             Scenarios.S_H_Lev005['name'],
             Scenarios.S_H_Lev04['name'],
             Scenarios.S_H_Lev01['name'],
             Scenarios.S_H_Lev0104['name'],
             Scenarios.S_H_LevAll['name']]

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC333['path'],
    #                Scenarios.H_HappC666['path'],
    #                Scenarios.H_HappC['path']]

    # names = [Scenarios.H_H['name'],
    #          Scenarios.H_HappC333['name'],
    #          Scenarios.H_HappC666['name'],
    #          Scenarios.H_HappC['name']]

    # theme = 'Regularisation'

    # directories = [Scenarios.H_H_L20['path'],
    #                Scenarios.H_H_L2em6['path'],
    #                Scenarios.H_H_L2em5['path'],
    #                Scenarios.H_H_L2em4['path'],
    #                Scenarios.H_H_L2em3['path']]

    # names = [Scenarios.H_H_L20['name'],
    #          Scenarios.H_H_L2em6['name'],
    #          Scenarios.H_H_L2em5['name'],
    #          Scenarios.H_H_L2em4['name'],
    #          Scenarios.H_H_L2em3['name']]

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC['path'],
    #                Scenarios.H_HappC_dicts['path'],
    #                Scenarios.H_HappC_dicts_stops['path']]

    # directories = [Scenarios.S_H['path'],
    #                Scenarios.S_H_class_decimal['path'],
    #                Scenarios.S_H_LevAll['path']]

    # names = [Scenarios.S_H['name'],
    #          Scenarios.S_H_class_decimal['name'],
    #          Scenarios.S_H_LevAll['name']]

    # directories = [Scenarios.S_H['path'],
    #                Scenarios.S_H_class_decimal['path'],
    #                Scenarios.S_H_LevAll['path']]

    # names = [Scenarios.S_H['name'],
    #          Scenarios.S_H_class_decimal['name'],
    #          Scenarios.S_H_LevAll['name']]

    # theme = 'Character Classes'

    # directories = [Scenarios.S_H_class_binary['path'],
    #                Scenarios.S_H_class_decimal_round['path'],
    #                Scenarios.S_H_class_binary_only['path'],
    #                Scenarios.S_H_class_decimal['path'],
    #                Scenarios.S_H_class_decimal_only['path'],
    #                Scenarios.S_H_class_20_point['path']]

    # names = [Scenarios.S_H_class_binary['name'],
    #          Scenarios.S_H_class_decimal_round['name'],
    #          Scenarios.S_H_class_binary_only['name'],
    #          Scenarios.S_H_class_decimal['name'],
    #          Scenarios.S_H_class_decimal_only['name'],
    #          Scenarios.S_H_class_20_point['name']]

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_H_dicts['path'],
    #                Scenarios.H_H_dicts_stops['path']]

    # names = [Scenarios.H_H['name'],
    #          Scenarios.H_H_dicts['name'],
    #          Scenarios.H_H_dicts_stops['name']]

    # theme = 'Block Shape'

    # directories = [Scenarios.H_H_width_height['path'],
    #                Scenarios.H_H_area['path'],
    #                Scenarios.H_H_height['path'],
    #                Scenarios.H_H_width['path']]

    # names = [Scenarios.H_H_width_height['name'],
    #          Scenarios.H_H_area['name'],
    #          Scenarios.H_H_height['name'],
    #          Scenarios.H_H_width['name']]

    # theme = 'Header Dicts'

    # directories = [Scenarios.H_H_dicts['path'],
    #                Scenarios.H_HappC_dicts['path'],
    #                Scenarios.H_H_dicts_2['path'],
    #                Scenarios.H_HappC_dicts_2['path'],
    #                Scenarios.H_H_dicts_3['path'],
    #                Scenarios.H_HappC_dicts_3['path']]

    # names = [Scenarios.H_H_dicts['name'],
    #          Scenarios.H_HappC_dicts['name'],
    #          Scenarios.H_H_dicts_2['name'],
    #          Scenarios.H_HappC_dicts_2['name'],
    #          Scenarios.H_H_dicts_3['name'],
    #          Scenarios.H_HappC_dicts_3['name']]

    # theme = 'Segmentation Dicts'

    # directories = [Scenarios.S_H_dicts['path'],
    #                Scenarios.S_HappC_dicts['path'],
    #                Scenarios.S_H_dicts_2['path'],
    #                Scenarios.S_HappC_dicts_2['path'],
    #                Scenarios.S_H_dicts_3['path'],
    #                Scenarios.S_HappC_dicts_3['path']]

    # names = [Scenarios.S_H_dicts['name'],
    #          Scenarios.S_HappC_dicts['name'],
    #          Scenarios.S_H_dicts_2['name'],
    #          Scenarios.S_HappC_dicts_2['name'],
    #          Scenarios.S_H_dicts_3['name'],
    #          Scenarios.S_HappC_dicts_3['name']]

    # theme = 'Header Baseline'

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC['path'],
    #                Scenarios.H_C['path'],
    #                Scenarios.H_CappH['path'],
    #                Scenarios.H_CH['path']]

    # names = [Scenarios.H_H['name'],
    #          Scenarios.H_HappC['name'],
    #          Scenarios.H_C['name'],
    #          Scenarios.H_CappH['name'],
    #          Scenarios.H_CH['name']]

    # theme = 'Segmentation Baseline'

    # directories = [Scenarios.S_H['path'],
    #                Scenarios.S_HappC['path'],
    #                Scenarios.S_C['path'],
    #                Scenarios.S_CappH['path'],
    #                Scenarios.S_CH['path']]

    # names = [Scenarios.S_H['name'],
    #          Scenarios.S_HappC['name'],
    #          Scenarios.S_C['name'],
    #          Scenarios.S_CappH['name'],
    #          Scenarios.S_CH['name']]

    # theme = 'Subsampling'

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC333['path'],
    #                Scenarios.H_HappC666['path'],
    #                Scenarios.H_HappC['path']]

    # names = [Scenarios.H_H['name'],
    #          Scenarios.H_HappC333['name'],
    #          Scenarios.H_HappC666['name'],
    #          Scenarios.H_HappC['name']]

    # theme = 'Header Dicts + Stops'

    # directories = [Scenarios.H_H_dicts_stops['path'],
    #                Scenarios.H_HappC_dicts_stops['path'],
    #                Scenarios.H_H_dicts_stops_2['path'],
    #                Scenarios.H_HappC_dicts_stops_2['path'],
    #                Scenarios.H_H_dicts_stops_3['path'],
    #                Scenarios.H_HappC_dicts_stops_3['path']]

    # names = [Scenarios.H_H_dicts_stops['name'],
    #          Scenarios.H_HappC_dicts_stops['name'],
    #          Scenarios.H_H_dicts_stops_2['name'],
    #          Scenarios.H_HappC_dicts_stops_2['name'],
    #          Scenarios.H_H_dicts_stops_3['name'],
    #          Scenarios.H_HappC_dicts_stops_3['name']]

    # theme = 'Segmentation Dicts + Stops'

    # directories = [Scenarios.S_H_dicts_stops['path'],
    #                Scenarios.S_HappC_dicts_stops['path'],
    #                Scenarios.S_H_dicts_stops_2['path'],
    #                Scenarios.S_HappC_dicts_stops_2['path'],
    #                Scenarios.S_H_dicts_stops_3['path'],
    #                Scenarios.S_HappC_dicts_stops_3['path']]

    # names = [Scenarios.S_H_dicts_stops['name'],
    #          Scenarios.S_HappC_dicts_stops['name'],
    #          Scenarios.S_H_dicts_stops_2['name'],
    #          Scenarios.S_HappC_dicts_stops_2['name'],
    #          Scenarios.S_H_dicts_stops_3['name'],
    #          Scenarios.S_HappC_dicts_stops_3['name']]

    # theme = 'Extensions'

    # directories = [Scenarios.S_H_5['path'],
    #                Scenarios.S_H_10['path'],
    #                Scenarios.S_H_15['path'],
    #                Scenarios.S_H_20['path']]

    # names = [Scenarios.S_H_5['name'],
    #          Scenarios.S_H_10['name'],
    #          Scenarios.S_H_15['name'],
    #          Scenarios.S_H_20['name']]

    # Load data
    for directory in directories:
        scenario = Scenario(names[directories.index(directory)])
        files = sorted(listdir(directory))
        for file in files:
            it = Iteration(files.index(file))
            f = open(directory + file)

            res = filter(bool, re.split(r'=====[\s\w-]+=====',
                                        f.read().strip('\n')))

            token_res = filter(bool, res[Category.TOKEN].split('\n'))[1:]
            token_res[-2] = token_res[-2]. \
                replace('all fields', '<micro>').strip('(micro average)')
            token_res[-1] = '<macro>\t' + \
                token_res[-1].strip('(macro average)')

            for row in token_res:
                row = filter(bool, row.split('\t'))

                label = row[0].strip('<>')
                data = map(lambda val: float(val), row[1:])

                f = Field(name=label,
                          accuracy=data[Stat.ACCURACY],
                          precision=data[Stat.PRECISION],
                          recall=data[Stat.RECALL],
                          f1=data[Stat.F1])

                it.add_field(f)
            scenario.add_iteration(it)
        scenarios.append(scenario)

    field = 'micro'

    # Plot data

    f1_data = []

    for s in scenarios:
        boxplot_data = []
        boxplot_data.append(s.iterations[0].fields[field].f1)
        boxplot_data.append(s.iterations[1].fields[field].f1)
        boxplot_data.append(s.iterations[2].fields[field].f1)
        boxplot_data.append(s.iterations[3].fields[field].f1)
        boxplot_data.append(s.iterations[4].fields[field].f1)
        f1_data.append(boxplot_data)

    plotBoxPlot(f1_data, [s.name for s in scenarios], field, theme)

    # titles_0 = [x.iterations[0].fields[field].f1 for x in scenarios]
    # titles_1 = [x.iterations[1].fields[field].f1 for x in scenarios]
    # titles_2 = [x.iterations[2].fields[field].f1 for x in scenarios]
    # titles_3 = [x.iterations[3].fields[field].f1 for x in scenarios]
    # titles_4 = [x.iterations[4].fields[field].f1 for x in scenarios]

    # averages = [(titles_0[i] +
    #              titles_1[i] +
    #              titles_2[i] +
    #              titles_3[i] +
    #              titles_4[i]) / n_folds for i in range(len(directories))]

    # figure()

    # grid(True)
    # title('%s (F1) : 5-Fold Cross Validation' % (field.capitalize()), fontsize=12)
    # plt.xlabel('Scenario', fontsize=12)
    # plt.ylabel('F1', fontsize=12)
    # gca().set_xticks(range(4))
    # yticks(fontsize=8)

    # boxplot(f1_data)

    # means = [np.mean(x) for x in f1_data]
    # scatter([1, 2, 3], means)

    # gca().set_xticklabels([s.name for s in scenarios], rotation='45', fontsize=10)

    # # plt.plot(range(len(scenarios)), titles_0, marker='o', color='b', linestyle=':', linewidth='1')
    # # plt.plot(range(len(scenarios)), titles_1, marker='o', color='b', linestyle=':', linewidth='1')
    # # plt.plot(range(len(scenarios)), titles_2, marker='o', color='b', linestyle=':', linewidth='1')
    # # plt.plot(range(len(scenarios)), titles_3, marker='o', color='b', linestyle=':', linewidth='1')
    # # plt.plot(range(len(scenarios)), titles_4, marker='o', color='b', linestyle=':', linewidth='1')
    # # plt.plot(range(len(scenarios)), averages, marker='o', color='r', linestyle='-', linewidth='2')

    # plt.tight_layout()

    # # show()
    # plt.savefig('/home/joseph/Desktop/%s.pdf' % (field))
    # plt.savefig(directory + '/../figs/subsampling/%s.pdf' % (field))

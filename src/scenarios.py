#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import listdir, path
from pylab import *
import re


class Scenarios:

    # baseline
    H_H = {'name': 'Baseline HEP', 'path': '../logs/baseline/H_H/'}
    H_HappC333 = {'name': 'Baseline HEP + 1/3CORA', 'path': '../logs/baseline/H_HappC333/'}
    H_HappC666 = {'name': 'Baseline HEP + 2/3CORA', 'path': '../logs/baseline/H_HappC666/'}
    H_HappC = {'name': 'Baseline HEP + CORA', 'path': '../logs/baseline/H_HappC/'}
    H_C = {'name': 'Baseline', 'path': '../logs/baseline/H_C/'}
    H_CH = {'name': 'Baseline', 'path': '../logs/baseline/H_CH/'}
    H_CappH = {'name': 'Baseline', 'path': '../logs/baseline/H_CappH/'}
    S_H = {'name': 'Baseline', 'path': '../logs/baseline/S_H/'}
    S_HappC = {'name': 'Baseline', 'path': '../logs/baseline/S_HappC/'}
    S_C = {'name': 'Baseline', 'path': '../logs/baseline/S_C/'}
    S_CH = {'name': 'Baseline', 'path': '../logs/baseline/S_CH/'}
    S_CappH = {'name': 'Baseline', 'path': '../logs/baseline/S_CappH/'}

    # dicts
    H_H_dicts = {'name': 'Dicts', 'path': '../logs/dicts/H_H_dicts/'}
    H_HappC_dicts = {'name': 'Dicts', 'path': '../logs/dicts/H_HappC_dicts/'}
    S_H_dicts = {'name': 'Dicts', 'path': '../logs/dicts/S_H_dicts/'}
    S_HappC_dicts = {'name': 'Dicts', 'path': '../logs/dicts/S_HappC_dicts/'}

    # dicts_stops
    H_H_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/H_H_dicts_stops/'}
    H_HappC_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/H_HappC_dicts_stops/'}
    S_H_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/S_H_dicts_stops/'}
    S_HappC_dicts_stops = {'name': 'Dicts + Stops', 'path': '../logs/dicts_stops/S_HappC_dicts_stops/'}

    # regularisation
    H_H_L20 = {'name': 'Regularisation', 'path': '../logs/regularisation/H_H_L2=0/'}
    H_H_L2em6 = {'name': 'Regularisation', 'path': '../logs/regularisation/H_H_L2=e-6/'}
    H_H_L2em5 = {'name': 'Regularisation', 'path': '../logs/regularisation/H_H_L2=e-5/'}
    H_H_L2em4 = {'name': 'Regularisation', 'path': '../logs/regularisation/H_H_L2=e-4/'}
    H_H_L2em3 = {'name': 'Regularisation', 'path': '../logs/regularisation/H_H_L2=e-3/'}

    # levenshtein
    S_H_Lev01 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.1/'}
    S_H_Lev0104 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.1+0.4/'}
    S_H_Lev02 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.2/'}
    S_H_Lev04 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.4/'}
    S_H_Lev005 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.05/'}
    S_H_Lev08 = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_Lev0.8/'}
    S_H_LevAll = {'name': 'Levenshtein', 'path': '../logs/levenshtein/S_H_LevAll/'}

    # levenshtein
    S_H_class_binary = {'name': 'Classes (binary)', 'path': '../logs/classes/S_H_class_binary/'}
    S_H_class_decimal = {'name': 'Classes (decimal)', 'path': '../logs/classes/S_H_class_decimal/'}


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


def plotBoxPlot(data, scenarios, field):
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
    ax1.set_title('%s (F1) : 5-Fold Cross Validation' % (field.capitalize()))
    ax1.set_xlabel('Scenario')
    ax1.set_ylabel('F1')

    # Now fill the boxes with desired colors
    boxColors = ['darkred', 'royalblue']
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
                 color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, numBoxes+0.5)
    top = 100
    bottom = min([min(x) for x in data])*0.99
    ax1.set_ylim(bottom, top)
    xtickNames = plt.setp(ax1, xticklabels=scenarios)
    plt.setp(xtickNames, rotation=45, fontsize=12)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    pos = np.arange(numBoxes) + 1
    means = ['$\mu$: %s' % np.round(np.average(data[i]), 2) for i in range(len(data))]  # [str(np.round(s, 2)) for s in medians]
    stds = ['$\sigma$: %s' % np.round(np.std(data[i]), 2) for i in range(len(data))]

    for tick, label in zip(range(numBoxes), ax1.get_xticklabels()):
        k = tick % 2
        ax1.text(pos[tick], top-((top-bottom)*0.05), means[tick],
                 horizontalalignment='center',
                 size=12,
                 color=boxColors[k])

        ax1.text(pos[tick], top-((top-bottom)*0.1), stds[tick],
                 horizontalalignment='center',
                 size=12,
                 color=boxColors[k])

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
    plt.tight_layout()
    plt.savefig('/home/joseph/Desktop/%s.pdf' % (field))


if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))
    n_folds = 5
    scenarios = []

    directories = [Scenarios.H_H['path'],
                   Scenarios.H_HappC333['path'],
                   Scenarios.H_HappC666['path'],
                   Scenarios.H_HappC['path']]

    names = [Scenarios.H_H['name'],
             Scenarios.H_HappC333['name'],
             Scenarios.H_HappC666['name'],
             Scenarios.H_HappC['name']]

    # directories = [Scenarios.H_H_L20['path'],
    #                Scenarios.H_H_L2em6['path'],
    #                Scenarios.H_H_L2em5['path'],
    #                Scenarios.H_H_L2em4['path'],
    #                Scenarios.H_H_L2em3['path']]

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

    plotBoxPlot(f1_data, [s.name for s in scenarios], field)

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

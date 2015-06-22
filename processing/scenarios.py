from os import listdir, path
from pylab import *
import re


class Scenarios:

    # baseline
    H_H = {'id': 0, 'path': '../logs/baseline/H_H/'}
    H_HappC333 = {'id': 1, 'path': '../logs/baseline/H_HappC333/'}
    H_HappC666 = {'id': 2, 'path': '../logs/baseline/H_HappC666/'}
    H_HappC = {'id': 3, 'path': '../logs/baseline/H_HappC/'}
    H_C = {'id': 4, 'path': '../logs/baseline/H_C/'}
    H_CH = {'id': 5, 'path': '../logs/baseline/H_CH/'}
    H_CappH = {'id': 6, 'path': '../logs/baseline/H_CappH/'}
    S_H = {'id': 7, 'path': '../logs/baseline/S_H/'}
    S_HappC = {'id': 8, 'path': '../logs/baseline/S_HappC/'}
    S_C = {'id': 9, 'path': '../logs/baseline/S_C/'}
    S_CH = {'id': 10, 'path': '../logs/baseline/S_CH/'}
    S_CappH = {'id': 11, 'path': '../logs/baseline/S_CappH/'}

    # dicts
    H_H_dicts = {'id': 12, 'path': '../logs/dicts/H_H_dicts/'}
    H_HappC_dicts = {'id': 13, 'path': '../logs/dicts/H_HappC_dicts/'}
    S_H_dicts = {'id': 14, 'path': '../logs/dicts/S_H_dicts/'}
    S_HappC_dicts = {'id': 15, 'path': '../logs/dicts/S_HappC_dicts/'}

    # dicts_stops
    H_H_dicts_stops = {'id': 16, 'path': '../logs/dicts_stops/H_H_dicts_stops/'}
    H_HappC_dicts_stops = {'id': 17, 'path': '../logs/dicts_stops/H_HappC_dicts_stops/'}
    S_H_stops = {'id': 18, 'path': '../logs/dicts_stops/S_H_dicts_stops/'}
    S_HappC_dicts_stops = {'id': 19, 'path': '../logs/dicts_stops/S_HappC_dicts_stops/'}

    # regularisation
    H_H_L20 = {'id': 20, 'path': '../logs/regularisation/H_H_L2=0/'}
    H_H_L2em6 = {'id': 21, 'path': '../logs/regularisation/H_H_L2=e-6/'}
    H_H_L2em5 = {'id': 22, 'path': '../logs/regularisation/H_H_L2=e-5/'}
    H_H_L2em4 = {'id': 23, 'path': '../logs/regularisation/H_H_L2=e-4/'}
    H_H_L2em3 = {'id': 24, 'path': '../logs/regularisation/H_H_L2=e-3/'}


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


if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))
    n_folds = 5
    scenarios = []

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC333['path'],
    #                Scenarios.H_HappC666['path'],
    #                Scenarios.H_HappC['path']]

    # directories = [Scenarios.H_H_L20['path'],
    #                Scenarios.H_H_L2em6['path'],
    #                Scenarios.H_H_L2em5['path'],
    #                Scenarios.H_H_L2em4['path'],
    #                Scenarios.H_H_L2em3['path']]

    # directories = [Scenarios.H_H['path'],
    #                Scenarios.H_HappC['path'],
    #                Scenarios.H_HappC_dicts['path'],
    #                Scenarios.H_HappC_dicts_stops['path']]

    directories = [Scenarios.H_H['path'],
                   Scenarios.H_H_dicts_stops['path']]

    # Load data
    for directory in directories:
        scenario = Scenario(path.basename(directory[:-1]))
        files = sorted(listdir(directory))
        for file in files:
            it = Iteration(files.index(file))
            f = open(directory + file)

            res = filter(bool, re.split('===== Token-level results =====|' +
                                        '===== Field-level results =====|',
                                        f.read().strip('\n')))

            for row in filter(bool, res[Category.TOKEN].split('\n'))[1:-2]:
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

    field = 'title'

    # Plot data
    titles_0 = [x.iterations[0].fields[field].f1 for x in scenarios]
    titles_1 = [x.iterations[1].fields[field].f1 for x in scenarios]
    titles_2 = [x.iterations[2].fields[field].f1 for x in scenarios]
    titles_3 = [x.iterations[3].fields[field].f1 for x in scenarios]
    titles_4 = [x.iterations[4].fields[field].f1 for x in scenarios]

    averages = [(titles_0[i] +
                 titles_1[i] +
                 titles_2[i] +
                 titles_3[i] +
                 titles_4[i]) / n_folds for i in range(len(directories))]

    figure()
    grid(True)
    title('5-Fold Cross Validation over CORA sample size - %s' % (field.capitalize()))
    plt.xlabel('Scenario', fontsize=18)
    plt.ylabel('F1', fontsize=16)
    gca().set_xticks(range(4))
    gca().set_xticklabels([s.name for s in scenarios], rotation='90', fontsize=12)

    plt.plot(range(len(scenarios)), titles_0, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(len(scenarios)), titles_1, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(len(scenarios)), titles_2, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(len(scenarios)), titles_3, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(len(scenarios)), titles_4, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(len(scenarios)), averages, marker='.', color='b', linestyle='-', linewidth='2')

    plt.tight_layout()

    # show()
    plt.savefig('/home/joseph/Desktop/%s.pdf' % (field))
    # plt.savefig(directory + '/../figs/subsampling/%s.pdf' % (field))

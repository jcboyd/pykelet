from os import listdir, path
from pylab import *
import re


class Scenarios:

    H_H = {'id': 0, 'path': '../logs/baseline/H_H/'}
    H_HappC333 = {'id': 1, 'path': '../logs/baseline/H_HappC333/'}
    H_HappC666 = {'id': 2, 'path': '../logs/baseline/H_HappC666/'}
    H_HappC = {'id': 3, 'path': '../logs/baseline/H_HappC/'}


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

    directories = [Scenarios.H_H['path'],
                   Scenarios.H_HappC333['path'],
                   Scenarios.H_HappC666['path'],
                   Scenarios.H_HappC['path']]

    # Load data
    for directory in directories:
        scenario = Scenario(directory)
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

    field = 'collaboration'

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
    gca().set_xticklabels(['H_H', 'H_Happ1/3C', 'H_Happ2/3C', 'H_HappC'], rotation='0', fontsize=12)

    plt.plot(range(4), titles_0, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(4), titles_1, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(4), titles_2, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(4), titles_3, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(4), titles_4, marker='.', color='b', linestyle=':', linewidth='1')
    plt.plot(range(4), averages, marker='.', color='b', linestyle='-', linewidth='2')

    plt.tight_layout()

    # show()
    plt.savefig(directory + '/../figs/subsampling/cv_%s.pdf' % (field))

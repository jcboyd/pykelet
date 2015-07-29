from os import path, listdir
import shutil
import re

from sklearn.cross_validation import KFold
# from grobid import GrobidTrainer
from grobid_shell import GrobidTrainer
from numpy import array
from numpy.random import seed, shuffle
from matplotlib import cm
from bs4 import BeautifulSoup

from pylab import *


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


def getFileId(file_path):
    with open(file_path) as f:
        try:
            return BeautifulSoup(f, 'xml').fileDesc.attrs['xml:id']
        except:
            return False


def k_fold_cross_validation(grobid,
                            classpath_trainer,
                            model,
                            n_folds,
                            raw_folder):
    grobid_home = grobid + '/grobid-home'
    corpus = grobid + \
        '/grobid-trainer/resources/dataset/%s/corpus/tei/' % (model)
    evaluation = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation/tei/' % (model)
    evaluate_raw = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation/%s/' % (model,
                                                                 raw_folder)
    evaluation_set = [x[:x.find('.')] for x in listdir(evaluate_raw)]

    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home)

    # k-fold evaluation only for those raw files in evaluate/
    k_fold_set = array(filter(lambda x: (getFileId(corpus + x)
                       in evaluation_set or x.strip('.tei.xml')
                       in listdir(evaluate_raw)), listdir(corpus)))
    # perform reproducible random shuffling
    seed(0)
    shuffle(k_fold_set)
    folds = list(KFold(len(k_fold_set), n_folds=n_folds))

    for fold in folds:
        try:
            # move all fold files to evaluate folder
            for index in fold[1]:
                shutil.move(corpus + k_fold_set[index], evaluation)

            grobid_trainer.train(model)
            grobid_trainer.evaluate(model)
        except IOError, e:
            print 'Error: check folder configuration'
            print e
        finally:
            # move fold files back to corpus folder
            for index in fold[1]:
                shutil.move(evaluation + k_fold_set[index], corpus)


def read_output(name, log_path, fig_path):
    token_stats = []
    field_stats = []
    instance_stats = []
    confusions = []
    confusion_aves = []
    all_labels = set([])

    for file in listdir(log_path):
        f = open(log_path + '/' + file)
        results = filter(bool, re.split('===== Token-level results =====|' +
                                        '===== Field-level results =====|' +
                                        '===== Instance-level results =====|' +
                                        '===== Confusion matrix =====|' +
                                        '===== Confusion matrix ave. =====|' +
                                        '===== Top 5 Classifications =====',
                                        f.read().strip('\n')))
        f.close()

        tokens = {}

        for row in filter(bool, results[Category.TOKEN].split('\n'))[1:-2]:
            row = filter(bool, row.split('\t'))
            label = row[0].strip('<>')
            data = map(lambda val: float(val), row[1:])

            tokens[label] = {'Accuracy': data[Stat.ACCURACY],
                             'Precision': data[Stat.PRECISION],
                             'Recall': data[Stat.RECALL],
                             'F1': data[Stat.F1]}

        fields = {}

        for row in filter(bool, results[Category.FIELD].split('\n'))[1:-2]:
            row = filter(bool, row.split('\t'))
            label = row[0].strip('<>')
            data = map(lambda val: float(val), row[1:])

            fields[label] = {'Accuracy': data[Stat.ACCURACY],
                             'Precision': data[Stat.PRECISION],
                             'Recall': data[Stat.RECALL],
                             'F1': data[Stat.F1]}

        confusion = {}

        labels = [row.split('\t')[0].strip('<>') for row in
                  filter(bool, results[Category.CONFUSION].split('\n'))]

        counts = [map(lambda x: int(x), row.split('\t')[1:]) for row in
                  filter(bool, results[Category.CONFUSION].split('\n'))]

        for row_label in labels:
            count_dict = {}
            for col_label in labels:
                count_dict[col_label] = counts[
                    labels.index(row_label)][labels.index(col_label)]
            confusion[row_label] = count_dict
            all_labels.add(row_label)

        aves = [map(lambda x: round(float(x), 2), row.split('\t')[1:]) for row
                in filter(bool, results[Category.CONFUSION_AVE].split('\n'))]

        confusion_ave = {}

        for row_label in labels:
            ave_dict = {}
            for col_label in labels:
                ave_dict[col_label] = aves[
                    labels.index(row_label)][labels.index(col_label)]
            confusion_ave[row_label] = ave_dict

        token_stats.append(tokens)
        field_stats.append(fields)
        instance_stats.append(results[Category.INSTANCE])
        confusions.append(confusion)
        confusion_aves.append(confusion_ave)

    plot_box_plots('Token-level (F1) - %s' % (name), 'token-level',
                   token_stats, fig_path)
    plot_box_plots('Field-level (F1) - %s' % (name), 'field-level',
                   field_stats, fig_path)
    plot_confusion_matrix(name=name,
                          type='totals',
                          matrix=sum_confusions(all_labels, confusions),
                          path=fig_path,
                          show_counts=True)

    plot_confusion_matrix(name=name,
                          type='averages',
                          matrix=average_confusions(all_labels,
                                                    confusion_aves),
                          path=fig_path,
                          show_counts=True)


def sum_confusions(labels, confusion_matrices):
    sum_confusion = {}
    for row_label in labels:
        sum_confusion[row_label] = {}
        for col_label in labels:
            sum_confusion[row_label][col_label] = 0

    for matrix in confusion_matrices:
        for row_label in matrix.keys():
            for col_label in matrix[row_label].keys():
                sum_confusion[row_label][col_label] += \
                    matrix[row_label][col_label]

    return sum_confusion


def average_confusions(labels, confusion_matrices):
    average_confusion = {}
    for row_label in labels:
        average_confusion[row_label] = {}
        for col_label in labels:
            average_confusion[row_label][col_label] = 0

    for row_label in labels:  # matrix.keys():
        for col_label in labels:  # matrix[row_label].keys():
            for matrix in confusion_matrices:
                if row_label not in matrix.keys() or col_label not in matrix.keys():
                    continue
                average_confusion[row_label][col_label] += \
                    matrix[row_label][col_label]
            average_confusion[row_label][col_label] /= len(confusion_matrices)

    return average_confusion


def plot_confusion_matrix(name, type, matrix, path, show_counts):
    labels = [key.strip('<>') for key in sorted(matrix.keys())]
    counts = []
    proportions = []
    for label in labels:
        count_dict = matrix[label]
        row_counts = [count_dict[key] for key in sorted(count_dict.keys())]
        counts.append(row_counts)
        scaled_row_counts = [0 if sum(row_counts) == 0 else
                             1. * val / sum(row_counts) for val in row_counts]
        proportions.append(scaled_row_counts)

    figure()
    # Keep major ticks labeless
    xticks(range(len(labels)), [])
    yticks(range(len(labels)), [])
    # Place labels on minor ticks
    gca().set_xticks([x + 0.5 for x in range(len(labels))], minor=True)
    gca().set_xticklabels(labels, rotation='90', fontsize=10, minor=True)
    gca().set_yticks([y + 0.5 for y in range(len(labels))], minor=True)
    gca().set_yticklabels(labels[::-1], fontsize=10, minor=True)
    # Finally, hide minor tick marks...
    gca().tick_params('both', width=0, which='minor')

    pcolor(array(proportions[::-1]), cmap=cm.Blues)
    if show_counts:
        for y in range(len(counts)):
            for x in range(len(counts[y])):
                if counts[::-1][y][x] != 0:
                    text(x + 0.5, y + 0.5, counts[::-1][y][x],
                         fontsize=9,
                         horizontalalignment='center',
                         verticalalignment='center')

    grid(True)
    title('Confusion matrix - %s' % (name))
    plt.tight_layout()
    savefig(path + '/confusion_%s.pdf' % (type))
    close()


def plot_box_plots(name, file_name, stats, path):
    labels = set([])
    # Collect all labels
    for stats_dict in stats:
        for key in stats_dict.keys():
            labels.add(key)
    labels = sorted([label for label in labels])
    f1_data = []
    # Collect all data
    for label in labels:
        f1_data.append([stats_dict[label]['F1'] for stats_dict in
                        filter(lambda x: label in x.keys(), stats)])
    figure()
    boxplot(f1_data)

    xticks(range(1, len(labels) + 1), labels, rotation='90', fontsize=8)
    yticks(range(0, 120, 20), [0, 0.2, 0.4, 0.6, 0.8, 1.0], fontsize=8)
    title(name)
    plt.tight_layout()
    savefig(path + '/boxplot-' + file_name + '.pdf')
    close()


if __name__ == '__main__':

    n_folds = 5

    directory = path.dirname(path.realpath(__file__))
    jar = '/grobid-trainer/target/grobid-trainer-0.3.4-SNAPSHOT.jar'
    batches = directory + '/../batches/'

    for file in listdir(batches):
        if file.startswith('H'):
            k_fold_cross_validation(grobid=batches + file,
                                    classpath_trainer=batches + file + jar,
                                    model='header',
                                    n_folds=n_folds,
                                    raw_folder='headers')
        elif file.startswith('S'):
            k_fold_cross_validation(grobid=batches + file,
                                    classpath_trainer=batches + file + jar,
                                    model='segmentation',
                                    n_folds=n_folds,
                                    raw_folder='raw')

# k_fold_cross_validation.read_output('Segmentation (CORA)', '../logs/baseline/S_C', '../figs/baseline/S_C')
# k_fold_cross_validation.read_output('Segmentation (HEP)', '../logs/baseline/S_H', '../figs/baseline/S_H')
# k_fold_cross_validation.read_output('Segmentation (CORA + HEP)', '../logs/baseline/S_CH', '../figs/baseline/S_CH')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA)', '../logs/baseline/S_HappC', '../figs/baseline/S_HappC')
# k_fold_cross_validation.read_output('Segmentation (Cora app. HEP)', '../logs/baseline/S_CappH', '../figs/baseline/S_CappH')
# k_fold_cross_validation.read_output('Header (CORA)', '../logs/baseline/H_C', '../figs/baseline/H_C')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/baseline/H_H', '../figs/baseline/H_H')
# k_fold_cross_validation.read_output('Header (CORA + HEP)', '../logs/baseline/H_CH', '../figs/baseline/H_CH')
# k_fold_cross_validation.read_output('Header (HEP app. CORA)', '../logs/baseline/H_HappC', '../figs/baseline/H_HappC')
# k_fold_cross_validation.read_output('Header (Cora app. HEP)', '../logs/baseline/H_CappH', '../figs/baseline/H_CappH')
# k_fold_cross_validation.read_output('Header (HEP app. 1/3 CORA)', '../logs/baseline/H_HappC333', '../figs/baseline/H_HappC333')
# k_fold_cross_validation.read_output('Header (HEP app. 2/3 CORA)', '../logs/baseline/H_HappC666', '../figs/baseline/H_HappC666')

# k_fold_cross_validation.read_output('Segmentation (HEP)', '../logs/dicts/S_H_dicts', '../figs/dicts/S_H_dicts')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA)', '../logs/dicts/S_HappC_dicts', '../figs/dicts/S_HappC_dicts')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/dicts/H_H_dicts', '../figs/dicts/H_H_dicts')
# k_fold_cross_validation.read_output('Header (HEP app. CORA)', '../logs/dicts/H_HappC_dicts', '../figs/dicts/H_HappC_dicts')
# k_fold_cross_validation.read_output('Segmentation (HEP) +- 2', '../logs/dicts/S_H_dicts+-2', '../figs/dicts/S_H_dicts+-2')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA) +- 2', '../logs/dicts/S_HappC_dicts+-2', '../figs/dicts/S_HappC_dicts+-2')
# k_fold_cross_validation.read_output('Header (HEP) +- 2', '../logs/dicts/H_H_dicts+-2', '../figs/dicts/H_H_dicts+-2')
# k_fold_cross_validation.read_output('Header (HEP app. CORA) +- 2', '../logs/dicts/H_HappC_dicts+-2', '../figs/dicts/H_HappC_dicts+-2')
# k_fold_cross_validation.read_output('Segmentation (HEP) +- 3', '../logs/dicts/S_H_dicts+-3', '../figs/dicts/S_H_dicts+-3')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA) +- 3', '../logs/dicts/S_HappC_dicts+-3', '../figs/dicts/S_HappC_dicts+-3')
# k_fold_cross_validation.read_output('Header (HEP) +- 3', '../logs/dicts/H_H_dicts+-3', '../figs/dicts/H_H_dicts+-3')
# k_fold_cross_validation.read_output('Header (HEP app. CORA) +- 3', '../logs/dicts/H_HappC_dicts+-3', '../figs/dicts/H_HappC_dicts+-3')

# k_fold_cross_validation.read_output('Segmentation (HEP)', '../logs/dicts_stops/S_H_dicts_stops', '../figs/dicts_stops/S_H_dicts_stops')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA)', '../logs/dicts_stops/S_HappC_dicts_stops', '../figs/dicts_stops/S_HappC_dicts_stops')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/dicts_stops/H_H_dicts_stops', '../figs/dicts_stops/H_H_dicts_stops')
# k_fold_cross_validation.read_output('Header (HEP app. CORA)', '../logs/dicts_stops/H_HappC_dicts_stops', '../figs/dicts_stops/H_HappC_dicts_stops')
# k_fold_cross_validation.read_output('Segmentation (HEP) +- 2', '../logs/dicts_stops/S_H_dicts_stops+-2', '../figs/dicts_stops/S_H_dicts_stops+-2')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA) +- 2', '../logs/dicts_stops/S_HappC_dicts_stops+-2', '../figs/dicts_stops/S_HappC_dicts_stops+-2')
# k_fold_cross_validation.read_output('Header (HEP) +- 2', '../logs/dicts_stops/H_H_dicts_stops+-2', '../figs/dicts_stops/H_H_dicts_stops+-2')
# k_fold_cross_validation.read_output('Header (HEP app. CORA) +- 2', '../logs/dicts_stops/H_HappC_dicts_stops+-3', '../figs/dicts_stops/H_HappC_dicts_stops+-2')
# k_fold_cross_validation.read_output('Segmentation (HEP) +- 3', '../logs/dicts_stops/S_H_dicts_stops+-3', '../figs/dicts_stops/S_H_dicts_stops+-3')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA) +- 3', '../logs/dicts_stops/S_HappC_dicts_stops+-3', '../figs/dicts_stops/S_HappC_dicts_stops+-3')
# k_fold_cross_validation.read_output('Header (HEP) +- 3', '../logs/dicts_stops/H_H_dicts_stops+-3', '../figs/dicts_stops/H_H_dicts_stops+-3')
# k_fold_cross_validation.read_output('Header (HEP app. CORA) +- 3', '../logs/dicts_stops/H_HappC_dicts_stops+-3', '../figs/dicts_stops/H_HappC_dicts_stops+-3')

# k_fold_cross_validation.read_output('Header (HEP)', '../logs/regularisation/H_H_L2=0', '../figs/regularisation/H_H_L2=0')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/regularisation/H_H_L2=e-6', '../figs/regularisation/H_H_L2=e-6')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/regularisation/H_H_L2=e-5', '../figs/regularisation/H_H_L2=e-5')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/regularisation/H_H_L2=e-4', '../figs/regularisation/H_H_L2=e-4')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/regularisation/H_H_L2=e-3', '../figs/regularisation/H_H_L2=e-3')

# k_fold_cross_validation.read_output('Header (HEP)', '../logs/block_shape/H_H_area', '../figs/block_shape/H_H_area')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/block_shape/H_H_height', '../figs/block_shape/H_H_height')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/block_shape/H_H_width', '../figs/block_shape/H_H_width')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/block_shape/H_H_width+height', '../figs/block_shape/H_H_width+height')

# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/H_H_class_binary', '../figs/classes/H_H_class_binary')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/H_H_class_decimal', '../figs/classes/H_H_class_decimal')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_baseline_no_classes', '../figs/classes/S_H_baseline_no_classes')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_binary', '../figs/classes/S_H_class_binary')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_binary', '../figs/classes/S_H_class_binary')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_decimal', '../figs/classes/S_H_class_decimal')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_classes_decimal_only', '../figs/classes/S_H_classes_decimal_only')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_20_point', '../figs/classes/S_H_class_20_point')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_binary_only', '../figs/classes/S_H_class_binary_only')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_decimal_only', '../figs/classes/S_H_class_decimal_only')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/classes/S_H_class_decimal_round', '../figs/classes/S_H_class_decimal_round')

# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.1', '../figs/levenshtein/S_H_Lev0.1')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.1+0.4', '../figs/levenshtein/S_H_Lev0.1+0.4')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.2', '../figs/levenshtein/S_H_Lev0.2')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.4', '../figs/levenshtein/S_H_Lev0.4')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.05', '../figs/levenshtein/S_H_Lev0.05')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_Lev0.8', '../figs/levenshtein/S_H_Lev0.8')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/levenshtein/S_H_LevAll', '../figs/levenshtein/S_H_LevAll')

# k_fold_cross_validation.read_output('Header (HEP)', '../logs/extension/S_H+5', '../figs/extension/S_H+5')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/extension/S_H+10', '../figs/extension/S_H+10')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/extension/S_H+15', '../figs/extension/S_H+15')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/extension/S_H+20', '../figs/extension/S_H+20')

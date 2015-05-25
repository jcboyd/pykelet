from os import path, listdir
import shutil
import re

from sklearn.cross_validation import KFold
# from grobid import GrobidTrainer
from grobid_shell import GrobidTrainer
from numpy import array
from matplotlib import cm

from pylab import *


class Category:
    TOKEN = 0
    FIELD = 1
    INSTANCE = 2
    CONFUSION = 3


class Stat:
    ACCURACY = 0
    PRECISION = 1
    RECALL = 2
    F1 = 3


def k_fold_cross_validation(grobid,
                            classpath_trainer,
                            model,
                            n_folds,
                            evaluate_raw):
    grobid_home = grobid + '/grobid-home'
    corpus = grobid + \
        '/grobid-trainer/resources/dataset/%s/corpus/tei/' % (model)
    evaluation = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation/tei/' % (model)
    evaluate_raw = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation/%s/' % (model,
                                                                 evaluate_raw)

    evaluation_set = listdir(evaluate_raw)

    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home)
    # k-fold evaluation only for those raw files in evaluate
    k_fold_set = filter(lambda x: x.strip('.tei.xml') in evaluation_set,
                        listdir(corpus))
    folds = list(KFold(len(k_fold_set), n_folds=n_folds))

    i = 1

    for fold in folds:
        try:
            # move all fold files to evaluate folder
            for index in fold[1]:
                shutil.move(corpus + k_fold_set[index], evaluation)

            grobid_trainer.train(model)
            grobid_trainer.evaluate(model)
            i += 1
        except IOError:
            print 'Error: check folder configuration'
        finally:
            # move fold files back to corpus folder
            for index in fold[1]:
                shutil.move(evaluation + k_fold_set[index], corpus)


def read_output(name, log_path, fig_path):

    token_stats = []
    field_stats = []
    instance_stats = []

    for file in listdir(log_path):
        f = open(log_path + '/' + file)
        results = filter(bool, re.split('===== Token-level results =====|' +
                                        '===== Field-level results =====|' +
                                        '===== Instance-level results =====|' +
                                        '===== Confusion matrix =====',
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

        token_stats.append(tokens)
        field_stats.append(fields)
        instance_stats.append(results[Category.INSTANCE])

    plot_box_plots('Token-level (F1) - %s' % (name), 'token-level',
                   token_stats, fig_path)
    plot_box_plots('Field-level (F1) - %s' % (name), 'field-level',
                   field_stats, fig_path)
    # Currently just produce confusion on the last fold
    plot_confusion_matrix(id, confusion, fig_path)


def plot_confusion_matrix(name, confusion, path):
    labels = [key.strip('<>') for key in sorted(confusion.keys())]
    counts = []
    for label in labels:
        count_dict = confusion[label]
        row_counts = [count_dict[key] for key in sorted(count_dict.keys())]
        scaled_row_counts = [0 if sum(row_counts) == 0 else
                             1. * val / sum(row_counts) for val in row_counts]
        counts.append(scaled_row_counts)

    figure()
    xticks(range(len(labels)), labels, rotation='90', fontsize=8)
    yticks(range(len(labels)), labels[::-1], fontsize=8)
    pcolor(array(counts[::-1]), cmap=cm.Blues)  # , interpolation='nearest')
    grid(True)
    title('Confusion matrix - %s' % (name))
    plt.tight_layout()
    savefig(path + '/confusion.pdf')
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
    classpath = directory + \
        '/../grobid/grobid-trainer/target/grobid-trainer-0.3.4-SNAPSHOT.jar'
    batches = directory + '/../batches/'

    for file in listdir(batches):
        if file.startswith('H'):
            k_fold_cross_validation(grobid=batches + file,
                                    classpath_trainer=classpath,
                                    model='header',
                                    n_folds=n_folds,
                                    evaluate_raw='headers')
        elif file.startswith('S'):
            k_fold_cross_validation(grobid=batches + file,
                                    classpath_trainer=classpath,
                                    model='segmentation',
                                    n_folds=n_folds,
                                    evaluate_raw='raw')

# k_fold_cross_validation.read_output('Segmentation (HEP)', '../logs/logs_S_H', '../figs/figs_S_H')
# k_fold_cross_validation.read_output('Segmentation (CORA)', '../logs/logs_S_C', '../figs/figs_S_C')
# k_fold_cross_validation.read_output('Segmentation (CORA + HEP)', '../logs/logs_S_CH', '../figs/figs_S_CH')
# k_fold_cross_validation.read_output('Segmentation (HEP app. CORA)', '../logs/logs_S_HappC', '../figs/figs_S_HappC')
# k_fold_cross_validation.read_output('Segmentation (Cora app. HEP)', '../logs/logs_S_CappH', '../figs/figs_S_CappH')
# k_fold_cross_validation.read_output('Header (HEP)', '../logs/logs_H_H', '../figs/figs_H_H')
# k_fold_cross_validation.read_output('Header (CORA + HEP)', '../logs/logs_H_CH', '../figs/figs_H_CH')

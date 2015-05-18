from os import path, listdir
import shutil
import re

from sklearn.cross_validation import KFold
# from grobid import GrobidTrainer
from grobid_shell import GrobidTrainer

import numpy as np
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


def k_fold_cross_validation(grobid, classpath_trainer, model, n_folds):
    grobid_home = grobid + '/grobid-home'
    corpus = grobid + \
        '/grobid-trainer/resources/dataset/%s/corpus/tei/' % (model)
    evaluation = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation/tei/' % (model)

    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home)
    training_set = listdir(corpus)

    folds = list(KFold(len(training_set), n_folds=n_folds))

    i = 1

    for fold in folds:
        try:
            # move all fold files to evaluate folder
            for index in fold[1]:
                shutil.move(corpus + training_set[index], evaluation)

            grobid_trainer.train(model)
            grobid_trainer.evaluate(model)
            i += 1
        except IOError:
            print 'Error: check folder configuration'
        finally:
            # move fold files back to corpus folder
            for index in fold[1]:
                shutil.move(evaluation + training_set[index], corpus)


def read_output(log_path, fig_path):

    token_stats = []
    field_stats = []
    instance_stats = []
    labels = []

    for file in listdir(log_path):
        f = open(log_path + '/' + file)
        results = filter(bool, re.split('===== Token-level results =====|' +
                                        '===== Field-level results =====|' +
                                        '===== Instance-level results =====|' +
                                        '===== Confusion matrix =====',
                                        f.read().strip('\n')))
        f.close()

        tokens = np.matrix([map(lambda x:float(x),
                            filter(bool, row.split('\t'))[1:]) for row in
                            filter(bool, results[Category.TOKEN].split('\n'))
                            [1:-2]])

        fields = np.matrix([map(lambda x:float(x),
                            filter(bool, row.split('\t'))[1:]) for row in
                            filter(bool, results[Category.FIELD].split('\n'))
                            [1:-2]])

        confusion = filter(bool, results[Category.CONFUSION].split('\n'))

        labels = map(lambda x: x.strip('<>'),
                     [row.split('\t')[0] for row in confusion])

        counts = np.matrix([row.split('\t')[1:] for row in confusion])

        token_stats.append(tokens)
        field_stats.append(fields)
        instance_stats.append(results[Category.INSTANCE])

    aggregate_stats('Token-level', labels, token_stats, fig_path)
    aggregate_stats('Field-level', labels, field_stats, fig_path)
    plot_confusion_matrix(labels, counts, fig_path)


def plot_confusion_matrix(labels, counts, path):
    N = len(labels)
    ind = np.arange(N)
    width = 0.5

    for label in labels:
        figure()
        row = [int(val) for val in counts.tolist()[labels.index(label)]]
        bar(ind, row, width, color='r')
        ylabel('Counts')
        title('%s - Confusion' % (label.capitalize()))
        xticks(ind + width/2., labels, rotation='vertical')
        savefig(path + '/' + label + '.pdf')
        close()


def aggregate_stats(name, labels, stats, path):
    data = []

    for label in labels:
        data.append([matrix[labels.index(label), Stat.F1] for matrix in stats])

    figure()
    boxplot(data)
    xticks(range(len(labels) + 1)[1:], labels, rotation='45')
    title('%s - F1' % (name.capitalize()))
    savefig(path + "/confusion_" + name + '.pdf')


if __name__ == '__main__':

    batches = '/home/joseph/Desktop/Batches/'
    n_folds = 5

    directory = path.dirname(path.realpath(__file__))
    classpath = directory + \
        '/../grobid/grobid-trainer/target/grobid-trainer-0.3.4-SNAPSHOT.jar'

    for file in listdir(batches):
        if file.startswith('H'):
            k_fold_cross_validation(batches + file, classpath, 'header', n_folds)
        elif file.startswith('S'):
            k_fold_cross_validation(batches + file, classpath, 'segmentation', n_folds)

from os import path, listdir
import shutil
import re

from sklearn.cross_validation import KFold
# from grobid import GrobidTrainer
from grobid_shell import GrobidTrainer

import numpy as np
import matplotlib.pyplot as plt


class Category:
    TOKEN = 0
    FIELD = 1
    INSTANCE = 2
    CONFUSION = 3


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


def read_output(log_path):
    f = open(log_path)

    results = filter(bool, re.split(r'===== Token-level results =====|\
                                      ===== Field-level results =====|\
                                      ===== Instance-level results =====|\
                                      ===== Confusion matrix =====',
                                    f.read()))
    f.close()
    # print results[0]

    # from pylab import *

    # data = [1, 2, 3, 4, 5]
    # figure()
    # boxplot(data)
    # show()

    confusion_matrix = filter(bool, results[Category.CONFUSION].split('\n'))
    labels = np.matrix([row.split('\t')[0] for row in confusion_matrix])
    counts = np.matrix([row.split('\t')[1:] for row in confusion_matrix])

    fig, ax = plt.subplots()
    ax.set_xticklabels(labels.tolist()[0])

    row = counts[0].tolist()[0]

    bars = ax.bar(range(len(row)), [int(val) for val in row])

    plt.show()


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

    # directory = path.dirname(path.realpath(__file__))

    # grobid = directory + '/../grobid/'
    # log_path = directory + '/logs/'
    # model = 'date'
    # n_folds = 5

    # k_fold_cross_validation(grobid=grobid, model=model,
    #                         n_folds=n_folds, log_path=log_path)

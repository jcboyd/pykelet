import os
import sys
import shutil
import re

from sklearn.cross_validation import KFold
from grobid import GrobidTrainer


def redirect_stdout(output):
    """http://stackoverflow.com/questions/8804893/redirect-stdout-from-python-for-c-calls"""
    sys.stdout.flush()  # <--- important when redirecting to files
    newstdout = os.dup(1)
    redirection = os.open(output, os.O_WRONLY)
    os.dup2(redirection, 1)
    os.close(redirection)
    sys.stdout = os.fdopen(newstdout, 'w')


def k_fold_cross_validation(corpus, evaluate, log, n_folds):
    redirect_stdout(open('log.txt', 'wb').name)

    grobid_home = '/home/joseph/Desktop/pykelet/pipeline/grobid/grobid-home'
    classpath_trainer = '/home/joseph/Desktop/pykelet/pipeline/grobid/grobid-trainer.jar'
    model = 'segmentation'
    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home,
                                   model=model)

    training_set = os.listdir(corpus)
    shutil.rmtree(evaluate)
    os.mkdir(evaluate)

    folds = list(KFold(len(training_set), n_folds=n_folds))

    for fold in folds:
        # move all fold files to evaluate folder
        for index in fold[1]:
            shutil.move(corpus + training_set[index], evaluate)

        grobid_trainer.train()

        grobid_trainer.evaluate()

        # move fold files back to corpus folder
        for index in fold[1]:
            shutil.move(evaluate + corpus[index], corpus)


def read_output():
    f = open('log.txt')

    results = re.split(r'===== Token-level results =====|\
                         ===== Field-level results =====|\
                         ===== Instance-level results =====',
                       f.read())[1:]
    f.close()
    print results[0]

    from pylab import *

    spread = rand(50) * 100
    center = ones(25) * 50
    flier_high = rand(10) * 100 + 100
    flier_low = rand(10) * -100
    data = concatenate((spread, center, flier_high, flier_low), 0)
    spread = rand(50) * 100
    center = ones(25) * 40
    flier_high = rand(10) * 100 + 100
    flier_low = rand(10) * -100
    d2 = concatenate((spread, center, flier_high, flier_low), 0)
    data.shape = (-1, 1)
    d2.shape = (-1, 1)
    data = [data, d2, d2[::2, 0]]
    figure()
    boxplot(data)
    show()

if __name__ == '__main__':
    corpus = '/home/joseph/Desktop/pykelet/pipeline/grobid/grobid-trainer/resources/dataset/segmentation/corpus/tei/'
    evaluate = '/home/joseph/Desktop/pykelet/pipeline/grobid/grobid-trainer/resources/dataset/segmentation/evaluation/tei/'
    log = '/home/joseph/Desktop/'
    n_folds = 5

    k_fold_cross_validation(corpus, evaluate, log, n_folds)

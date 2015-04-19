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


def k_fold_cross_validation(grobid, model, n_folds, log):
    grobid_home = grobid + '/grobid-home'
    corpus = grobid + '/grobid-trainer/resources/dataset/' \
                      'segmentation/corpus/tei/'
    evaluation = grobid + '/grobid-trainer/resources/dataset/' \
                          'segmentation/evaluation/tei/'
    classpath_trainer = grobid + '/grobid-trainer.jar'
    grobid_trainer = GrobidTrainer(classpath=classpath_trainer,
                                   grobid_home=grobid_home,
                                   model=model)
    training_set = os.listdir(corpus)
    shutil.rmtree(evaluation)
    os.mkdir(evaluation)

    folds = list(KFold(len(training_set), n_folds=n_folds))

    for fold in folds:
        try:
            # move all fold files to evaluate folder
            for index in fold[1]:
                shutil.move(corpus + training_set[index], evaluation)

            grobid_trainer.train()
            # redirect_stdout(open('log.txt', 'wb').name)
            grobid_trainer.evaluation()
        finally:
            # move fold files back to corpus folder
            for index in fold[1]:
                shutil.move(evaluation + corpus[index], corpus)


def read_output():
    f = open('log.txt')

    results = re.split(r'===== Token-level results =====|\
                         ===== Field-level results =====|\
                         ===== Instance-level results =====',
                       f.read())[1:]
    f.close()
    print results[0]

    from pylab import *

    data = [1, 2, 3, 4, 5]
    figure()
    boxplot(data)
    show()

if __name__ == '__main__':
    grobid = '/home/joseph/Desktop/pykelet/pipeline/grobid/'
    model = 'segmentation'
    log = '/home/joseph/Desktop/'
    n_folds = 5

    k_fold_cross_validation(grobid, model, n_folds, log)

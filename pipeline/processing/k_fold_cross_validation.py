from os import open, close, dup, O_WRONLY
from sklearn.cross_validation import KFold
from grobid import GrobidTrainer
import shutil
import os

def k_fold_cross_validation(folds, corpus, evaluate, log):
    grobid_trainer = grobid.GrobidTrainer()

    training_set = os.listdir(corpus)
    shutil.rmtree(evaluate)
    os.mkdir(evaluate)

    folds = list(KFold(len(training_set), n_folds=folds))

    for fold in folds:
        # move all fold files to evaluate folder
        for index in fold[0][1]:
            shutil.move(corpus + corpus[index], evaluate)

        grobid_trainer.train()

        old = dup(1)
        close(1)
        open(log + , O_WRONLY) # should open on 1

        grobid_trainer.evaluate()

        close(1)
        dup(old) # should dup to 1
        close(old) # get rid of left overs

        # move fold files back to corpus folder
        for index in fold[0][1]:
            shutil.move(evaluate + corpus[index], corpus)

if __name__ == '__main__':
    folds = 5
    corpus = 'path/to/corpus'
    evaluate = 'path/to/evaluate'
    log = '/path/to/log'

    k_fold_cross_validation(folds, corpus, evaluate, log)

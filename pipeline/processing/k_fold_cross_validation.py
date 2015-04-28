from os import path, listdir
import shutil
import re

from sklearn.cross_validation import KFold
from grobid import GrobidTrainer


def k_fold_cross_validation(grobid, model, n_folds, log_path):
    grobid_home = grobid + '/grobid-home'
    corpus = grobid + \
        '/grobid-trainer/resources/dataset/%s/corpus//' % (model)
    evaluation = grobid + \
        '/grobid-trainer/resources/dataset/%s/evaluation//' % (model)
    classpath_trainer = grobid + \
        '/grobid-trainer/target/grobid-trainer-0.3.4-SNAPSHOT.jar'

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
            grobid_trainer.evaluate(model, log_path + "/%s_%s" % (model, i))
            i += 1
        except IOError:
            print 'Error: check folder configuration'
        finally:
            # move fold files back to corpus folder
            for index in fold[1]:
                shutil.move(evaluation + training_set[index], corpus)


def read_output(log_path):
    f = open(log_path)

    results = re.split(r'===== Token-level results =====|\
                         ===== Field-level results =====|\
                         ===== Instance-level results =====|\
                         ===== Confusion matrix =====',
                       f.read())[1:]
    f.close()
    print results[0]

    # from pylab import *

    # data = [1, 2, 3, 4, 5]
    # figure()
    # boxplot(data)
    # show()

if __name__ == '__main__':
    directory = path.dirname(path.realpath(__file__))

    grobid = directory + '/../grobid/'
    log_path = directory + '/logs/'
    model = 'date'
    n_folds = 5

    k_fold_cross_validation(grobid=grobid, model=model,
                            n_folds=n_folds, log_path=log_path)

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import learning_curve, ShuffleSplit, RandomizedSearchCV
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# mapping similar index of multiple containers of data within feature labels to be used as a single entity
def reshapeX(X): return X.reshape((X.shape[0], X.shape[1] * X.shape[2]))
def reshapeY(Y): return list(zip(*Y))[0]

# param_distributions: a dictionary with parameters names (string) as keys of parameters to try
def randomSearch(X, Y, param_distributions):
    # number of jobs = -1 to run all processors; n_iter trades off runtime with quality of solution
    # cv is at default value for 5-fold cross validation
    # verbose gives out messages; refit is to refit an estimator to find the best parameters
    # random_state is a pseudo random number generator used for random uniform sampling from list of possible values instead of using scipy.stats distributions
    searchrand = RandomizedSearchCV(SVC(), param_distributions, n_iter=10, n_jobs=-1, refit=True, verbose=3)
    searchrand.fit(X, Y)
    searchrand.cv_results_
    
    # returns the best parameter values of each kernel along with the kernel 
    return searchrand.best_params_, searchrand.best_estimator_

def plot_learning_curve(estimator, title, X, y, axes=None, ylim=None, cv=None,
                        n_jobs=None, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate plots: the test and training learning curve
    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods. Parse linear, rbf and polynomial classifier
    title : string
        Title for the chart.
    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.
    y : array-like, shape (n_samples)
        Target relative to X for classification or regression;
        None for unsupervised learning.
    axes : Axes to use for plotting the curves.
    ylim : Defines minimum and maximum yvalues plotted.
    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 5-fold cross-validation,
          - integer, to specify the number of folds.
          - :term:`CV splitter`,
          - An iterable yielding (train, test) splits as arrays of indices.
        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.
        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.
    n_jobs : int or None, optional (default=None)
        Number of jobs to run in parallel.
        ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
        ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
        for more details.
    train_sizes : array-like, shape (n_ticks,), dtype float or int
        Relative or absolute numbers of training examples that will be used to
        generate the learning curve. If the dtype is float, it is regarded as a
        fraction of the maximum size of the training set (that is determined
        by the selected validation method), i.e. it has to be within (0, 1].
        Otherwise it is interpreted as absolute sizes of the training sets.
        Note that for classification the number of samples usually have to
        be big enough to contain at least one sample from each class.
        (default: np.linspace(0.1, 1.0, 5))
    """

    axes.set_title(title)
    if ylim is not None:
        axes.set_ylim(*ylim)
        axes.set_xlabel("Training examples")
        axes.set_ylabel("Score")
        
        train_sizes, train_scores, test_scores = learning_curve(
            estimator, X, y, train_sizes=train_sizes, cv=cv, n_jobs=n_jobs)
        
        train_scores_mean = np.mean(train_scores, axis=1)
        train_scores_std = np.std(train_scores, axis=1)
        test_scores_mean = np.mean(test_scores, axis=1)
        test_scores_std = np.std(test_scores, axis=1)

        # Plot learning curve
        axes.grid()
        axes.fill_between(train_sizes, train_scores_mean - train_scores_std,
                             train_scores_mean + train_scores_std, alpha=0.1,
                             color="r")
        axes.fill_between(train_sizes, test_scores_mean - test_scores_std,
                             test_scores_mean + test_scores_std, alpha=0.1,
                             color="g")
        axes.plot(train_sizes, train_scores_mean, 'o-', color="r",
                     label="Training score")
        axes.plot(train_sizes, test_scores_mean, 'o-', color="g",
                     label="Cross-validation score")
        axes.legend(loc="best")

    return

def train(tr_X, te_X, tr_Y, te_Y):
    # setting upper and lower boundary values for random search range and
    # Obtaining optimum hyperparameters and classifier for different kernels
#     linSVC_param, lin_SVC = randomSearch(tr_X, tr_Y, {
#         'C': stats.uniform(0.1, 10), 'kernel': ['linear']})
#     polySVC_param, poly_SVC = randomSearch(tr_X, tr_Y, {
#         'C': stats.uniform(0.1, 10), 'degree': stats.uniform(1, 4), 'kernel': ['poly']})
    rbfSVC_param, rbf_SVC = randomSearch(tr_X, tr_Y, {
        'C': stats.uniform(0.1, 10), 'gamma': stats.uniform(0.0001, 0.01), 'kernel': ['rbf']})

    # Display optimum hyperparameters for SVC kernel
#     print('Optimum hyperparameters for linear kernel: ')
#     print(linSVC_param)
#     print('Optimum hyperparameters for polynomial kernel: ')
#     print(polySVC_param)
    print('Optimum hyperparameters for rbf kernel: ')
    print(rbfSVC_param)

    # printing validation accuracy score for each kernel
#     print(lin_SVC.score(te_X, te_Y))
#     print(poly_SVC.score(te_X, te_Y))
#     print(rbf_SVC.score(te_X, te_Y))
    
    # Cross validation with more iterations to get smoother mean test and train score curves, each time with 20% data randomly selected as a validation set.
    # SVC is more expensive so we do a lower number of CV iterations.
    # cv = ShuffleSplit(n_splits=50, test_size=0.2, random_state=0)

    # plt.figure(figsize=(9,18))

    # axes = plt.subplot(311)
    # title = r"Learning Curves (linear)"
    # plot_learning_curve(lin_SVC, title, te_X, te_Y, axes=axes, ylim=(0.8, 1.01), cv=cv, n_jobs=-1)

    # axes = plt.subplot(312)
    # title = r"Learning Curves (poly)"
    # plot_learning_curve(poly_SVC, title, te_X, te_Y, axes=axes, ylim=(0.8, 1.01), cv=cv, n_jobs=-1)

    # axes = plt.subplot(313)
    # title = r"Learning Curves (rbf)"
    # plot_learning_curve(rbf_SVC, title, te_X, te_Y, axes=axes, ylim=(0.7, 1.01), cv=cv, n_jobs=-1)

    # plt.show()
    
    return rbf_SVC

####################### EVALUATION STARTS HERE #####################

def testResults(model, filename, type_, label):
    A,b = filename.extract_features_labels(type_, label)

    # similar preprocessing works for test data
    B = np.array([b, -(b - 1)]).T

    te_A = reshapeX(A)
    te_B = reshapeY(B)
    
    op_rbf_results = model.predict(te_A)

    cm = confusion_matrix(te_B, op_rbf_results)
    print(cm)
    plt.matshow(cm)
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    print('\nConfusion matrix')
    plt.show()

    # cm2 = confusion_matrix(te_B, op_rbf_results, normalize='all')
    # print(cm2)
    # plt.matshow(cm2)
    # plt.colorbar()
    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')
    # print('\nConfusion matrix(normalised)')
    # plt.show()
    
    test_accuracy = accuracy_score(te_B, op_rbf_results)

    print(classification_report(te_B, op_rbf_results))
    print('Accuracy achieved:', test_accuracy, '\u2661''\u2661''\u2661')
    
    return test_accuracy
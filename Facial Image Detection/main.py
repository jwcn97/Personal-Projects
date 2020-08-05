import os
import preprocess
import A.landmarks as l1
import A.A as gender
from B.B import CNN_model

# define paths
AMLS_dir = os.path.abspath(os.curdir)
B_dir = os.path.join(AMLS_dir, 'B')
model_B1_path = os.path.join(B_dir, 'VGGNet.h5')
model_B2_path = os.path.join(B_dir, 'VGGNet_eye.h5')

# task A1
tr_X, te_X, tr_Y, te_Y = preprocess.A(l1, 'celeba', 1)
rbf_SVC = gender.train(tr_X, te_X, tr_Y, te_Y)
acc_A1_train = rbf_SVC.score(tr_X, tr_Y)
acc_A1_test = gender.testResults(rbf_SVC, l1, 'celeba_test', 1)

# task A2
tr_X, te_X, tr_Y, te_Y = preprocess.A(l1, 'celeba', 2)
rbf_SVC = gender.train(tr_X, te_X, tr_Y, te_Y)
acc_A2_train = rbf_SVC.score(tr_X, tr_Y)
acc_A2_test = gender.testResults(rbf_SVC, l1, 'celeba_test', 2)

# task B1
train_generator, validation_generator, eval_generator, test_generator = preprocess.B1('cartoon_set/', 'cartoon_set_test/')
model_B1 = CNN_model()
acc_B1_train, model_path1 = model_B1.train(B_dir, 'VGGNet.h5', 5, train_generator, validation_generator, eval_generator)
acc_B1_test = model_B1.test(model_B1_path, test_generator)

# task B2
train_generator, validation_generator, eval_generator, test_generator = preprocess.B2('cartoon_set/', 'cartoon_set_test/')
model_B2 = CNN_model()
acc_B2_train, model_path2 = model_B2.train(B_dir, 'VGGNet_eye.h5', 5, train_generator, validation_generator, eval_generator)
acc_B2_test = model_B2.test(model_B2_path, test_generator)

# ======================================================================================================================
## Print out your results with following format:
print('TA1:{},{};TA2:{},{};TB1:{},{};TB2:{},{};'.format(acc_A1_train, acc_A1_test,
                                                        acc_A2_train, acc_A2_test,
                                                        acc_B1_train, acc_B1_test,
                                                        acc_B2_train, acc_B2_test))
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator

# mapping similar index of multiple containers of data within feature labels to be used as a single entity
def reshapeX(X): return X.reshape((X.shape[0], X.shape[1] * X.shape[2]))
def reshapeY(Y): return list(zip(*Y))[0]

def A(filename, type_, label):
    # returning landmark features and feature labels as X and Y respectively
    X,y = filename.extract_features_labels(type_, label)
    # creating and self transposing array of y, offsetting y values by -1
    Y = np.array([y, -(y - 1)]).T

    # random shuffling of data 
    X, Y = shuffle(X,Y)
    # split 70% of the dataset as training data and remaning as validation data
    tr_X, te_X, tr_Y, te_Y = train_test_split(X, Y, train_size=0.7)
    
    tr_X = reshapeX(tr_X)
    te_X = reshapeX(te_X)
    tr_Y = reshapeY(tr_Y)
    te_Y = reshapeY(te_Y)
    
    return tr_X, te_X, tr_Y, te_Y

def split(df, df2, train_path, test_path):
    training, testing = np.split(df.sample(frac=1), [int(0.9*len(df)),]) #splitting at n-array

    img = train_path + 'img'
    img2 = test_path + 'img'

    # set up data generator
    train_data_generator = ImageDataGenerator(
        rescale = 1./255.,
        validation_split = 0.2,
        horizontal_flip=True,
        vertical_flip=True
    )
    
    # Generate test dataset from dataframe
    test_data_generator = ImageDataGenerator(rescale=1./255)
    
    # Get batches of training dataset from the dataframe
    print("Training Dataset Preparation: ")
    train_generator = train_data_generator.flow_from_dataframe(
            dataframe = training, directory = img,
            x_col = "file_name", y_col = "face_shape",
            class_mode = 'categorical', target_size = (64,64), shuffle=True,
            batch_size = 128, subset = 'training')

    # Get batches of validation dataset from the dataframe
    print("\nValidation Dataset Preparation: ")
    validation_generator = train_data_generator.flow_from_dataframe(
            dataframe = training, directory = img,
            x_col = "file_name", y_col = "face_shape",
            class_mode = 'categorical', target_size = (64,64), shuffle=True,
            batch_size = 128, subset = 'validation')

    # Get batches of test dataset from the dataframe
    print("\nEvaluation Dataset Preparation: ")
    eval_generator = train_data_generator.flow_from_dataframe(
            dataframe = training, directory = img,
            x_col = "file_name", y_col = "face_shape",
            class_mode = 'categorical', target_size = (64,64), shuffle=True,
            batch_size = 1, subset = 'validation')

    # Get batches of test dataset from the dataframe
    print("\nTest Dataset Preparation: ")
    test_generator = test_data_generator.flow_from_dataframe(
            dataframe = testing, directory = img2,
            x_col = "file_name", y_col = "face_shape",
            class_mode = 'categorical', target_size = (64,64), shuffle=False,
            batch_size = 1)
    
    return train_generator, validation_generator, eval_generator, test_generator

def B1(train_p, test_p):
    train_path = 'Dataset/' + train_p
    test_path = 'Dataset/' + test_p

    df = pd.read_csv(train_path + 'labels.csv', sep = '\t')
    df = df.drop(columns = [df.columns[0]]).drop(columns = [df.columns[1]])
    df['face_shape'] = df['face_shape'].apply(str)

    df2 = pd.read_csv(test_path + 'labels.csv', sep = '\t')
    df2 = df2.drop(columns = [df2.columns[0]]).drop(columns = [df2.columns[1]])
    df2['face_shape'] = df2['face_shape'].apply(str)

    return split(df, df2, train_path, test_path)

def B2(train_p, test_p):
    train_path = '../Dataset/' + train_p
    test_path = '../Dataset/' + test_p

    df = pd.read_csv(train_path + 'labels.csv', sep = '\t')
    df = df.drop(columns = [df.columns[0]]).drop(columns = [df.columns[2]])
    df['eye_color'] = df['eye_color'].apply(str)

    df2 = pd.read_csv(test_path + 'labels.csv', sep = '\t')
    df2 = df2.drop(columns = [df2.columns[0]]).drop(columns = [df2.columns[2]])
    df2['eye_color'] = df2['eye_color'].apply(str)
    
    training, testing = np.split(df.sample(frac=1), [int(0.9*len(df)),]) #splitting at n-array

    img = train_path + 'img'
    img2 = test_path + 'img'

    # set up data generator
    data_generator = ImageDataGenerator(
        rescale = 1./255.,
        validation_split = 0.2,
        horizontal_flip=True,
        vertical_flip=True
    )

    # Get batches of training dataset from the dataframe
    print("Training Dataset Preparation: ")
    train_generator = data_generator.flow_from_dataframe(
            dataframe = training, directory = img,
            x_col = "file_name", y_col = "eye_color",
            class_mode = 'categorical', target_size = (64,64),
            batch_size = 128, subset = 'training') 

    # Get batches of validation dataset from the dataframe
    print("\nValidation Dataset Preparation: ")
    validation_generator = data_generator.flow_from_dataframe(
            dataframe = training, directory = img ,
            x_col = "file_name", y_col = "eye_color",
            class_mode = 'categorical', target_size = (64,64),
            batch_size = 128, subset = 'validation')
    
    return train_generator, validation_generator, data_generator, df2, img2
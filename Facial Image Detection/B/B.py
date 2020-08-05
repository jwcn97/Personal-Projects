import os
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, GlobalAveragePooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import matplotlib.pyplot as plt

# Use early stopping to terminate training epochs through callbacks
from tensorflow.python.keras.callbacks import EarlyStopping, ModelCheckpoint

from sklearn.metrics import accuracy_score

class CNN_model:
    # Callback function to interrupt the overfitting model
    def callback_func(self, B_dir, model_name):
        # Seek a mininum for validation loss and display the stopped epochs using verbose and adding delays
        es = EarlyStopping(monitor='val_lose', mode='min', verbose=1, patience=5)
        
        # Save best model using checkpoint
        model_path = os.path.join(B_dir, model_name)
        mcp = ModelCheckpoint(os.path.normcase(model_path), monitor='val_loss', mode='min', verbose=1, save_best_only=True)
        
        # Define callback function in a list
        callback_list = [es, mcp]
        
        return callback_list, model_path


    def train(self, myDir, model_name, num_class, train_generator, validation_generator, eval_generator):
        cb_list, CNN_model_path = self.callback_func(myDir, model_name)

        my_model = Sequential()

        # Add first convolutional block
        #     for more info on Conv2D, refer to https://www.pyimagesearch.com/2018/12/31/keras-conv2d-and-convolutional-layers/
        #     for more info on MaxPooling2D, refer to https://deeplizard.com/learn/video/ZjM_XQa5s6s
        my_model.add(Conv2D(16, (3, 3), activation='relu', padding='same',input_shape=(64,64,3))) 
        my_model.add(MaxPooling2D((2, 2), padding='same'))
        # second block
        my_model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
        my_model.add(MaxPooling2D((2, 2), padding='same'))
        # third block
        my_model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
        my_model.add(MaxPooling2D((2, 2), padding='same'))
        # fourth block
        my_model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
        my_model.add(MaxPooling2D((2, 2), padding='same'))

        # make predictions
        my_model.add(Flatten())
        my_model.add(Dense(units=num_class, activation='softmax'))
        # Show a summary of the model. Displaying the number of trainable parameters
        my_model.summary()
        my_model.compile(optimizer='adam', loss='categorical_crossentropy', 
                        metrics=['accuracy'])

        # Set steps per epoch for callback
        STEP_SIZE_TRAIN = train_generator.samples // train_generator.batch_size
        STEP_SIZE_VALID = validation_generator.samples // validation_generator.batch_size

        result = my_model.fit_generator(
                generator=train_generator,
                steps_per_epoch=STEP_SIZE_TRAIN,
                epochs=13,
                callbacks=cb_list,
                validation_data=validation_generator,
                validation_steps=STEP_SIZE_VALID
        )

        eval_model = my_model.evaluate_generator(generator=eval_generator, steps=STEP_SIZE_VALID, verbose=1)
        print('Training '+ str(my_model.metrics_names[1]) + ': '  + str(eval_model[1]))
        train_acc = {'CNN-softmax': eval_model[1]}

        # plt.figure(figsize=(18, 3))

        # plt.subplot(131)
        # plt.plot(result.history['accuracy'])
        # plt.plot(result.history['val_accuracy'])
        # plt.ylim([.3,1.1])
        # plt.ylabel('Accuracy')
        # plt.xlabel('Epoch')
        # plt.legend(['Train', 'Validation'], loc='upper left')

        # plt.subplot(132)
        # plt.plot(result.history['loss'])
        # plt.plot(result.history['val_loss'])
        # plt.ylim([0,1.7])
        # plt.ylabel('Loss')
        # plt.xlabel('Epoch')
        # plt.legend(['Train', 'Validation'], loc='best')

        # plt.show()

        return train_acc, CNN_model_path
        
    def test(self, model_path, test_generator):
        # Fit the model to the test dataset by loading the model
        saved_model = load_model(model_path)
        
        # Predict the face shape
        STEP_SIZE_TEST = test_generator.samples // test_generator.batch_size
        test_generator.reset()
        pred = saved_model.predict_generator(test_generator, steps=STEP_SIZE_TEST, verbose=1)
        
        # Determine the maximum activation value at the output layers for each sample
        pred_class = np.argmax(pred, axis=1)   # axis = 1 give max value along each row
        
        # True labels of test dataset
        true_class = test_generator.classes
        
        # Accuracy score
        test_score = accuracy_score(true_class, pred_class)
        
        test_acc = {'CNN-softmax': test_score}
        
        return test_acc

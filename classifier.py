import tensorflow as tf

import numpy as np
from sklearn.model_selection import train_test_split

# TODO: max accuracy ~ 72% -> Ensembles? andere stoplist? negationen wichtig!


class Classifier:
    """Simple binary classifier that takes multiple sentences and tries to
       predict the label of a new given sentence"""
    def __init__(self, data, labels, dictionary_size):
        """Creates and trains a new nn

        Arguments:
            data: list<String>, sentences
            labels: list<String>, labels of the sentences
            dictionary_size: int, size of the dictionary"""

        # same length for every datapoint
        data = tf.keras.preprocessing.sequence.pad_sequences(
            data, maxlen=256, padding='post')
        # split into train and test set
        x_train, x_test, y_train, y_test = train_test_split(
            data, labels, test_size=0.2, shuffle=True)
        # split further into train and validation set
        x_train, x_validate, y_train, y_validate = train_test_split(
            x_train, y_train, test_size=0.2, shuffle=False)
        # self.x_train, self.x_validate, self.x_test = (x_train,)

        print('Size - Train:{0}, Test:{1}, Validation: {2}'.format(
            len(x_train), len(x_test), len(x_validate)))

        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Embedding(dictionary_size, 32))
        self.model.add(tf.keras.layers.Dropout(0.2))
        self.model.add(tf.keras.layers.GlobalAveragePooling1D())
        self.model.add(tf.keras.layers.Dense(32, activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dropout(0.5))
        self.model.add(tf.keras.layers.Dense(1, activation=tf.nn.sigmoid))

        self.model.compile(optimizer=tf.train.AdamOptimizer(),
                           loss='binary_crossentropy',
                           metrics=['accuracy'])

        history = self.model.fit(x_train,
                                 y_train,
                                 epochs=10,
                                 batch_size=256,
                                 validation_data=(x_validate, y_validate),
                                 verbose=1)

        results = self.model.evaluate(x_test, y_test)
        print(results)

    def predict(self, datapoint):
        """Predicts the label of a sentence

        Arguments:
            datapoint: String, a sentence

        Returns:
            prediction"""
        datapoint = (tf.keras.preprocessing.sequence.pad_sequences(
            [datapoint], maxlen=256, padding='post'))
        return self.model.predict(datapoint)

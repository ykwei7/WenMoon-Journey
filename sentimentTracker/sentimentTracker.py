import os
import re
import string
import tensorflow as tf
import random
import numpy as np
from tensorflow import keras

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

def load_data(data_directory):
    dataset = []
    label_count = 0
    # neg, pos, neu labelled as 0,1,2 respectively
    for label in ["neg", "pos", "neu"]:
        labeled_dir = f"{data_directory}/{label}"
        for file in os.listdir(labeled_dir):
            if file.endswith(".txt"):
                with open(f"{labeled_dir}/{file}", mode='r') as f:
                    reader = f.read()
                    text = tf.expand_dims(reader, -1)
                    # print(vectorize_layer(text).shape)
                    # tensor of shape (1,250) is outputted
                    # print(type(vectorize_layer(text)))
                    dataset.append([vectorize_layer(text), label_count])
        label_count += 1
    random.shuffle(dataset)
    x_train = []
    y_train = []

    for data in dataset:
        x_train.append(data[0])
        y_train.append(np.int32(data[1]))

    x_train = np.array(x_train)
    y_train = np.array(y_train)

    return x_train, y_train

max_features = 10000
sequence_length = 250

vectorize_layer = TextVectorization(
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

def create_model():
    # Make a text-only dataset (without labels), then call adapt
    embedding_dim = 16
    x_train, y_train = load_data("training_data")
    embedding_dim = 16

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) #relu refers to rectified linear function
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(3, activation=tf.nn.softmax)) #2 is number of categories to output to

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def train_model(model, epochs,x_train,y_train):
    epochs = epochs
    history = model.fit(
        x_train,
        y_train,
        epochs=epochs)

# model.save("stock_model")

text2 = "This stock is bearish"
def vectorize_text(text):
    text = tf.expand_dims(text, -1)
    text = vectorize_layer(text)
    return np.array(text)

# predicts which category the text belongs to and returns an index corresponding to this category
def predict(model, text):
    scores = model.predict(vectorize_text(text))[0].tolist()
    # print(scores)
    max_score = max(scores)
    return scores.index(max_score)

if __name__ == '__main__':
    x_train, y_train = load_data("training_data")
    model = create_model()
    train_model(model,1000,x_train,y_train)
    model.save("stock_model")
    # path = "stock_model"
    # model = keras.models.load_model(path)
    print(predict(model, "this stock is average"))
#print(model.predict(vectorize_text(text2)))







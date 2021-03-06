"""
This file is added to test the functionality of alexnet for pokemon
"""

import tensorflow as tf
import os
import csv

from helper import load_pokemon, preprocess

dataset_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/dataset'
checkpoint_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/training/cp.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)
table_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/AlexNet_TensorFlow2.0-2.2/training' \
             '/label.csv '


def predict(path, model_):
    x, _ = preprocess(path, 1)
    x = tf.reshape(x, (-1, 227, 227, 3))
    return model_(x)


def myeval():
    model = tf.saved_model.load('saved_model/my_model')
    images, labels, _ = load_pokemon(dataset_path, 'test')
    db = tf.data.Dataset.from_tensor_slices((images, labels))
    db = db.shuffle(1000).map(preprocess).batch(32).repeat(20)
    acc_meter = tf.metrics.Accuracy()
    for step, (x, y) in enumerate(db):
        # Build the gradient records
        with tf.GradientTape() as tape:
            # Flatten the input such as [b,28,28]->[b,784]
            x = tf.reshape(x, (-1, 227, 227, 3))
            output = model(x)
            # Compare the predicted value and labels and related precision
            acc_meter.update_state(tf.argmax(output, axis=1), y)
            # Print the results per 200 steps
        # if step % 50 == 0:
            print('Step', step, ' Accuracy: ', acc_meter.result().numpy())
            acc_meter.reset_states()


# myeval()

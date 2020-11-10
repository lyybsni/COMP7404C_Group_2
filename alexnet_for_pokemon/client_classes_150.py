# client.py

"""
The application of the client is used to call the alexnet model. 
"""

import csv
import glob
import os
import random

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import optimizers, metrics

from helper import load_pokemon, preprocess

from alexnet import AlexNet

# Set the GPU growth to avoid the cuDNN runtime error. 
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

# Configuration
dataset_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/dataset'
checkpoint_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/training/cp.ckpt'
checkpoint_dir = os.path.dirname(checkpoint_path)
table_path = '/Users/richardli/Documents/Academia/HKU-2020/COMP7404/Group_Project/AlexNet_TensorFlow2.0-2.2/training/label.csv'
# tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

# Upload the self-defined datasets
images, labels, table = load_pokemon(dataset_path, 'train')

# Write Table to csv file
with open(table_path, mode='w', newline='') as f:
    writer = csv.writer(f)
    for key in table:
        # Write them into the csv and divide them with comma, i.e, pokemon\\mewtwo\\00001.png, 2
        writer.writerow([table[key], key])  #
    print('written into csv file:', table_path)

# Print them if necessary
# -print('images', len(images), images)
# -print('labels', len(labels), labels)
# -print(table)
# images:string path，labels:number
db = tf.data.Dataset.from_tensor_slices((images, labels))
db = db.shuffle(1000).map(preprocess).batch(32).repeat(20)

# Set the global constant as 150
num_classes = 150

# EDITED BY LI YUYANG
try:
    # model.load_weights(checkpoint_path)
    model = tf.saved_model.load('saved_model/my_model')
    print("model loaded")
except ValueError:
    model = AlexNet((227, 227, 3), num_classes)
    print("No previous model trained. Training.")
finally:
    print("model ready")

# model.summary()

# Train the model: compute gradients and update network parameters
optimizer = optimizers.SGD(lr=0.01)
acc_meter = metrics.Accuracy()
x_step = []
y_accuracy = []


def train():
    # Input the batch for the training
    for step, (x, y) in enumerate(db):
        # Build the gradient records
        with tf.GradientTape() as tape:
            # Flatten the input such as [b,28,28]->[b,784]
            x = tf.reshape(x, (-1, 227, 227, 3))
            output = model(x)
            y_onehot = tf.one_hot(y, depth=150)
            loss = tf.square(output - y_onehot)
            loss = tf.reduce_sum(loss) / 32
            # Compute the gradients of each parameter
            grads = tape.gradient(loss, model.trainable_variables)
            # Update network parameters
            optimizer.apply_gradients(zip(grads, model.trainable_variables))
            # Compare the predicted value and labels and related precision
            acc_meter.update_state(tf.argmax(output, axis=1), y)
            # Print the results per 200 steps
        if step % 50 == 0:
            print('Step', step, ': Loss is: ', float(loss), ' Accuracy: ', acc_meter.result().numpy())
            x_step.append(step)
            y_accuracy.append(acc_meter.result().numpy())
            acc_meter.reset_states()

            # EDITED BY LI YUYANG
            # save the model to the file
            tf.saved_model.save(model, checkpoint_path)
            # model.save('saved_model/my_model')
            print("Model saved")


# Start to train the model
train()

# Visualize the result with matplolib
plt.plot(x_step, y_accuracy, label="training")
plt.xlabel("step")
plt.ylabel("accuracy")
plt.title("accuracy of training")
plt.legend()
plt.show()

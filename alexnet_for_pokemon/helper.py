import glob
import os
import csv
import random

import tensorflow as tf

# Create image path and labels and write them into the .csv file; root: dataset root directory,
# filename:csv name, name2label:class coding table.
def load_csv(root, filename, name2label):
    # If there is no csv, create a csv file and save it into the directory of home/mike/datasets/pokemon
    if not os.path.exists(os.path.join(root, filename)):
        # Initialize the array in which image paths are saved.
        images = []
        # Iterate all sub-directories and obtain all the paths of images.
        for name in name2label.keys():
            # Adopt the glob filename to match and obtain all files with the formats of png, jpg and jpeg
            images += glob.glob(os.path.join(root, name, '*.png'))
            images += glob.glob(os.path.join(root, name, '*.jpg'))
            images += glob.glob(os.path.join(root, name, '*.jpeg'))
        # Print it if necessary
        # -print(len(images), images)
        random.shuffle(images)
        # Create the csv file and write both the paths of images and the info of labels
        with open(os.path.join(root, filename), mode='w', newline='') as f:
            writer = csv.writer(f)
            for img in images:
                # Adopt the symbol of \\ to divide items and take all 2nd items as class names
                name = img.split(os.sep)[-2]
                # Find the values(as labels) related to the keys of classes
                label = name2label[name]
                # Write them into the csv and divide them with comma, i.e, pokemon\\mewtwo\\00001.png, 2
                writer.writerow([img, label])  #
            print('written into csv file:', filename)

    # Read the csv file and create two empty arrays of which y is used to save both paths and labels.
    images, labels = [], []

    with open(os.path.join(root, filename)) as f:
        reader = csv.reader(f)
        for row in reader:
            img, label = row
            label = int(label)
            images.append(img)
            labels.append(label)
    # Determine whether the images have the same size as the labels
    assert len(images) == len(labels)
    return images, labels


# Iterate all sub-directories under the pokemon; take classnames as keys and lengths as class labels
def load_pokemon(root, mode='train'):
    # Create an empty dictionary{key:value} which holds both classnames and labels
    name2label = {}
    # Iterate sub-directories under the root dir and sort them.
    for name in sorted(os.listdir(os.path.join(root))):
        if not os.path.isdir(os.path.join(root, name)):
            continue
        name2label[name] = len(name2label.keys())
    # Read the paths and the labels of the csv
    images, labels = load_csv(root, 'images.csv', name2label)
    # Divide the dataset with the ratio of 6：2：2 for train、val and test sets.
    if mode == 'train':
        images = images[:int(0.6 * len(images))]
        labels = labels[:int(0.6 * len(labels))]
    elif mode == 'val':
        images = images[int(0.6 * len(images)): int(0.8 * len(images))]
        labels = labels[int(0.6 * len(labels)): int(0.8 * len(labels))]
    else:
        images = images[int(0.8 * len(images)):]
        labels = labels[int(0.8 * len(labels)):]
    return images, labels, name2label


img_mean = tf.constant([0.485, 0.456, 0.406])
img_std = tf.constant([0.229, 0.224, 0.225])


def normalize(x, mean=img_mean, std=img_std):
    x = (x - mean) / std
    return x


# Denormalize the images if necessary.
# -def denormalize(x, mean=img_mean, std=img_std):
# -x = x * std + mean
# -return x

def preprocess(image_path, label):
    x = tf.io.read_file(image_path)
    x = tf.image.decode_jpeg(x, channels=3)
    x = tf.image.resize(x, [244, 244])
    # Conduct data augmentation if necessary
    # -x = tf.image.random_flip_up_down(x)    # Flip up and down
    # -x = tf.image.random_flip_left_right(x) # Mirror from left to right
    x = tf.image.random_crop(x, [227, 227, 3])  # Crop images
    x = tf.cast(x, dtype=tf.float32) / 255.  # Normalization
    x = normalize(x)
    y = tf.convert_to_tensor(label)
    return x, y
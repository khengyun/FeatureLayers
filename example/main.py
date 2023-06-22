import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from featurelayers.layers.LBC import LBC
import tensorflow as tf


def unet(pretrained_weights=None, input_size=(128, 128, 3)):
    inputs = tf.keras.layers.Input(input_size)
    s = tf.keras.layers.Lambda(lambda x: x / 255.0)(inputs)  # normalization

    c1 = tf.keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same")(s)
    c1 = tf.keras.layers.BatchNormalization()(c1)
    # c1 = tf.keras.layers.Dropout(0.1)(c1)
    c1 = tf.keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same")(s)
    c1p = LBC(16, (3, 3), activation="relu", padding="same")(c1)
    p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1p)

    c2 = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(p1)
    c2 = tf.keras.layers.BatchNormalization()(c2)
    # c2 = tf.keras.layers.Dropout(0.1)(c2)
    c2 = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(c2)
    c2p = LBC(32, (3, 3), activation="relu", padding="same")(c2)
    p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2p)

    c3 = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(p2)
    c3 = tf.keras.layers.BatchNormalization()(c3)
    # c3 = tf.keras.layers.Dropout(0.1)(c3)
    c3 = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(c3)
    c3p = LBC(64, (3, 3), activation="relu", padding="same")(c3)
    p3 = tf.keras.layers.MaxPooling2D((2, 2))(c3p)

    c4 = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(p3)
    c4 = tf.keras.layers.BatchNormalization()(c4)
    # c4 = tf.keras.layers.Dropout(0.1)(c4)
    c4 = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(c4)
    c4p = LBC(128, (3, 3), activation="relu", padding="same")(c4)
    p4 = tf.keras.layers.MaxPooling2D((2, 2))(c4p)

    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation="relu", padding="same")(p4)
    c5 = tf.keras.layers.BatchNormalization()(c5)
    # c5 = tf.keras.layers.Dropout(0.1)(c5)
    c5 = tf.keras.layers.Conv2D(256, (3, 3), activation="relu", padding="same")(c5)
    c5 = LBC(256, (3, 3), activation="relu", padding="same")(c5)

    u6 = tf.keras.layers.Conv2DTranspose(128, (2, 2), strides=(2, 2), padding="same")(c5)
    u6 = tf.keras.layers.concatenate([u6, c4])
    c6 = tf.keras.layers.Conv2D(128, (3, 3), activation="relu", padding="same")(u6)
    c6 = tf.keras.layers.BatchNormalization()(c6)
    # c6 = tf.keras.layers.Dropout(0.1)(c6)
    c6 = LBC(128, (3, 3), activation="relu", padding="same")(c6)

    u7 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding="same")(c6)
    u7 = tf.keras.layers.concatenate([u7, c3])
    c7 = tf.keras.layers.Conv2D(64, (3, 3), activation="relu", padding="same")(u7)
    c7 = tf.keras.layers.BatchNormalization()(c7)
    # c7 = tf.keras.layers.Dropout(0.1)(c7)
    c7 = LBC(64, (3, 3), activation="relu", padding="same")(c7)

    u8 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding="same")(c7)
    u8 = tf.keras.layers.concatenate([u8, c2])
    c8 = tf.keras.layers.Conv2D(32, (3, 3), activation="relu", padding="same")(u8)
    c8 = tf.keras.layers.BatchNormalization()(c8)
    # c8 = tf.keras.layers.Dropout(0.1)(c8)
    c8 = LBC(32, (3, 3), activation="relu", padding="same")(c8)

    u9 = tf.keras.layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding="same")(c8)
    u9 = tf.keras.layers.concatenate([u9, c1])
    c9 = tf.keras.layers.Conv2D(16, (3, 3), activation="relu", padding="same")(u9)
    c9 = tf.keras.layers.BatchNormalization()(c9)
    # c9 = tf.keras.layers.Dropout(0.1)(c9)
    c9 = LBC(16, (3, 3), activation="relu", padding="same")(c9)

    outputs = tf.keras.layers.Conv2D(1, (1, 1), activation='sigmoid')(c9)

    model = tf.keras.Model(inputs=[inputs], outputs=[outputs], name='unet_model')
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()
    return model


model = unet()

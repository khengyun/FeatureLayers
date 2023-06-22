import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, Conv2DTranspose, MaxPooling2D, concatenate, ZeroPadding2D, Lambda, \
    BatchNormalization
from featurelayers.layers.LDP import LDP


def unet(pretrained_weights=None, input_size=(128, 128, 3)):
    inputs = Input(input_size)
    s = Lambda(lambda x: x / 255.0)(inputs)  # normalization

    c1 = Conv2D(16, (3, 3), activation="relu", padding="same")(s)
    c1 = BatchNormalization()(c1)
    c1 = Conv2D(16, (3, 3), activation="relu", padding="same")(c1)
    c1 = LDP(mode='single', alpha=0.0)(c1)
    p1 = MaxPooling2D((2, 2))(c1)

    model = Model(inputs=[inputs], outputs=[p1], name='unet_model')
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()
    return model


model = unet()
from keras.utils.vis_utils import plot_model

plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True)
model.summary()

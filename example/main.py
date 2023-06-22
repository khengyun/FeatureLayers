
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten
from featurelayers.layers.LBC import LBC

# Create a simple Keras model
model = Sequential()
# Add the LBC layer as the first layer in the model
model.add(LBC(filters=32, kernel_size=3, stride=1, padding='same', activation='relu', sparsity=0.9, name='lbc_layer'))
# Add a Flatten layer to convert the output to 1D
model.add(Flatten())
# Add a Dense layer for classification
model.add(Dense(units=10, activation='softmax'))

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
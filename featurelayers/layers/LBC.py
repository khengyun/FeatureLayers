# Imports
from scipy.stats import bernoulli
import joblib
import numpy as np
import tensorflow as tf
import keras
from keras.layers import Conv2D
from keras import backend as K
from keras.engine.base_layer import Layer


# Non-trainable filters initialized with distribution
# of Bernoulli as in article and then it's non-trainable
def new_weights_non_trainable(h, w, num_input, num_output, sparsity=0.5):
    """
       Create non-trainable weights with a Bernoulli distribution.

       Args:
           h: Height of the weight matrix.
           w: Width of the weight matrix.
           num_input: Number of input channels.
           num_output: Number of output channels.
           sparsity: Sparsity level of the weights.

       Returns:
           The non-trainable weight matrix.

       """

    # Extract integer values from the tuples
    h_val, w_val = h
    num_input_val, num_output_val = num_input, num_output

    # Number of elements
    num_elements = h_val * w_val * num_input_val * num_output_val
    # Create an array with n number of elements
    array = np.arange(num_elements)
    # Random shuffle it
    np.random.shuffle(array)
    # Fill with 0
    weight = np.zeros([num_elements])
    # Get the number of elements in the array that need to be non-zero
    ind = int(sparsity * num_elements + 0.5)
    # Get a piece of it as indexes for the weight matrix
    index = array[:ind]

    for i in index:
        # Fill those indexes with Bernoulli distribution
        # Method rvs = random variates
        weight[i] = bernoulli.rvs(0.5) * 2 - 1
    # Reshape weights array for the matrix that we need
    weights = weight.reshape(h_val, w_val, num_input_val, num_output_val)
    return weights


class LBC(Layer):
    def __init__(self, filters, kernel_size, stride=1, padding='same', activation='relu', dilation=1, sparsity=0.9,
                 name="lbc_layer"):
        """
        Local Binary Convolution (LBC) layer.

        Args:
            filters: Number of filters (output channels) in the convolution.
            kernel_size: Size of the convolution kernel.
            stride: Stride of the convolution. Default is 1.
            padding: Padding mode for the convolution. Default is 'same'.
            activation: Activation function to use. Default is 'relu'.
            dilation: Dilation rate for the convolution. Default is 1.
            sparsity: Sparsity level of the non-trainable weights. Default is 0.9.
            name: Name of the layer. Default is 'lbc_layer'.
        """
        super(LBC, self).__init__()
        self.nOutputPlane = filters
        self.kW = kernel_size
        self.sparsity = sparsity
        self.LBC = Conv2D(filters, kernel_size=kernel_size, strides=stride, padding=padding,
                          dilation_rate=dilation, activation=activation, use_bias=False, name=name)

    def build(self, input_shape):
        """
        Build the layer.

        Args:
            input_shape: Shape of the input tensor.
        """
        nInputPlane = input_shape[-1]

        with K.name_scope(self.LBC.name):
            self.LBC.build(input_shape)
        anchor_weights = tf.Variable(new_weights_non_trainable(h=self.kW, w=self.kW, num_input=nInputPlane,
                                                               num_output=self.nOutputPlane,
                                                               sparsity=self.sparsity).astype(np.float32),
                                     trainable=False)
        self.LBC.kernel = anchor_weights
        super(LBC, self).build(input_shape)

    def call(self, x):
        """
        Perform the forward pass of the layer.

        Args:
            x: Input tensor.

        Returns:
            Output tensor.
        """
        return self.LBC(x)

    def compute_output_shape(self, input_shape):
        """
        Compute the output shape of the layer.

        Args:
            input_shape: Shape of the input tensor.

        Returns:
            Output shape.
        """
        return self.LBC.compute_output_shape(input_shape)

    def get_config(self):
        """
        Get the configuration of the layer.

        Returns:
            Configuration dictionary.
        """
        config = super(LBC, self).get_config()
        config.update({
            'filters': self.nOutputPlane,
            'kernel_size': self.kW,
            'stride': self.LBC.strides[0],
            'padding': self.LBC.padding,
            'activation': self.LBC.activation,
            'dilation': self.LBC.dilation_rate[0],
            'sparsity': self.sparsity,
            'name': self.LBC.name
        })
        return config

# coding: utf-8


import numpy as np

from DeepNeuralNetwork.scripts.util_activations import sigmoid, relu, sigmoid_backward, relu_backward


class DNN2(object):
    def __init__(self, layers_dims):
        """
        init the object.
        :param layers_dims: list, layers of every layer, layers_dims[0] is the input dim and the last is output dim
        """
        self.layer_dims_ = layers_dims
        self.num_layers_ = len(self.layer_dims_)

        self.parameters_ = {}

        self.layer_cache_ = {}
        self.layer_out_ = []          # A0=X, A1, A2,... AL

    def _initializer(self):
        """
        initialize parameters deep
        :return:
        """
        np.random.seed(3)
        for l in range(self.num_layers_):
            self.parameters_['w' + str(l)] = (np.random.rand(self.layer_dims_[l], self.layer_dims_[l-1]) - 0.5) * 0.01
            self.parameters_['b' + str(l)] = np.zeros((self.layer_dims_[l]), 1)

            assert (self.parameters_['w' + str(l)]) == (self.layer_dims_[l], self.layer_dims_[l-1])
            assert (self.parameters_['w' + str(l)]) == (self.layer_dims_[l], 1)

    def _linear_forward(self, layer):
        """
        Implement the linear part of a layer's forward propation
        :return:
        """
        Z = np.dot(self.parameters_['w' + str(layer)], self.layer_out_[layer]) + self.parameters_['b' + str(layer)]
        assert (Z.shape == self.parameters_['w' + str(layer)].shape[0], self.layer_out_[layer].shape[1])
        return Z

    @staticmethod
    def _linear_activation_forward(Z, activation):
        if activation == "sigmoid":
            A = sigmoid(Z)
        elif activation == "relu":
            A = relu(Z)
        return A

    def _l_model_forward(self, X):
        A = X.copy()
        for l in range(1, self.num_layers_):
            A_prev = A
            Z = self._linear_forward(l)
            self.layer_cache_['layer_' + str(l)] = Z
            A = self._linear_activation_forward(Z, 'relu')

        ZL = self._linear_forward(self.num_layers_)
        self.layer_cache_['layer_' + str(self.num_layers_)] = ZL
        AL = self._linear_activation_forward(ZL, 'sigmoid')

        assert (AL.shape == (self.layer_dims_[-1], X.shape[1]))

        return AL

    @staticmethod
    def _compute_cost(AL, Y):
        m = Y.shape[1]
        cost = np.sum(np.multiply(Y, np.log(AL)) + np.multiply((1 - Y), np.log(1 - AL)), axis=-1) / m
        cost = np.squeeze(cost)
        return cost

    def _linear_backward(self, dZ, layer):
        """
        Implement the linear portion of backward propagation
        :param dZ: Gradient of the cost with respect to the linear output (of the current layer l)
        :layer:
        :return:
        """
        A_prev = self.layer_out_[layer - 1]
        w = self.parameters_['w' + str(layer)]
        b = self.parameters_['b' + str(layer)]
        m = A_prev.shape[1]

        dw = np.matmul(dZ, A_prev.T) / m
        db = np.sum(dZ, axis=-1, keepdims=True) / m
        dA_prev = np.matmul(w.T, dZ)

        assert (dA_prev.shape == A_prev.shape)
        assert (dw.shape == w.shape)
        assert (db.shape == b.shape)

        return dA_prev

    def _linear_activation_backward(self, dA, Z, activation):
        """
        Implement the backward propagation for the LINEAR->ACTIVATION layer
        :param activation:
        :return:
        """
        if activation == 'relu':
            dZ = relu_backward(dA, Z)
        elif activation == 'sigmoid':
            dZ = sigmoid_backward(dA, Z)

    def _l_model_backward(self, AL, Y):
        """
        Implement the backward propagation for the LINEAR->RELU * (L-1) -> LINEAR -> SIGMOID group
        :param AL: probability vector, output of the forward propagation (L_model_forward())
        :param Y: true 'label' vector (containing 0 if non-cat, 1 if cat
        :return:
        """
        grads = {}
        m = m

























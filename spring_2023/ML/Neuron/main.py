import numpy as np

def sigmoid(x):
    # this is out activation function

    return 1/(1+np.exp(-x))


class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias
    
    def feedforward(self, inputs):
        # weighted input adding the bias
        # passing activation func

        total = np.dot(self.weights, inputs) + self.bias

        return sigmoid(total)

class NeuralNetwork:
    def __init__(self):
        # we can also pass it in as parameters
        weights = np.array([0,1])
        bias = 0

        # 2 hidden layers
        self.h1 = Neuron(weights, bias)
        self.h2 = Neuron(weights, bias)
        # the output layer
        self.o1 = Neuron(weights, bias)
    
    def feedforward(self, x):
        out_h1 = self.h1.feedforward(x)
        out_h2 = self.h2.feedforward(x)
        out_o1 = self.o1.feedforward(np.array([out_h1, out_h2]))
        return out_o1

weights = np.array([0,1])
bias = 4

# first example
oneNeuron = Neuron(weights, bias)
xs = np.array([2,3])
print(oneNeuron.feedforward(xs))

# second example
neuralNetwork = NeuralNetwork()
print(neuralNetwork.feedforward(xs))


    
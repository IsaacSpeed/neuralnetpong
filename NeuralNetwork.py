import random
import copy
import math


class NeuralNetwork:
    chance_of_mutation = 0.01
    chance_of_crossover = 0.7

    def __init__(self, number_of_inputs, neuron_layers):
        """ neuron_layers is an array, one int for each layer, and the int represents how many neurons in that layer"""
        self.hidden_layers = []
        self.neuron_layers = neuron_layers
        self.number_of_inputs = number_of_inputs
        self.inputs = []
        for i in range(0, len(neuron_layers)):
            layer = []
            for j in range(0, neuron_layers[i]):
                weights = []
                weight_sum = 0.0
                if i == 0:
                    for k in range(0, self.number_of_inputs):
                        weights.append(random.random() * 2 - 1)
                        weight_sum += weights[k]
                else:
                    for k in range(0, neuron_layers[i-1]):
                        weights.append(random.random() * 2 - 1)
                        weight_sum += weights[k]

                threshold = random.random() * weight_sum * 2

                if i == 0:
                    layer.append(Neuron(self.inputs, number_of_inputs, weights, threshold))
                else:
                    layer.append(Neuron(self.hidden_layers[i-1], len(self.hidden_layers[i-1]), weights, threshold))
            self.hidden_layers.append(layer)

    # this is inefficient
    @classmethod
    def from_other_network(cls, base_network):
        network = cls(base_network.number_of_inputs, base_network.neuron_layers)
        network.inputs = []
        network.hidden_layers = copy.deepcopy(base_network.hidden_layers)

        # set the inputs for the neurons in the network
        for neuron in network.hidden_layers[0]:
            neuron.inputs = network.inputs

        return network

    @classmethod
    def crossover(cls, first_network, second_network):
        child = cls.from_other_network(first_network)

        layer_index = random.randint(0, len(child.hidden_layers) - 1)
        neuron_index = random.randint(0, len(child.hidden_layers[layer_index]) - 1)

        for i in range(layer_index, len(child.hidden_layers)):
            for j in range(neuron_index, len(child.hidden_layers[i])):
                child.hidden_layers[i][j].weights = copy.deepcopy(second_network.hidden_layers[i][j].weights)
                child.hidden_layers[i][j].threshold = second_network.hidden_layers[i][j].threshold
            neuron_index = 0

        # set the inputs for the neurons in the network
        for neuron in child.hidden_layers[0]:
            neuron.inputs = child.inputs

        return child

    def feed_forward(self, inputs):
        del self.inputs[:]
        for an_input in inputs:
            self.inputs.append(InputNeuron(an_input))

        outputs = []

        for neuron in self.hidden_layers[-1]:
            outputs.append(neuron.get_output())

        return outputs

    def mutate(self):
        for layer in self.hidden_layers:
            for neuron in layer:
                chance = random.random()
                if chance <= self.chance_of_mutation:
                    neuron.mutate()

    def print_network(self):
        print("Inputs: ")
        for an_input in self.inputs:
            print(an_input.get_output())

        for i, layer in enumerate(self.hidden_layers):
            print("Layer number {}".format(i + 1))
            for neuron in layer:
                neuron.print_neuron()


class Neuron:
    def __init__(self, inputs, number_of_inputs, weights, threshold):
        self.inputs = inputs
        self.weights = []
        self.threshold = threshold

        for i in range(0, number_of_inputs):
            self.weights.append(weights[i])

    def get_output(self):
        input_sum = 0.0

        for input, weight in zip(self.inputs, self.weights):
            input_sum += input.get_output() * weight

        try:
            denominator = 1 + math.exp(-5*input_sum)
        except OverflowError:
            denominator = float("inf")
        result = 1/denominator - 0.5
        return result

    def mutate(self):
        i = random.randint(0, len(self.weights) - 1)
        change = random.random() * 2 - 1
        self.weights[i] += change

    def print_neuron(self):
        print("Neuron!")

        inputs_string = "["
        for input in self.inputs:
            inputs_string += str(input.get_output()) + ", "
        inputs_string += "]"
        print("Inputs: " + inputs_string)
        print(self.weights)
        print("Threshold: " + str(self.threshold))

        print("Actual value: " + str(self.get_output()))
        print()


class InputNeuron:
    def __init__(self, value):
        self.value = value

    def get_output(self):
        return self.value


class WeightedInput:
    def __init__(self, value_giver, weight):
        self.value_giver = value_giver
        self.weight = weight

    def get_weighted_value(self):
        return self.value_giver.get_output() * self.weight

    def mutate(self):
        self.weight = random.random()

    def __repr__(self):
        return "(Value: {:f}, weight: {:f}, actual value: {:f})".format(self.value_giver.get_output(), self.weight,
                                                                        self.get_weighted_value())

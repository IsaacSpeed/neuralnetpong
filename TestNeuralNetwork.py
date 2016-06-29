from NeuralNetwork import *


def main():
    net = NeuralNetwork(2, [3, 2])
    outputs = net.feed_forward([0, -1])
    net.print_network()

    print(outputs)


if __name__ == '__main__': main()
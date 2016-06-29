from NeuralNetwork import NeuralNetwork

class GeneticAlgorithm:
	chance_of_mutation = 0.01
    chance_of_crossover = 0.7

	def __init__(self, number_of_generations, number_of_population):
		self.number_of_generations = number_of_generations
		self.number_of_population = number_of_population
		self.population = []

		for i in range(0, number_of_population):
			self.population.append(NeuralNetwork(number_of_inputs_for_neural_network, neuron_layers))

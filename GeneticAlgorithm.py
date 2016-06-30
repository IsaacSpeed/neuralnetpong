from NeuralNetPlayer import NeuralNetPlayer
import random


class GeneticAlgorithm:
    chance_of_mutation = 0.01
    chance_of_crossover = 0.7
    number_of_inputs_for_neural_network = 2
    neuron_layers = 1

    def __init__(self, number_of_generations, number_of_population):
        self.number_of_generations = number_of_generations
        self.number_of_population = number_of_population
        self.population = []
        self.generation_counter = 1

        for i in range(0, number_of_population):
            self.population.append(NeuralNetPlayer.empty())

    def next_generation(self):
        if self.generation_counter >= self.number_of_generations:
            return False

        first_individual = self.roulette()
        second_individual = self.roulette()

        mutation_chance = random.random()
        crossover_chance = random.random()

        if crossover_chance <= self.chance_of_crossover:
            child = NeuralNetPlayer.crossover(first_individual, second_individual)
        else:
            child = NeuralNetPlayer.from_other(first_individual)

        if mutation_chance <= self.chance_of_mutation:
            child.mutate()

        self.generation_counter += 1
        return True

    def roulette(self):
        weighted_array = []
        for i in range(0, len(self.population)):
            for j in range(0, self.population[i].get_fitness_score()):
                weighted_array.append(i)

        index = random.randint(0, len(weighted_array) - 1)

        return self.population[weighted_array[index]]

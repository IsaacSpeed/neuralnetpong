from NeuralNetPlayer import NeuralNetPlayer
import random


class GeneticAlgorithm:
    chance_of_mutation = 0.00
    chance_of_crossover = 0.0
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

        sum_fitness = 0.0
        for i in range(0, len(self.population)):
            print("Player {:} {:} has a score of {:}".format(i, self.population[i], self.population[i].get_fitness_score()))
            sum_fitness += self.population[i].get_fitness_score()
        print("Average fitness: {:}".format(sum_fitness / len(self.population)))

        new_population = []

        while len(new_population) < self.number_of_population:
            first_individual = self.roulette()
            second_individual = self.roulette()

            mutation_chance = random.random()
            crossover_chance = random.random()

            #if crossover_chance <= self.chance_of_crossover:
            child = NeuralNetPlayer.crossover(first_individual, second_individual)
            #else:
            #child = NeuralNetPlayer.from_other(first_individual)

            if mutation_chance <= self.chance_of_mutation:
                child.mutate()

            new_population.append(child)

        self.population = new_population

        self.generation_counter += 1
        return True

    def roulette(self):
        weighted_array = []
        for i in range(0, len(self.population)):
            for j in range(0, self.population[i].get_fitness_score()):
                weighted_array.append(i)

        index = random.randint(0, len(weighted_array) - 1)

        individual_index = weighted_array[index]
        return self.population[individual_index]

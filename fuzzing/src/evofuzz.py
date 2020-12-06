# Evolutionary Fuzzer
# 12/5/2020
# reevesbra@outlook.com

'''
Terminology
 population: all inputs that have been explored
 fitness: likeliness individual will reproduce successfully
 recombination: two individuals are sliced then combined to create two offspring inputs
                e.g. A and B are split at point P. A1 is combined with B2, A2 is combined with B1
 culling: member with low fitness are eliminated from population
 carrying capacity: maximum size of population
 seed: some choice of initial inputs
 generations: number of cycles to run fuzzer
'''

import sys
import numpy as np
import mutation

coverage_dict = {}
important_samples = []

def cgi_decode(input):
    ''' Parameters
        ----------
        input: encoded string
            
        Returns
        _______
        output: decoded string
    '''
    output = ""
    i = 0

    while i < len(input):
        current_char = input[i]
        if current_char == "+":
            # replace '+' with ' '
            output += " "
        elif current_char == "%":
            # replace '%xx' with char of hex number xx
            digit_high, digit_low = input[i + 1], input[i + 2]
            i += 2
            try:
                v = int(digit_high, 16)*16 + int(digit_low, 16)
                output += chr(v)
            except:
                raise ValueError("Invalid Input")
        else:
            output += current_char
        i += 1
    return output

def line_tracer(frame, event, arg):
    ''' Parameters
        ----------
        self: EvolutionaryFuzzer object
        frame: current stack frame
        event: 'call', 'line', 'return', 'exception', 'opcode'
        arg: argument passed to event type
            
        Returns
        _______
        line_tracer: reference to local trace function
    '''
    if event == "line":
        lineno = frame.f_lineno
        global coverage
        coverage.add(lineno)
    return line_tracer

def record_coverage(function, s):
    ''' Parameters
        ----------
        self: EvolutionaryFuzzer object
        function: function to trace
        s: string to execute on function
            
        Returns
        _______
        coverage: set containing lines of code executed
    '''
    global coverage
    coverage = set([])
    sys.settrace(line_tracer)
    function(s)
    sys.settrace(None)
    coverage = frozenset(coverage)
    return coverage

def add_to_coverage_dict(value, coverage):
    ''' Parameters
        ----------
        self: EvolutionaryFuzzer object
        value: covered string
        coverage: set containing lines of code executed
            
        Returns
        _______
        None
    '''
    if coverage_dict.get(coverage, 0) == 0:
        important_samples.append(value)
    coverage_dict[coverage] = coverage_dict.get(coverage, 0) + 1

class Individual:

    def __init__(self, value):
        ''' Parameters
            ----------
            self: Individual object
            value: string value
            
            Returns
            _______
            None
        '''
        self.value = value

        try:
            self.coverage = record_coverage(cgi_decode, self.value)
        except:
            self.coverage = str(sys.exc_info()[0])
            print("Got Error " + str(sys.exc_info()[0]) + " for input " + self.value)

        add_to_coverage_dict(self.value, self.coverage)
        self.fitness = None

    def print_info(self):
        ''' Parameters
            ----------
            self: Individual object
            
            Returns
            _______
            None
        '''
        print(self.value)
        print(self.coverage)
        print(self.fitness)

    def compute_fitness(self):
        ''' Parameters
            ----------
            self: Individual object
            
            Returns
            _______
            None
        '''
        self.fitness = 1/coverage_dict[self.coverage]

class EvolutionaryFuzzer:

    def __init__(self, carrying_capacity, seed, mutation_prob):
        self.carrying_capacity = carrying_capacity
        self.seed = seed
        self.population = [Individual(x) for x in seed]
        self.mutation_prob = mutation_prob
        self.mutator = mutation.Mutator()
        self.update_fitness_scores(self.population)

    def update_fitness_scores(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            None
        '''
        for individual in population:
            individual.compute_fitness()

    def print_population_info(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            None
        '''
        for individual in population:
            individual.print_info()

    def get_fitness_scores(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            fitness_distribution: distribution of fitness scores
        '''
        fitness_distribution = np.array([x.fitness for x in population])
        fitness_distribution = fitness_distribution/sum(fitness_distribution)
        return fitness_distribution

    def sample_pair_for_reproduction(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            individual1: first individual of pair
            individual2: second individual of pair
        '''
        fitness_distribution = self.get_fitness_scores(population)
        index1 = np.random.choice(len(fitness_distribution), p=fitness_distribution)
        individual1 = population[index1]
        index2 = np.random.choice(len(fitness_distribution), p=fitness_distribution)
        individual2 = population[index2]
        return individual1, individual2

    def recombine(self, individual1, individual2):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            individual1: first individual of pair
            individual2: second individual of pair
            
            Returns
            _______
            offspring of individual1
            offspring of individual2
        '''
        L1 = len(individual1.value)
        L2 = len(individual2.value)
        L = min(L1, L2)
        locus = np.random.randint(L)
        offspring1_value = individual1.value[:locus] + individual2.value[locus:]
        offspring2_value = individual2.value[:locus] + individual1.value[locus:]
        return Individual(offspring1_value), Individual(offspring2_value)

    def recombination_phase(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            new_population: population of recombining
        '''
        new_population = population.copy()
        population_size = len(population)
        number_of_recombinations = population_size//2
        for i in range(number_of_recombinations):
            individual1, individual2 = self.sample_pair_for_reproduction(population)
            try:
                offspring1, offspring2 = self.recombine(individual1, individual2)
                new_population.append(offspring1)
                new_population.append(offspring2)
            except ValueError:
                pass
        self.update_fitness_scores(new_population)
        return new_population

    def mutation_phase(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            population: population after mutations
        '''
        for i in range(len(population)):
            individual = population[i]
            mutate_this_individual = np.random.choice(2, p=[1 - self.mutation_prob, self.mutation_prob])
            if mutate_this_individual:
                try:
                    mutated_individual = Individual(self.mutator.mutate(individual.value))
                    population[i] = mutated_individual
                except ValueError:
                    pass
        self.update_fitness_scores(population)
        return population

    def culling_phase(self, population):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            population: current population of individuals
            
            Returns
            _______
            new_population: population after culling
        '''
        population_size = len(population)
        N = min(self.carrying_capacity, population_size)
        fitness_distribution = self.get_fitness_scores(population)
        new_population = list(np.random.choice(population, N, p=fitness_distribution))
        self.update_fitness_scores(new_population)
        return new_population

    def fuzz(self, number_of_generations):
        ''' Parameters
            ----------
            self: EvolutionaryFuzzer object
            
            Returns
            _______
            important_samples:
            coverage_dict: 
        '''
        for i in range(number_of_generations):
            self.population = self.recombination_phase(self.population)
            self.population = self.mutation_phase(self.population)
            self.population = self.culling_phase(self.population)

        return important_samples, coverage_dict













 
























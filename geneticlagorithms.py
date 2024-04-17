import random

POP_SIZE = 500
MUT_RATE = 0.1
TARGET = 'rayan ali'
GENES = ' abcdefghijklmnopqrstuvwxyz'


def initialize_pop(TARGET):
    population = list()
    tar_len = len(TARGET)

    for i in range(POP_SIZE):
        temp = list()
        for j in range(tar_len):
            temp.append(random.choice(GENES))
        population.append(temp)

    return population


def crossover(selected_chromo, CHROMO_LEN, population):
    offspring_cross = []
    for i in range(int(POP_SIZE)):
        parent1 = random.choice(selected_chromo)
        parent2 = random.choice(population[:int(POP_SIZE * 50)])

        p1 = parent1[0]
        p2 = parent2[0]

        '''
        #original
        crossover_point = random.randint(1, CHROMO_LEN - 1)
        child = p1[:crossover_point] + p2[crossover_point:]
        offspring_cross.extend([child])
        '''

        # Two-point crossover: Choose two crossover points
        crossover_point1 = random.randint(1, CHROMO_LEN - 2)  # Ensure there's at least one gene between the points
        crossover_point2 = random.randint(crossover_point1 + 1, CHROMO_LEN - 1)

        # Swap segments between the two parents
        child = p1[:crossover_point1] + p2[crossover_point1:crossover_point2] + p1[crossover_point2:]

        offspring_cross.append(child)  # Use append instead of extend with a list containing a single element
    return offspring_cross


def mutate(offspring, MUT_RATE):
    mutated_offspring = []

    '''
    #original
    for arr in offspring:
        for i in range(len(arr)):
            if random.random() < MUT_RATE:
                arr[i] = random.choice(GENES)
    '''
    #swap mutation
    for arr in offspring:
        for i in range(len(arr) - 1):  # Iterate up to len(arr) - 1 to avoid swapping the last element with itself
            if random.random() < MUT_RATE:
                j = random.randint(i + 1, len(arr) - 1)  # Choose a swap partner (j) that is different from i

                # Swap elements at positions i and j
                arr[i], arr[j] = arr[j], arr[i]

        mutated_offspring.append(arr)
    return mutated_offspring


def selection(population, TARGET):
    sorted_chromo_pop = sorted(population, key=lambda x: x[1])
    return sorted_chromo_pop[:int(0.5 * POP_SIZE)]


def fitness_cal(TARGET, chromo_from_pop):
    difference = 0
    for tar_char, chromo_char in zip(TARGET, chromo_from_pop):
        if tar_char != chromo_char:
            difference += 1

    return [chromo_from_pop, difference]


def replace(new_gen, population):
    for _ in range(len(population)):
        if population[_][1] > new_gen[_][1]:
            population[_][0] = new_gen[_][0]
            population[_][1] = new_gen[_][1]
    return population


def main(POP_SIZE, MUT_RATE, TARGET, GENES):
    # 1) initialize population
    initial_population = initialize_pop(TARGET)
    found = False
    population = []
    generation = 1

    # 2) Calculating the fitness for the current population
    for _ in range(len(initial_population)):
        population.append(fitness_cal(TARGET, initial_population[_]))

    # now population has 2 things, [chromosome, fitness]
    # 3) now we loop until TARGET is found
    while not found:

        # 3.1) select best people from current population
        selected = selection(population, TARGET)

        # 3.2) mate parents to make new generation
        population = sorted(population, key=lambda x: x[1])
        crossovered = crossover(selected, len(TARGET), population)

        # 3.3) mutating the childeren to diversfy the new generation
        mutated = mutate(crossovered, MUT_RATE)

        new_gen = []
        for _ in mutated:
            new_gen.append(fitness_cal(TARGET, _))

        # 3.4) replacement of bad population with new generation
        # we sort here first to compare the least fit population with the most fit new_gen

        population = replace(new_gen, population)

        if (population[0][1] == 0):
            print('Target found')
            print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(
                population[0][1]))
            break
        print('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(
            population[0][1]))
        generation += 1


main(POP_SIZE, MUT_RATE, TARGET, GENES)
import numpy as np
import matplotlib.pyplot as plt

DNA_SIZE = 10
POP_SIZE = 100
CROSS_RATE = 0.8
MUTATION_RATE = 0.003
N_GENERATIONS = 200
X_BOUND = [0, 5]


# F(x)
def target_function(x):
    return np.sin(10 * x) * x + np.cos(2 * x) * x


# find non-zero fitness for selection
def get_fitness(pred):
    return pred + 1e-3 - np.min(pred)


def decode_gene(pop):
    return pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * X_BOUND[1]


def select(pop, fitness):
    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True,
                           p=fitness / fitness.sum())
    return pop[idx]


def crossover(parent, pop):
    if np.random.rand() < CROSS_RATE:
        i_ = np.random.randint(0, POP_SIZE, size=1)
        cross_points = np.random.randint(0, 2, size=DNA_SIZE).astype(np.bool)
        parent[cross_points] = pop[i_, cross_points]
    return parent


def mutate(child):
    for point in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            child[point] = 1 if child[point] == 0 else 0
    return child


if __name__ == '__main__':
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE))
    plt.ion()
    x = np.linspace(*X_BOUND, 200)
    plt.plot(x, target_function(x))

    for _ in range(N_GENERATIONS):
        F_value = target_function(decode_gene(pop))

        if 'sca' in globals():
            sca.remove()
        sca = plt.scatter(decode_gene(pop), F_value, s=200, lw=10, c='red', alpha=0.5)
        plt.pause(0.05)

        fitness = get_fitness(F_value)
        print("Most fitted DNA: ", pop[np.argmax(fitness), :])
        pop = select(pop, fitness)
        pop_copy = pop.copy()
        for parent in pop:
            child = crossover(parent, pop_copy)
            child = mutate(child)
            parent[:] = child

plt.ioff()
plt.show()

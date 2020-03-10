from keras.models import Sequential
from keras.layers import Dense
import keras
from operator import itemgetter
import random
import numpy as np

class Genetic(object):
    ##### TODO ADAPT CODE FOR class

    def __init__(self, nb_individual):
        self.pop=[]
        self.mean_fitness = []
        self.nb_generation = 0
        self.score_list = []
        self.create_population(nb_individual)


    def create_population(self, nb_individual):
        for i in range(nb_individual):
            nn = create_model()
            self.pop.append(nn)


    def get_average_fitness(self):
        return np.mean(self.score_list)

    @property
    def get_pop(self):
        return self.pop

    @property
    def set_score(self, _score):
        self.score_list=_score

    def selection(self, selection = 0.4):
        try :
            score_sorted, model_sorted = zip(*sorted(zip(self.score_list, self.pop), key = lambda v: (v[0], random.random(), v[1]), reverse=True))
        except :
            print(len(self.score_list))
            print(len(self.pop))
            print(self.score_list)
        retain = selection * len(self.pop)
        # print(retain)
        model_sorted = model_sorted[:int(retain)]

        return model_sorted

    def mutation(self, mutation_rate = 0.01):
        new_pop = []
        for individual in self.pop:
            if random.random() < mutation_rate :
                for layer in range(len(individual.layers)):

                    weight = individual.layers[layer].get_weights()
                    bias = weight[1]

                    flat_weight = weight[0].flatten()
                    shape_layer = weight[0].shape
                    nb_mutations = np.random.choice(range(len(flat_weight)))

                    cases = np.random.choice(range(len(flat_weight)), nb_mutations)

                    for i in cases:
                        flat_weight[i] = np.random.uniform(-1, 1, 1)
                    weight = np.reshape(flat_weight, shape_layer)
                    c=[]
                    c.append(weight)
                    c.append(bias)
                    individual.layers[layer].set_weights(c)
            new_pop.append(individual)

        return new_pop

    def crossover(self, a, b):
        child = create_model()
        for layer in range(len(a.layers)):

            weight = a.layers[layer].get_weights()
            shape_layer = weight[0].shape

            weights_a = np.array(a.layers[layer].get_weights()[0]).flatten()
            weights_b = np.array(b.layers[layer].get_weights()[0]).flatten()

            bias_a = np.array(a.layers[layer].get_weights()[1]).flatten()
            bias_b = np.array(b.layers[layer].get_weights()[1]).flatten()

            new_w = np.array(np.random.choice(np.concatenate([weights_a, weights_b]), len(weights_a)))
            new_w = np.reshape(new_w, shape_layer)

            # new_b = np.array(np.random.choice(np.concatenate([bias_a, bias_b]), len(bias_a) ))
            new_b = np.array(np.zeros(len(bias_a)))
            c = []
            c.append(new_w)
            c.append(new_b)

            child.layers[layer].set_weights(c)
        return child

    def evolve(self, _new_gen):
        self.nb_generation +=1
        self.mean_fitness.append(self.get_average_fitness())
        model_sorted = self.selection()
        childs = []
        for i in range(_new_gen-2):
            father = np.random.choice(range(len(model_sorted)))
            mother = np.random.choice(range(len(model_sorted)))
            childs.append(self.crossover(model_sorted[mother], model_sorted[father]))
        childs.append(model_sorted[0])
        childs.append(model_sorted[1])
        self.pop = childs
        self.pop = self.mutation()



def create_model():
    model = Sequential()
    init_weight = keras.initializers.RandomUniform(minval=-1, maxval=1, seed=None)
    model.add(Dense(32, activation = 'relu',input_shape=(1,8), kernel_initializer= init_weight))
    model.add(Dense(32, activation = 'relu', kernel_initializer= init_weight))
    # model.add(Dense(32, activation = 'relu', kernel_initializer= init_weight))
    model.add(Dense(4, activation = 'softmax'))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # weights = [np.random.uniform((*w.shape)) for w in model.get_weights()]
    # model.set_weights(weights)

    return model

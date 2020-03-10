from threading import Thread
from snake import *
from genetic_algorithm import *
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.models import model_from_json

class Instance(Thread):

    def __init__(self, _model):
        Thread.__init__(self)
        self.model = _model
        self.score = 0
        self.mean_dist = 0
        self.fitness = 0

    def run(self):
        App = GameApp(model = self.model, auto = 1)
        App.start()
        self.score = App.score
        self.mean_dist = App.mean_dist
        self.fitness = self.score - self.mean_dist + 1
        # print('Score : ', self.score,'Mean dist : ', self.mean_dist, 'Fitness :', self.fitness)



class Train_genetic(object):

    def __init__(self, nb_generation = 30, nb_individual = 50):
        self.gen = Genetic(nb_individual)
        self.nb_individual = nb_individual

        self.pop = self.gen.pop

        self.nb_generation = nb_generation
        self.thread = []
        self.fitness = []
        self.highest_fitness = []
        self.train()

    def natural_selection(self):
        for i in range(self.nb_individual):
            self.thread.append(Instance(self.pop[i]))

        for i in range(self.nb_individual):
            self.thread[i].start()

        for i in range(self.nb_individual):
            self.thread[i].join()
            self.fitness.append(self.thread[i].fitness)

        self.highest_fitness.append(np.max(self.fitness))
        self.gen.score_list = self.fitness
        self.fitness = []
        self.gen.evolve(self.nb_individual)
        self.pop = self.gen.pop

    def train(self):

        for i in range(self.nb_generation):
            print('Generation {} selection...'.format(i))
            self.natural_selection()
            self.thread = []

        model = self.gen.selection()
        model = model[0]
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        model.save_weights("model.h5")

        self.graph()


    def graph(self):
        plt.plot(range(self.nb_generation), self.gen.mean_fitness, 'r', label = 'Average fitness')
        plt.plot(range(self.nb_generation), self.highest_fitness, 'b', label = 'Max score')
        plt.legend()
        plt.xlabel('Generation')
        plt.ylabel('Average fitness')
        plt.title('Evolution of average fitness')
        plt.show()


Train_genetic()

# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
#
# loaded_model.load_weights("model.h5")
#
# App = GameApp(model = loaded_model)
# App.start()
# a = [4, 5, 1, 2, 4, 5]
# b = [1, 2, 3, 4, 5, 6]
# print((*sorted(zip(a, b), key = lambda v: (v[0], random.random(), v[1]), reverse=True)))
# thread_1 = Instance(m1)
# thread_2 = Instance(m2)
#
# thread_1.start()
# thread_2.start()
#
# thread_1.join()
# thread_2.join()

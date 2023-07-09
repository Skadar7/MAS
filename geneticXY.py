import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import vis


class Genetic:
    def __init__(self, size, min_value, max_value, N, mut_rate, tour_size):
        self.pop_size = size
        self.min_value = min_value
        self.max_value = max_value
        self.num_generations = N
        self.mut_rate = mut_rate
        self.tour_size = tour_size

    def fitness_function(self, x, y):
        return 10 * x ** 2 + 3 * x * y + y ** 2 + 10 * y

    # Создаем начальную популяцию
    def create_population(self):
        population = np.random.uniform(low=self.min_value, high=self.max_value, size=(self.pop_size, 2))
        return population

    # Оцениваем приспособленность индивидуумов
    def evaluate_fitness(self, population):
        fitness_scores = self.fitness_function(population[:, 0], population[:, 1])
        return fitness_scores

    # Выбор родителей на основе турнирного отбора
    def selection(self, population, fitness_scores):
        parents = []
        for _ in range(2):
            tournament_indices = np.random.choice(len(population), size=self.tour_size, replace=False)
            tournament_fitness = fitness_scores[tournament_indices]
            winner_index = np.argmin(tournament_fitness)
            winner = population[tournament_indices[winner_index]]
            parents.append(winner)
        return parents

    # Скрещиваем родителей
    def crossover(self, parents):
        child = np.mean(parents, axis=0)
        return child

    # Мутация индивидуумов
    def mutate(self, individual):
        if random.random() < self.mut_rate:
            individual[0] = random.uniform(self.min_value, self.max_value)
            individual[1] = random.uniform(self.min_value, self.max_value)
        return individual

    # Замена старой популяции на новую
    def replace_population(self, population, offspring):
        population = offspring
        return population

    def genetic_algorithm(self):
        population = self.create_population()
        best_fitness = float('inf')  # Лучшее значение функции
        fitness_progress = []
        history = []
        cnt = 0

        for generation in range(self.num_generations):
            fitness_scores = self.evaluate_fitness(population)
            parents = self.selection(population, fitness_scores)
            offspring = np.zeros_like(population)

            for i in range(self.pop_size):
                child = self.crossover(parents)
                child = self.mutate(child)
                offspring[i] = child

            population = self.replace_population(population, offspring)
            current_best_fitness = np.min(fitness_scores)
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                cnt = 0
            elif current_best_fitness == best_fitness:
                cnt += 1

            if cnt == 20:
                break

            best_individual = population[np.argmin(fitness_scores)]
            history.append((*best_individual, best_fitness))
            # print(f"Generation {generation+1}: Best individual = {best_individual}, Best fitness = {best_fitness}")

            fitness_progress.append(best_fitness)

        # Находим индивидуум с наименьшим значением функции
        best_individual = population[np.argmin(fitness_scores)]
        history.append((*best_individual, best_fitness))
        return best_individual, fitness_progress, history


g = Genetic(500, -10, 10, 300, 0.2, 100)
best_individual, fitness_progress, history = g.genetic_algorithm()
print("Best individual:", best_individual)
print("Best fitness:", g.fitness_function(best_individual[0], best_individual[1]))
#vis.visualize(history)
plt.plot(fitness_progress)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.axhline(y=g.fitness_function(0.967764, -6.445815), color='r', linestyle='--', label='Real Minimum')
plt.legend()
plt.show()

import random
import matplotlib.pyplot as plt
import vis


class Evolution:

    def __init__(self, pop_size, N, mut_rate, elite):
        self.pop_size = pop_size
        self.num_gen = N
        self.mut_rate = mut_rate
        self.elite = elite
        # Инициализация популяции
        self.population = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(self.pop_size)]
        self.x_progress = []
        self.y_progress = []
        self.fitness_progress = []
        self.history = []

    def fitness_function(self, x, y):
        return 10 * x ** 2 + 3 * x * y + y ** 2 + 10 * y

    # Умножение гена на коэффициент (идиоадаптации)
    def multiply_gene(self, individual):
        return individual * 0.9

    # Увеличение гена на константу (идиоадаптации)
    def increase_gene(self, individual):
        return individual + 0.1

    # Естественная мутация
    def natural_mutation(self, individual):
        mutation_type = random.randint(0, 2)
        
        if mutation_type == 0:
            mutation_factor = random.uniform(0.5, 1.5)
            individual = individual * mutation_factor
        elif mutation_type == 1:
            mutation_offset = random.uniform(-1, 1)
            individual = individual + mutation_offset
        else:
            individual = -individual
        
        return individual
    
    def evulotion_algorithm(self):
        for generation in range(self.num_gen):
            # Вычисление значения функции для каждого индивида
            fitness_scores = [self.fitness_function(x, y) for x, y in self.population]
            
            # Нахождение наилучшего индивида
            best_individual = self.population[fitness_scores.index(min(fitness_scores))]
            best_fitness = min(fitness_scores)
            
            print(f"Поколение {generation}: Лучшее значение функции = {best_fitness}, Лучший индивид = {best_individual}")
            
            self.history.append((*best_individual, best_fitness))
            self.x_progress.append(best_individual[0])
            self.y_progress.append(best_individual[1])
            self.fitness_progress.append(best_fitness)
            
            total_fitness = sum(fitness_scores)
            relative_fitness = [fitness / total_fitness for fitness in fitness_scores]
            
            num_elites = int(self.elite * self.pop_size)
            
            new_population = []
            
            # Добавление элитных индивидов в новую популяцию
            elites_indices = sorted(range(len(relative_fitness)), key=lambda k: relative_fitness[k])[:num_elites]
            for index in elites_indices:
                new_population.append(self.population[index])
            
            # Мутация предыдущего поколения
            for index in range(num_elites, self.pop_size):
                individual = self.population[index]
                
                if random.random() < self.mut_rate:
                    # Естественная мутация
                    individual = (self.natural_mutation(individual[0]), self.natural_mutation(individual[1]))
                else:
                    # Идиоадаптация
                    if random.random() <= 0.5:
                        individual = (self.multiply_gene(individual[0]), self.increase_gene(individual[1]))
                    else:
                        individual = (self.increase_gene(individual[0]), self.multiply_gene(individual[1]))
                
                new_population.append(individual)
            
            self.population = new_population
        
        # Нахождение наилучшего индивида в финальной популяции
        fitness_scores = [self.fitness_function(x, y) for x, y in self.population]
        best_individual = self.population[fitness_scores.index(min(fitness_scores))]
        best_fitness = min(fitness_scores)
        self.history.append((*best_individual, best_fitness))

        print("Результаты поиска:")
        print(f"Лучшее значение функции = {best_fitness}")
        print(f"Лучший индивид = {best_individual}")

        return self.history, self.fitness_progress
        

real_minimum = (0.967764, -6.445815)
evol = Evolution(500, 200, 0.2, 0.15)
history, fitness_progress = evol.evulotion_algorithm()
vis.visualize(history)
plt.plot(fitness_progress)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.axhline(y=evol.fitness_function(*real_minimum), color='r', linestyle='--', label='Real Minimum')
plt.legend()
plt.show()
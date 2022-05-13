import cv2
import random as r
import numpy as np
from skimage.metrics import mean_squared_error
from copy import deepcopy
import multiprocessing as mp

img = cv2.imread('img/jog.jpg')
img = cv2.resize(img, None, None, 0.25, 0.25, cv2.INTER_CUBIC)
height, width, _ = img.shape
img = img[:min(height, width), :min(height, width)]
SIZE = height  # = width

n_init_gene = 50  # 한 그림에 들어갈 gene 처음개수
n_genomes = 50  # 한 세대에 들어있는 genome
prob_mutation = 0.01
prob_add = 0.3
prob_remove = 0.2

min_rad, max_rad = 5, 15
show_iter = 10


class Gene():
    def __init__(self):
        self.center = np.array([r.randint(0, SIZE) for _ in range(2)])
        self.radius = np.array([r.randint(min_rad, max_rad) for _ in range(1)])
        self.color = np.array([r.randint(0, 255) for _ in range(3)])

    def mutate(self):
        amount_mutate = max(1, int(r.gauss(15, 4))) / 100

        for target in ['center', 'radius', 'color']:
            if target == 'center':
                prob = r.random()
                if prob >= 0.33: continue
                temp = []
                for c in self.center:
                    temp.append(np.clip(r.randint(int(c * (1 - amount_mutate)), int(c * (1 + amount_mutate))), 0, SIZE))
                self.center = np.array(temp)

            elif target == 'radius':
                prob = r.random()
                if prob >= 0.33: continue
                temp = []
                for c in self.radius:
                    temp.append(np.clip(r.randint(int(c * (1 - amount_mutate)), int(c * (1 + amount_mutate))), min_rad,
                                        max_rad))
                self.radius = np.array(temp)

            elif target == 'color':
                prob = r.random()
                if prob >= 0.33: continue
                temp = []
                for c in self.color:
                    temp.append(np.clip(r.randint(int(c * (1 - amount_mutate)), int(c * (1 + amount_mutate))), 0, 255))
                self.color = np.array(temp)


def compute_fitness(genome):
    genome_image = np.full((SIZE, SIZE, 3), dtype=np.uint8, fill_value=255)

    for gene in genome:
        cv2.circle(genome_image, center=tuple(gene.center), radius=gene.radius[0], color=tuple(map(int, gene.color)),
                   thickness=-1)
    fitness = 255 / mean_squared_error(genome_image, img)

    return fitness, genome_image


def generate_next_genome(old_genome):
    new_genome = deepcopy(old_genome)
    if len(new_genome) < 200:
        for gene in new_genome:
            if r.random() < prob_mutation:
                gene.mutate()
    else:
        for gene in r.sample(new_genome, k=int(len(new_genome) * prob_mutation)):
            gene.mutate()

    if r.random() < prob_add:
        new_genome.append(Gene())
    if r.random() < prob_remove:
        new_genome.remove(r.choice(new_genome))

    return new_genome


def get_next_fitness(old_genome):
    new_genome = generate_next_genome(old_genome)
    fitness, genome_image = compute_fitness(new_genome)
    return fitness, genome_image, new_genome


if __name__ == '__main__':
    p = mp.Pool(mp.cpu_count() - 1)

    cur_genome = [Gene() for _ in range(n_init_gene)]
    nth = 0

    while True:
        try:
            cur_population = [deepcopy(cur_genome)] * n_genomes
            result = p.map(get_next_fitness, cur_population)
        except KeyboardInterrupt:
            p.close()
            break
        result.sort(key=lambda x: -x[0])
        cur_fitness, cur_image, cur_genome = result[0]  # best fitness -> cur

        print(f'Generation #{nth}, Score : {cur_fitness}')
        if nth % show_iter == 0:
            cur_image = cv2.resize(cur_image, None, None, 2, 2, cv2.INTER_CUBIC)
            cv2.imshow('best out', cur_image)
            cv2.waitKey(1)

        nth += 1

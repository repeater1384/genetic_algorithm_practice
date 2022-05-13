import cv2
import random as r
import numpy as np
from skimage.metrics import mean_squared_error

img = cv2.imread('jingjingyee.jfif')
height, width, _ = img.shape
img = img[:min(height, width), :min(height, width)]
SIZE = height  # = width

n_population = 50
prob_mutation = 0.01
prob_add = 0.3
prob_remove = 0.2

min_rad, max_rad = 5, 15


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
        cv2.circle(genome_image, center=tuple(gene.center), radius=gene.radius[0], color=tuple(gene.color),
                   thickness=-1)


from mpi4py import MPI
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm

# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth) / self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex, smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations
    

# Fonction pour calculer la partie d'image assignée à un processus
def compute_chunk(start_y, end_y):
    chunk = np.empty((end_y - start_y, width), dtype=np.double)
    for i, y in enumerate(range(start_y, end_y)):
        for x in range(width):
            c = complex(-2. + scaleX * x, -1.125 + scaleY * y)
            chunk[i, x] = mandelbrot_set.convergence(c, smooth=True)
    return chunk

# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

scaleX = 3. / width
scaleY = 2.25 / height

# Temps d'exécution parallèle
parallel_time_start = MPI.Wtime()

# Stratégie maître-esclave
if rank == 0:
    # Maître : divise les tâches entre les esclaves
    for i in range(1, size):
        start_y = i * (height // size) + min(i, height % size)
        end_y = start_y + (height // size) + (1 if i < height % size else 0)
        comm.send((start_y, end_y), dest=i)
else:
    # Esclave : reçoit les tâches du maître et effectue le calcul
    start_y, end_y = comm.recv()
    local_convergence = compute_chunk(start_y, end_y)
    comm.send((start_y, end_y, local_convergence), dest=0)

# Maître : récupère les résultats des esclaves
if rank == 0:
    final_convergence = np.empty((height, width), dtype=np.double)
    for i in range(1, size):
        start_y, end_y, local_convergence = comm.recv(source=i)
        final_convergence[start_y:end_y, :] = local_convergence

    parallel_time_end = MPI.Wtime()
    parallel_time = parallel_time_end - parallel_time_start
    print(f"Parallel execution time: {parallel_time}")

    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(final_convergence.T)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()
    
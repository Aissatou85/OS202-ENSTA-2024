from mpi4py import MPI
import numpy as np

# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Dimension du problème
dim = 120

# Calcul du nombre de lignes par tâche
Nloc = dim // size

# Répartition des lignes entre les tâches
start_row = rank * Nloc
end_row = start_row + Nloc

# Initialisation de la matrice A sur chaque tâche
A_local = np.array([[(i+j) % dim+1. for j in range(dim)] for i in range(start_row, end_row)])
u = np.array([i+1. for i in range(dim)])
# Produit matrice-vecteur local
v_local = A_local.dot(u)
v_global = np.empty(dim, dtype=float)
comm.Allgather(v_local, v_global)

print(f"Matrice A (Tâche {rank}):\n{A_local}")
print(f"Vecteur u (Tâche {rank}): {u}")
print(f"Vecteur v_local (Tâche {rank}): {v_local}")
print(f"Vecteur v_global (Tâche {rank}): {v_global}")


from mpi4py import MPI
import numpy as np

# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Dimension du problème
dim = 120

# Calcul du nombre de colonnes par tâche
Nloc = dim // size

# Répartition des colonnes entre les tâches
start_col = rank * Nloc 
end_col = start_col + Nloc

# Initialisation de la matrice locale A pour chaque tâche
A_local = np.array([[(i+j) % dim+1. for j in range(start_col, end_col)] for i in range(dim)])
A_local = A_local.T
u = np.array([i+1. for i in range(dim)])

# Produit matrice-vecteur local
v_local = A_local.dot(u)
v_global = np.empty(dim, dtype=float)

#On utilise Allgather car on veut que toutes les tâches disposent du résulat final
comm.Allgather(v_local, v_global)

print(f"Matrice A (Tache {rank}):\n{A_local}")
print(f"Vecteur u (Tache {rank}): {u}")
print(f"Vecteur v_local (Tache {rank}): {v_local}")
print(f"Vecteur v_global (Tache {rank}): {v_global}")

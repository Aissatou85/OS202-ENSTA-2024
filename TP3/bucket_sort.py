from mpi4py import MPI
import numpy as np
from time import time


# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


#processus maitre
def master_process(data):
    min_value = min(data)
    max_value= max(data)
    bucket_size = (max_value - min_value) / (size-1)
    
    #Envoie des buckets aux processus esclaves
    for i in range(1,size):
        start = min_value + (i-1)*bucket_size
        end = min_value + i*bucket_size
        bucket_data = [x for x in data if start <= x < end]
        comm.send(bucket_data, dest=i)
        
    #Reception des données triées des processus esclaves
    sorted_data = []
    for i in range(1,size):
        sorted_bucket= comm.recv(source = i)
        sorted_data.extend(sorted_bucket)
    
    return sorted_data

def slave_process():
    #reception des données du processus maître
    bucket = comm.recv(source=0)
    
    #Tri local
    sorted_bucket = sorted(bucket)
    
    #Envoi des données triées au processus maître
    comm.send(sorted_bucket, dest=0)
    

if rank == 0:
    #Génération du tableau de nombres arbitraires
    data = np.random.randint(0,100, size=20)
    sorted_data = master_process(data)
    print("Le tableau Initial:", data)
    print("Le tableau trié:", sorted_data)
    
else:
    slave_process()
    
    
    
    
    
    
    
        
    
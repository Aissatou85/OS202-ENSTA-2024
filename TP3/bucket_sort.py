from mpi4py import MPI
import numpy as np
from time import time


# Initialisation de MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


if rank == 0:
    data = np.random.randint(0,100, size=20)
    min_value = min(data)
    max_value= max(data)
    bucket_size = (max_value - min_value) / (size-1)
    
    #Envoie des buckets aux autres processus 
    for i in range(1,size):
        start = min_value + (i-1)*bucket_size
        end = min_value + i*bucket_size
        bucket_data = [x for x in data if start <= x < end]
        comm.send(bucket_data, dest=i)
        
    #Reception des données triées des autres processus 
    sorted_data = []
    for i in range(1,size):
        sorted_bucket= comm.recv(source = i)
        sorted_data.extend(sorted_bucket)
   
    print("Le tableau Initial:", data)
    print("Le tableau trie:", sorted_data)
    
else:
    #reception des données du processus 0
    bucket = comm.recv(source=0)
    
    #Tri local
    sorted_bucket = sorted(bucket)
    
    #Envoi des données triées au processus 0
    comm.send(sorted_bucket, dest=0)
    
    
    
    
    
    
    
        
    
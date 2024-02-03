# **TRAVAUX PRATIQUES 2 OS202 2024:**


## **Exercie 1: Questions du cours**


Le code donné pour l'interblocage dans le cours est : 

MPI_Comm_rank(comm, &myRank ) ;


if (myRank == 0 )


{


MPI_Ssend( sendbuf1, count, MPI_INT, 2, tag, comm);


MPI_Recv( recvbuf1, count, MPI_INT, 2, tag, comm, &status);


}


else if ( myRank == 1 )


{


MPI_Ssend( sendbuf2, count, MPI_INT, 2, tag, comm);


}


else if ( myRank == 2 )


{


MPI_Recv( recvbuf1, count, MPI_INT, MPI_ANY_SOURCE, tag, comm,
&status );


MPI_Ssend( sendbuf2, count, MPI_INT, 0, tag, comm);


MPI_Recv( recvbuf2, count, MPI_INT, MPI_ANY_SOURCE, tag, comm,
&status );


}



### Scénario 1: Sans interblocage


- Le processus 0 envoie un message au processus 2;
- Le processus 2 reçoit le message du processus 0;
- Le processus 2 envoie un message au processus 0;
- Le processus 0 reçoit le message du processus 2;
- Le processus 1 envoie un message au processus 2;
- Le processus 2 reçoit le message du processus 1;

### Scénario 2: Avec interblocage 


- Le processus 0 envoie un message au processus 2;
- Le processus 1 envoie un message au processus 2;
- Le processus 0 est bloqué car il attent la réception du message du processus 2;
- Le processus 2 est bloqué car il reçoit 2 messages or il ne peut en recevoir qu'un avant de pouvoir envoyer un message au processus 0;

La probabilité d'avoir un interblocage est **p=1/2**



## **Exercice 2: Question du cours 2**

Utilisons la loi d'Amdhal pour prédire l'accélération maximale que peut obtenir Alice avec son code:
La loi d'Amdhal stipule que: soit ts le temps nécessaire pour exécuter le code séquentiellement, f la fraction de ts ne pouvant pas etre parallélisée et n le nombre d'unités de calcul alors :

$S(n) = ts/((f.ts)+((1-f)ts/n)) = n/(1+ (n-1)f) = 1/f$ si n tend vers l'infini.

Alors, $S(n) = 1/f = 1/0,1 = 10$ pour un grand nombre d'unités de calcul.

Pour ne pas trop gaspiller de ressources CPU, il est important de trouver un équilibre. Si n est trop grand, il y aura des coûts liés à la communication entre les différents noeuds de calculs et à la coordination des tâches, ce qui va entraîner la diminution de l'éfficacite de la parallélisation.


En doublant la quantité de données à traiter et en supposant la complexité de l'algorithme  parallèle linéaire, utilisons la loi de Gustafson pour déterminer l'accélération maximale qu'Alice peut espérer avoir:

La loi de Gustafson stipule que :
$S(n) = ts + n.tp /(ts+tp) = n+ (1-n)ts/(ts+tp) = n+ (1-n).ts$

Si Alice double la quantité de données à traiter, la nouvelle accélération maximale serait :
 $S(n) = 2n + (1-2n).ts$


 ## Exercice 3 : Ensemble de mandelbrot

1. 

 

 









# **TRAVAUX PRATIQUES 2 OS202 2024:**


## **Exercie 1: Questions du cours**


Le code donné pour l'interblocage dans le cours est : 

*MPI_Comm_rank(comm, &myRank ) ;
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
}*



### Scénario 1: Sans interblocage


-Le processus 0 envoie un message au processus 2;
-Le processus 2 reçoit le message du processus 0;
-Le processus 2 envoie un message au processus 0;
-Le processus 0 reçoit le message du processus 2;
-Le processus 1 envoie un message au processus 2;
-Le processus 2 reçoit le message du processus 1;

### Scénario 2: Avec interblocage 


-Le processus 0 envoie un message au processus 2;
-Le processus 1 envoie un message au processus 2;
-Le processus 0 est bloqué car il attent la réception du message du processus 2;
-Le processus 2 est bloqué car il reçoit 2 messages or il ne peut en recevoir qu'un avant de pouvoir envoyer un message au processus 0;

La probabilité d'avoir un interblocage est **p=1/2**



## **Exercice 2: Question du cours 2**











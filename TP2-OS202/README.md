# **TRAVAUX PRATIQUES 2 OS202 2024:**
# **GUIDADO AISSATOU HAIRIYA GROUPE 2 OS202 2024**


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

1. Le code s'appelle mandelbrot_para.cpp

Je n'ai pas pu tester pour un nombre de tâches qui n'est pas un diviseur de 1024 car la fonction MPI Gather ne permet pas d'envoyer des tableaux qui n'ont pas la meme taille.

Soit tp= temps d'exécution parallèle et ts=temps d'exécution sequentielle 

* Pour nbp = 1, tp = 2.900 et ts = 0.018 d'où le speedup = ts/tp = 6.207x 10^-3
* Pour nbp = 2, tp = 1.527 et ts = 0.017 d'où speedup = 0,011
* Pour nbp = 4, tp = 1.132 et ts = 0.034 d'où speedup = 0,030
* Pour nbp = 8, tp = 1.099 et ts = 0.049 d'où speedup = 0,045

On constate que lorsqu'on augmente le nombre de tâches, le temps d'exécution parallèle diminue et le speedup augmente. Mais, ces diminutions ne sont que très faibles. On peut donc conclure que l'application ne bénéficie pas pleinement de l'ajout de processeurs ce qui peut être causé par la partie séquentielle de l'algorithme ou des coûts de communication élevés entre les processeurs, qui limitent l'amélioration des performances parallèles.

Le code pour générer la courbe est dans le fichier "courbe.py" et vous pouvez consulter la courbe, c'est l'image "evolution_speedup".


 2. Mettons en oeuvre une stratégie maitre-esclave pour distribuer les différentes lignes de l'image:

La programmation maître-esclave (ou modèle maître-esclave) est un modèle de programmation parallèle où un processus principal, appelé le maître, coordonne l'exécution en répartissant des tâches entre lui-même et des processus esclaves. Dans notre cas, le maître distribue les portions d'images à traiter par chaque processeur et ensuite il va se charger de restituer l'image.
Le code pour cette partie s'appelle "maitre_esclaves.py".

Les résultats obtenus en tenant compte des notations utilisées dans la question précédente sont :

* Pour nbp = 2, tp = 2.956 et ts = 0.050 d'où speedup = 0.017
* Pour nbp = 4, tp = 1.576  et ts = 0.061 d'où speedup = 0.039
* Pour nbp = 8, tp = 1.168 et ts = 0.065 d'où speedup = 0.056


 De façon analogue à la première question, on constate que lorsqu'on augmente le nombre de tâches, le temps d'exécution parallèle diminue et le speedup augmente. Mais, ces diminutions ne sont que très faibles.

 
## Exercice 4: Produit matrice-vecteur

1. Le code s'appelle **matvec_para_col.py**

2. Le code s'appelle **matvec_para_lig.py**










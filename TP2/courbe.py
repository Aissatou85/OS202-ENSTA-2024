import matplotlib.pyplot as plt

# Données fournies
nbp = [1, 2, 4, 8]
speedup = [6.207e-3, 0.011, 0.030, 0.045]

# Tracer la courbe
plt.plot(nbp, speedup, marker='o', linestyle='-', color='b')

# Ajouter des labels et un titre
plt.xlabel('Nombre de processeurs (nbp)')
plt.ylabel('Speedup')
plt.title('Évolution du Speedup en fonction du nombre de processeurs')

# Afficher la légende
plt.legend(['Speedup'], loc='upper left')

# Enregistrer l'image
plt.savefig('evolution_speedup.png')

# Afficher le graphique
plt.show()

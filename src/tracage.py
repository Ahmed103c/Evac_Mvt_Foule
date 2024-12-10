import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from simulation import simulate

def tracage(nombre_ball,largeur_porte, nombre_simulation): 
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression

    Personne_evacuee = np.arange(1, nombre_ball + 1)
    Temps_Sortie_Personne = []

    # Effectuer les simulations
    for i in range(nombre_simulation):
        temps_simulation = simulate(nombre_ball,largeur_porte)
        Temps_Sortie_Personne.append(temps_simulation)

    # Convertir en tableau numpy
    Temps_Sortie_Personne = np.array(Temps_Sortie_Personne)

    # Calculer la moyenne des temps de sortie
    avg_times = Temps_Sortie_Personne.mean(axis=0)

    # Ajuster les dimensions de Personne_evacuee
    x = np.arange(1, len(avg_times) + 1)

    # Vérification des tailles
    print(f"Taille de avg_times: {len(avg_times)}")
    print(f"Taille de x: {len(x)}")

    # Tracer les courbes
    plt.figure()
    for i in range(nombre_simulation):
        plt.plot(Temps_Sortie_Personne[i], np.arange(1, len(Temps_Sortie_Personne[i]) + 1), color='green')

    # Régression linéaire
    reg = LinearRegression()
    reg.fit(avg_times.reshape(-1, 1), x.reshape(-1, 1))

    # Prédictions pour la régression linéaire
    x_pred = np.linspace(avg_times.min(), avg_times.max(), 100)
    y_pred = reg.predict(x_pred.reshape(-1, 1))

    # Tracer la régression linéaire
    plt.plot(x_pred, y_pred, color='red', label='Régression linéaire')

    plt.xlabel('Temps de sortie moyen')
    plt.ylabel('Nombre de personnes évacuées')
    plt.legend()
    plt.show()

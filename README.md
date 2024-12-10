Voici un fichier `README.md` complet pour votre projet :

---

# Evac_Mvt_Foule

## Comment installer le projet

1. **Créer un environnement virtuel** :

   ```bash
   python -m venv venv
   ```

2. **Activer l'environnement virtuel** :

   - Sous Windows :
     ```bash
     .\venv\Scripts\activate
     ```
   - Sous Linux/Mac :
     ```bash
     source venv/bin/activate
     ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

---

## Exécution du projet

Pour lancer la simulation, exécutez la commande suivante :

```bash
python .\src\main.py
```

---

## Description de la simulation

Cette simulation est basée sur le **modèle de force sociale** de Bertrand Maury, tel qu'élaboré dans son livre _Crowds in Equations: An Introduction to the Microscopic Modeling of Crowds_.

Le modèle vise à simuler les mouvements d’une foule en tenant compte des interactions sociales et des forces physiques entre les individus. Une version **non inertielle** (overdamped) du modèle est utilisée ici, où les forces d’interaction sont proportionnelles à \(1/\tau\), avec \(\tau \to 0\). Cela simplifie les équations différentielles en un système d’équations différentielles ordinaires du premier ordre :

<img src="https://latex.codecogs.com/svg.latex?\mathbf{u}_i=\frac{d\mathbf{x}_i}{dt}=\mathbf{U}_i+\sum_{j\neq i}\mathbf{W}_{ij}" />
où :

- \( \mathbf{x}\_i(t) \in \mathbb{R}^2 \) représente la position de l’individu \(i\) à l’instant \(t\),
- \( \mathbf{U}\_i \) est la vitesse désirée de l’individu \(i\),
- \( \mathbf{W}\_{ij} \) est la force d’interaction entre l’individu \(i\) et \(j\).

### Caractéristiques principales :

1. **Modèle non-inertiel :** Les déplacements sont modélisés en supposant une absence d'inertie, ce qui est pertinent dans des scénarios où les mouvements sont dominés par des forces sociales immédiates.
2. **Vitesse désirée :** Chaque individu a une vitesse cible, représentant son objectif (par exemple, atteindre une sortie).
3. **Forces d'interaction :** Elles reflètent les interactions avec d'autres individus, empêchant la collision et favorisant un comportement réaliste de la foule.
4. **Segments de porte :** La simulation inclut des obstacles et des portes pour guider ou ralentir les mouvements.

---

## Objectifs de la simulation

1. Modéliser les mouvements de foules dans des espaces confinés.
2. Observer l’impact des paramètres tels que la densité de la foule, la largeur des portes, et la vitesse désirée.
3. Tester différents scénarios pour évaluer l'efficacité des évacuations (par exemple, une porte étroite ou large).
   4.Tracage d'une courbe de régression linéaire basée sur les résultats moyens de plusieurs itérations.
   Cela permet de lisser les données, car les positions initiales des individus sont choisies aléatoirement, ce qui peut introduire des variations dans les résultats.

---

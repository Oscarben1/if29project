# Projet IF29 - Data Analytics

# Comparaison de deux méthodes de classification de profils Twitter

## Objectif :

Nous disposons d'une base de données composée de tweets. L'objectif est de comparer l'efficacité de plusieures méthodes d'analyse permettant de détecter les profils suspects de Twitter. Pour cela nous allons implanter deux algorithmes de Machine Learning avec une approche suppervisée puis non-suppervisée. Ensuite nous réaliserons une étude comparative de la pertinence des résultats fournis par chacun des algorithmes. Nous identifierons notamment l'algorithme qui est le plus adapté à répondre à notre problématique.

## Utilisation du programme :

### Prérequis :

1. Structure initiale des données :

Vos données de tweets doivent être au format json.
Elles doivent être rangées dans un dossier nommé "data" et chaque fichier de tweet est nommé "raw0, raw1...".

2. Se placer dans le répertoire de travail

3. Modules à installer :
    - os
    - json
    - pandas
    - numpy
    - matplotlib
    - sklearn

L'installation d'un module se fait avec la commande suivante :

    pip install nomModule

### Lancement des analyses :

1. Calcul des indicateurs :

Afin de déterminer si un profil est suspect ou non, nous récupérons les indicateurs suivants :

    - nombre de followers
    - nombre d'abonnés
    - ratio followers/abonnés
    - longeur du tweet
    - nombre de hashtags 
    - nombre d'URLs
    - agressivité
    - visibilité


2. Lancer ACP
  
3. Lancer l'algorithme supervisé :

4. Lancer l'agorithme non supervisé :

#!/usr/bin/env python
# coding: utf-8

# # Notebook projet IF29
# 
# Ce Notebook fait office de rendu de code pour le projet d'IF29. Le but étant, à partir d'une base de données de plus de 4 millions de tweets, de réaliser un algorithme supervisé et un non-supervisé afin de classifier les utilisateurs comme suspect ou non.
# 
# ## Importation des librairies utiles au projet

# In[ ]:


import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import svm, datasets
from sklearn import metrics 


# ## Récupération des données dans un DF Pandas
# On récupère les données parsées dans la base SQLite que l'on a exporté dans un .csv puis on enlève les colonnes identifiant et identifiant_user qui ne nous seront pas utiles pour notre analyse. On choisi de ne prendre que 400000 users pour nos traitements car nos machines ne supportent pas le traitement de toute la base.

# In[ ]:


df = pd.read_csv('data/finalDF.csv').drop(["id", "id_user"], axis=1).iloc[500000:900000,:]


# ## Centrage-réduction des données pour réaliser l'ACP
# On centre réduit les données pour supprimer la variabilité des données à cause de leur unité

# In[ ]:


#On centre réduit les données
s_sc = StandardScaler() 
df_processed = s_sc.fit_transform(df)


# ## Réalisation de l'ACP
# On réalise l'ACP pour réduire la dimensionnalité de notre dataframe, afin de réaliser l'algorithme non-supervisé K-Means. On passe donc de 8 variables à 2 variables qui sont les composantes principales retenues.

# In[ ]:


#On réalise l'ACP
modelPCA = PCA(n_components=2)
df_reduced = modelPCA.fit_transform(df_processed)


# On récupère ici les variances expliquées par chaque composante principale afin d'avoir cette indication sur notre graph. On trace donc le graph avec les deux composantes principales comme axes.

# In[ ]:


CP1inertie = str(round(round(modelPCA.explained_variance_ratio_[0],3)*100,1))
CP2inertie = str(round(round(modelPCA.explained_variance_ratio_[1],3)*100,1))
xlab = str("CP1 ("+CP1inertie+"%)")
ylab = str("CP2 ("+CP2inertie+"%)")
plt.scatter(df_reduced[:,0],df_reduced[:,1])
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.show()


# ## Trouver le nombre de clusters pour le K-Means
# Pour trouver le nombre de clusters que nous allons prendre pour le K-Means, on réalise la méthode du coude représentant l'inertie en fonction du nombre de clusters.

# In[ ]:


#Elbow method
inertia = []
K_range = range(1, 8)
for i in K_range:
    modelElbow = KMeans(n_clusters=i).fit(df_reduced)
    inertia.append(modelElbow.inertia_)

plt.plot(K_range, inertia)
plt.xlabel('nb de clusters')
plt.ylabel('Inertie')
plt.show()


# ## K-Means avec 3 clusters
# On réalise le K-Means avec 3 clusters, car c'est notre zone de coude

# In[ ]:


#KMeans with 3 clusters
modelKMeans = KMeans(n_clusters=3)
df_KMeans = modelKMeans.fit(df_reduced)


# On trace le graph en donnant une couleur définie à nos clusters

# In[ ]:


label = modelKMeans.fit_predict(df_reduced)

filtered_label0 = df_reduced[label == 0]
filtered_label1 = df_reduced[label == 1]
filtered_label2 = df_reduced[label == 2]
plt.scatter(filtered_label0[:,0] , filtered_label0[:,1] , color = 'red')
plt.scatter(filtered_label1[:,0] , filtered_label1[:,1] , color = 'black')
plt.scatter(filtered_label2[:,0] , filtered_label2[:,1] , color = 'green')
plt.show()


# ## K-Means avec 6 clusters
# Pour plus de représentativité par rapport à la problématique, on réalise un K-Means avec 6 clusters

# In[ ]:


#KMeans with 6 clusters
modelKMeans = KMeans(n_clusters=6)
df_KMeans = modelKMeans.fit(df_reduced)


# On trace le graph avec les 6 clusters en choisissant la couleur de chacun.

# In[ ]:


label = modelKMeans.fit_predict(df_reduced)

filtered_label0 = df_reduced[label == 0]
filtered_label1 = df_reduced[label == 1]
filtered_label2 = df_reduced[label == 2]
filtered_label3 = df_reduced[label == 3]
filtered_label4 = df_reduced[label == 4]
filtered_label5 = df_reduced[label == 5]
plt.scatter(filtered_label0[:,0] , filtered_label0[:,1] , color = 'red')
plt.scatter(filtered_label1[:,0] , filtered_label1[:,1] , color = 'black')
plt.scatter(filtered_label2[:,0] , filtered_label2[:,1] , color = 'green')
plt.scatter(filtered_label3[:,0] , filtered_label3[:,1] , color = 'cyan')
plt.scatter(filtered_label4[:,0] , filtered_label4[:,1] , color = 'magenta')
plt.scatter(filtered_label5[:,0] , filtered_label5[:,1] , color = 'yellow')
plt.show()


# ## Labellisation de nos utilisateurs
# On labellise les utilisateurs comme suspect ou non en fonction du résultat du K-Means. Le cluster ayant le pourcentage de comptes supprimés le plus élevé est considéré comme étant suspect.

# In[ ]:


#User from each clusters

cluster0 = pd.DataFrame(df-reduced[df_KMeans.labels_==0])
cluster1 = pd.DataFrame(df-reduced[df_KMeans.labels_==1])
cluster2 = pd.DataFrame(df_reduced[df_KMeans.labels_==2])
cluster3 = pd.DataFrame(df_reduced[df_KMeans.labels_==3])
cluster4 = pd.DataFrame(df_reduced[df_KMeans.labels_==4])
cluster5 = pd.DataFrame(df_reduced[df_KMeans.labels_==5])

cluster0['suspect'] = 0
cluster1['suspect'] = 0
cluster2['suspect'] = 0
cluster3['suspect'] = 1
cluster4['suspect'] = 0
cluster5['suspect'] = 0


#  On concatène nos 6 clusters pour creer un dataset final

# In[ ]:


dataset_label = pd.concat([cluster0, cluster1, cluster2, cluster3, cluster4, cluster5])
dataset_label.to_csv('data/dataset_label.csv', encoding='utf-8')
dataset_final = np.array(dataset_label)


# # SVM
# ## Séparation des labels
# On sépare les variables X de leur label Y

# In[ ]:


X = dataset_final[:,:-1]
Y = dataset_final[:,-1]


# ## Répartition Training/Test
# On sépare notre jeu de données en 2 sous-datasets, un pour l'entrainement du model et un pour le test, comprenant respectivement 80% et 20% des données prises aléatoirement.

# In[ ]:


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.8, random_state = 0)


# ## Entrainement du model
# On entraine tout d'abord le model avec la fonction noyau 'linear'

# In[1]:


linear = svm.SVC(kernel='linear')

linear.fit(X_train, Y_train)


# In[ ]:


plt.scatter(X_train[:, 0], X_train[:, 1], c = Y_train)
plt.show()


# ## Test et analyse
# On test le model sur nos données test

# In[ ]:


Y_pred = linear.predict(X_test)


# On analyse les résultats avec le dataset de test

# In[ ]:


print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))


# In[ ]:


plt.scatter(X_test[:, 0], X_test[:, 1], c = Y_pred)
plt.show()


# ### Confusion Matrix

# In[2]:


from sklearn.metrics import plot_confusion_matrix
# Plot non-normalized confusion matrix
titles_options = [("Matrice de confusion, avec normalisation", None),
                  ("Matrice de confusion normalisée", 'true')]
for title, normalize in titles_options:
    disp = plot_confusion_matrix(linear, X_test, Y_test,
                                 display_labels=['normal','suspect'],
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
    disp.ax_.set_title(title)

    print(title)
    print(disp.confusion_matrix)

plt.show()


# ## SVM avec la fonction poly
# 

# In[ ]:


poly = svm.SVC(kernel='poly')

poly.fit(X_train, Y_train)

Y_pred = poly.predict(X_test)


# In[ ]:


plt.scatter(X_train[:, 0], X_train[:, 1], c = Y_train)
plt.show()


# In[ ]:


print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))


# In[ ]:


plt.scatter(X_test[:, 0], X_test[:, 1], c = Y_pred)
plt.show()


# ## SVM avec la fonction rdf 

# In[ ]:


rbf = svm.SVC(kernel='rbf')

rbf.fit(X_train, Y_train)

Y_pred = rbf.predict(X_test)


# In[ ]:


plt.scatter(X_train[:, 0], X_train[:, 1], c = Y_train)
plt.show()


# In[ ]:


print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))


# In[ ]:


plt.scatter(X_test[:, 0], X_test[:, 1], c = Y_pred)
plt.show()


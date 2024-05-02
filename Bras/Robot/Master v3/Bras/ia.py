import numpy as np
#np.set_printoptions(threshold=np.nan)
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
import warnings
import matplotlib.pyplot as plt
import tensorflow as tf

warnings.filterwarnings('ignore')


def knn(X_test, X_train, y_test, y_train):
    loops = 20
    mean_accuracy = 0
    print("\n========= Résultat K plus proche avant Scaler ===========")
    model = KNeighborsClassifier(n_neighbors=5)
    for i in range(loops):
        model.fit(X_train,y_train)
        prediction= model.predict(X_test)
        mean_accuracy += accuracy_score(y_test, prediction)
    print("Le score d'accuracy est : "+str(mean_accuracy/loops))

    mean_accuracy = 0
    scaler = StandardScaler()
    print("\n========= Résultat K plus proche après StandardScaler ===========")
    model = KNeighborsClassifier(n_neighbors=5)
    for i in range(loops):
        model.fit(scaler.fit_transform(X_train),y_train)
        prediction= model.predict(X_test)
        mean_accuracy += accuracy_score(y_test, prediction)
    print("Le score d'accuracy est : "+str(mean_accuracy/loops))

    mean_accuracy = 0
    print("\n========= Résultat K plus proche après MinMaxScaler ===========")
    model = KNeighborsClassifier(n_neighbors=5)
    scaler = MinMaxScaler()
    for i in range(loops):
        model.fit(scaler.fit_transform(X_train),y_train)
        prediction= model.predict(X_test)
        mean_accuracy += accuracy_score(y_test, prediction)
    print("Le score d'accuracy est : "+str(mean_accuracy/loops))

    mean_accuracy = 0
    print("\n========= Résultat K plus proche après PCA et StandardScaler ===========")
    model = KNeighborsClassifier(n_neighbors=5)
    pca = PCA()
    scaler = StandardScaler()
    for i in range(loops):
        X_scaler = scaler.fit_transform(X_train)
        X_pca = pca.fit_transform(X_scaler)
        #print(X_train.shape)
        model = model.fit(X_train, y_train)
        X_scaler_test = scaler.fit_transform(X_test)
        X_pca_test = pca.fit_transform(X_scaler_test)
        prediction= model.predict(X_pca_test)
        mean_accuracy += accuracy_score(y_test, prediction)
    print("Le score d'accuracy est : "+str(mean_accuracy/loops))

    mean_accuracy = 0
    print("\n========= Résultat K plus proche après PCA et MinMaxScaler ===========")
    model = KNeighborsClassifier(n_neighbors=5)
    pca = PCA()
    scaler = MinMaxScaler()
    for i in range(loops):
        X_scaler = scaler.fit_transform(X_train)
        X_pca = pca.fit_transform(X_scaler)
        #print(X_train.shape)
        model = model.fit(X_train, y_train)
        X_scaler_test = scaler.fit_transform(X_test)
        X_pca_test = pca.fit_transform(X_scaler_test)
        prediction= model.predict(X_pca_test)
        mean_accuracy += accuracy_score(y_test, prediction)
    print("Le score d'accuracy est : "+str(mean_accuracy/loops))



def main():
    df = pd.read_csv("sample.csv")
    X = np.array(df.values[:, 0:5])
    Y = np.array(df.values[:, 5:8])
    
    # Divisez les données en ensembles d'entraînement et de test
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    print("\n\n\nLinear regression")
    # Créez un modèle de régression linéaire (vous pouvez utiliser d'autres modèles si vous le souhaitez)
    model = LinearRegression()
    # Entraînez le modèle sur les données d'entraînement
    model.fit(X_train, Y_train)
    # Prédisez les valeurs des trois derniers angles à partir des trois premiers angles et des coordonnées
    predictions = model.predict(X_test)
    # Évaluez la performance du modèle (par exemple, en utilisant la RMSE ou d'autres métriques)
    from sklearn.metrics import mean_squared_error
    rmse = mean_squared_error(Y_test, predictions, squared=False)
    print(f"RMSE: {rmse}")
    mean_actual = Y_test.mean()
    error_percentage = (rmse / mean_actual) * 100
    print(f"Marge d'erreur en pourcentage : {error_percentage}%")


    poly = PolynomialFeatures(degree=2)  # Vous pouvez ajuster le degré au besoin
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Créez un modèle de régression linéaire
    model = LinearRegression()

    # Entraînez le modèle sur les données d'entraînement avec les caractéristiques polynomiales
    model.fit(X_train_poly, Y_train)

    # Prédisez les valeurs des trois derniers angles à partir des caractéristiques polynomiales
    predictions = model.predict(X_test_poly)

    # Évaluez la performance du modèle (par exemple, en utilisant la RMSE ou d'autres métriques)
    rmse = mean_squared_error(Y_test, predictions, squared=False)
    print(f"RMSE: {rmse}")

    print("\n\n\nRéseau de neuronne")
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    # Créer le modèle de réseau de neurones
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(3)  # 3 neurones de sortie pour les trois derniers angles
    ])
    # Compiler le modèle
    model.compile(optimizer='adam', loss='mean_squared_error')
    # Entraîner le modèle
    model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_split=0.2)
    # Évaluer le modèle sur l'ensemble de test
    loss = model.evaluate(X_test, Y_test)
    print(f"Loss sur l'ensemble de test : {loss}")
    # Faites des prédictions
    predictions = model.predict(X_test)


main()
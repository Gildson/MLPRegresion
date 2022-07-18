#Importações das bibliotecas que utilizaremos no projeto
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
plt.style.use('classic')
# %matplotlib inline

from google.colab import drive
drive.mount('/content/drive')

#Leitura do arquivo csv
olist_dataset = pd.read_csv('/content/drive/MyDrive/Projeto_de_ciencia_de_dados/my_dataset.csv')

#Dataset original
olist_dataset

olist_dataset = olist_dataset.drop(columns = ['Unnamed: 0', 'order_item_id',
                                              'order_id', 'product_id', 'seller_zip_code_prefix',
                                              'seller_id', 'seller_city', 'product_name_lenght',
                                              'product_description_lenght',
                                              'payment_sequential', 'payment_installments', 'product_category_name',
                                              'product_photos_qty',	'product_weight_g',	'product_length_cm', 'shipping_limit_date'])
#Retirando as colunas que não serão necessárias.
olist_dataset = olist_dataset.drop(columns = ['review_id', 'review_score', 'review_comment_title', 'order_approved_at',
                                              'review_comment_message', 'customer_zip_code_prefix',
                                              'review_creation_date', 'customer_city', 'order_status',
                                              'review_answer_timestamp', 'product_height_cm',	'product_width_cm',
                                              'customer_unique_id', 'customer_id', 'ano_envio', 'mes_envio', 'seller_state',
                                              'order_delivered_carrier_date',	'order_delivered_customer_date',	'order_estimated_delivery_date'])

olist_dataset['order_purchase_timestamp'] =  pd.to_datetime(olist_dataset['order_purchase_timestamp'], format='%Y-%m-%d %H:%M:%S')
olist_dataset['mes_compra'] = olist_dataset['order_purchase_timestamp'].dt.month
olist_dataset['ano_compra'] = olist_dataset['order_purchase_timestamp'].dt.year
olist_dataset = olist_dataset.drop(columns = ['price', 'freight_value', 'order_purchase_timestamp'])
olist_dataset

#Dividir o dataset por vendas por estado
dataset_RN = olist_dataset[olist_dataset.customer_state=='RN']
dataset_CE = olist_dataset[olist_dataset.customer_state=='CE']
dataset_PB = olist_dataset[olist_dataset.customer_state=='PB']
dataset_MG = olist_dataset[olist_dataset.customer_state=='MG']
dataset_SP = olist_dataset[olist_dataset.customer_state=='SP']
dataset_PR = olist_dataset[olist_dataset.customer_state=='PR']
dataset_RJ = olist_dataset[olist_dataset.customer_state=='RJ']
dataset_SC = olist_dataset[olist_dataset.customer_state=='SC']
dataset_RS = olist_dataset[olist_dataset.customer_state=='RS']
dataset_DF = olist_dataset[olist_dataset.customer_state=='DF']
dataset_BA = olist_dataset[olist_dataset.customer_state=='BA']
dataset_GO = olist_dataset[olist_dataset.customer_state=='GO']
dataset_PE = olist_dataset[olist_dataset.customer_state=='PE']
dataset_MA = olist_dataset[olist_dataset.customer_state=='MA']
dataset_ES = olist_dataset[olist_dataset.customer_state=='ES']
dataset_MT = olist_dataset[olist_dataset.customer_state=='MT']
dataset_MS = olist_dataset[olist_dataset.customer_state=='MS']
dataset_RO = olist_dataset[olist_dataset.customer_state=='RO']
dataset_PI = olist_dataset[olist_dataset.customer_state=='PI']
dataset_SE = olist_dataset[olist_dataset.customer_state=='SE']
dataset_PA = olist_dataset[olist_dataset.customer_state=='PA']
dataset_AM = olist_dataset[olist_dataset.customer_state=='AM']
dataset_AC = olist_dataset[olist_dataset.customer_state=='AC']

df_2018 = olist_dataset[olist_dataset.ano_compra == 2018]
df_2018
#df_2018.to_csv('olist_data_2018')

# Commented out IPython magic to ensure Python compatibility.
plt.style.use('classic')
# %matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt

X = df_2018.iloc[:, 0 : 2].values
Y = df_2018.iloc[:, 3].values
labelencoder = LabelEncoder()
X[:,0] = labelencoder.fit_transform(X[:,0])

X = np.asarray(X).astype(np.float32)
Y = np.asarray(Y).astype(np.float32)

#Separando dados de treinamento e teste
x_treinamento, x_teste, y_treinamento, y_teste = train_test_split(X, Y, test_size=0.3, random_state=40)

#Criação do modelo de rede neural para uma regressão
model = keras.Sequential(
    [layers.Dense(100, activation='relu'),
    layers.Dense(100, activation='relu'),
    layers.Dense(1)
])

optimizer = tf.keras.optimizers.RMSprop(0.001)

model.compile(loss='mse',
              optimizer=optimizer,
              metrics=['mae', 'mse'])

previsoes = model.predict(x_teste)

history = model.fit(X, Y, epochs=50, validation_split = 0.3, verbose=2)

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
hist



def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch

  plt.figure(figsize=(10,7))
  plt.xlabel('Épocas')
  plt.ylabel('Erro')
  plt.title("Curva do erro médio")
  plt.plot(hist['epoch'], hist['mae'], color="red", 
           label='Erro de treinamento')
  plt.plot(hist['epoch'], hist['val_mae'],
           label = 'Erro de validação')
  plt.ylim([1.5,3])
  plt.legend()
  plt.savefig('erro.png', format='png')
  plt.show()

plot_history(history)

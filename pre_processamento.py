# -*- coding: utf-8 -*-
"""pre_processamento.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14_QsU5I6EvKB6G0OBv6HzhIJVZA_xKws
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import random
from imblearn.over_sampling import RandomOverSampler

#Carregando a base
#É necessário fazer o download da base no kaggle e dar o upload no collab
#Link da base: https://www.kaggle.com/dipam7/student-grade-prediction
base = pd.read_csv('student-mat.csv', sep=',')

#Drop em variáveis que não serão utilizadas
base = base.drop(['school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu', 'Mjob', 'Fjob', 'reason', 'guardian', 'Dalc', 'Walc', 'G1', 'G2'], axis=1)

#Transformado as variáveis binárias (yes or no) para 1 ou 0
base = base.replace(to_replace = ['yes','no'], value = ['1', '0'])

#Transformando a variável G3 para aprovado ou reprovado (G3>=10 - Aprovado (1) / G3<10 - Reprovado (0))
base.G3 = base.G3.replace(to_replace = range(0, 10), value = 0)
base.G3 = base.G3.replace(to_replace = range(10, 21), value = 1)

X = base.drop(['G3'], axis=1).values
Y = base.G3.values

#Oversampling
ros = RandomOverSampler(random_state=42)
X_res, y_res = ros.fit_resample(X, Y)

#Split na base
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42, stratify=y_res)

#Desenvolvendo a base de treino
x_train_df = pd.DataFrame(
    data=X_train, 
    columns=['traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'health', 'absences'])
y_train_df = pd.DataFrame(
    data=y_train,
    columns=['G3']
)

train = pd.concat([x_train_df, y_train_df], axis=1, sort=False)

#Colocando ruído na base de treino
#for column in train:
#    train.at[random.randint(0, len(train[column])), column] = None
#    train.at[random.randint(0, len(train[column])), column] = None


#Desenvolvendo a base de testes
x_test_df = pd.DataFrame(
    data=X_test, 
    columns=['traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'health', 'absences'])
y_test_df = pd.DataFrame(
    data=y_test,
    columns=['G3']
)

test = pd.concat([x_test_df, y_test_df], axis=1, sort=False)


#==================================
# selecionar e renomear colunas
#==================================

# test
test.drop(['famsup','schoolsup', 'nursery', 'romantic', 'famrel', 'failures', 'paid'], axis=1, inplace=True)
test.columns =['tempo_ate_escola', 'tempo_de_estudo', 'atividades_extra_curriculares', 'quer_entrar_na_universidade',  'internet_casa', 'tempo_livre_depois_escola', 'sai_com_amigos', 'estado_saude', 'numero_de_faltas','aprovacao']
test.to_csv('teste.csv')
test_x = test[['tempo_ate_escola', 'tempo_de_estudo', 'atividades_extra_curriculares', 'quer_entrar_na_universidade',  'internet_casa', 'tempo_livre_depois_escola', 'sai_com_amigos', 'estado_saude', 'numero_de_faltas']]
test_y = test['aprovacao']

# train
train.drop(['famsup','schoolsup', 'nursery', 'romantic', 'famrel', 'failures', 'paid'], axis=1, inplace=True)
train.columns =['tempo_ate_escola', 'tempo_de_estudo', 'atividades_extra_curriculares', 'quer_entrar_na_universidade', 'internet_casa', 'tempo_livre_depois_escola', 'sai_com_amigos', 'estado_saude', 'numero_de_faltas','aprovacao']
train.to_csv('treino.csv')
train_x = train[['tempo_ate_escola', 'tempo_de_estudo', 'atividades_extra_curriculares', 'quer_entrar_na_universidade',  'internet_casa', 'tempo_livre_depois_escola', 'sai_com_amigos', 'estado_saude', 'numero_de_faltas']]
train_y = train['aprovacao']


def modelExperiments(train_x, train_y, test_x, test_y, model):
    acc_shots = []
    from sklearn.metrics import confusion_matrix
    while len(acc_shots) < 100:
        # choose model
        if model == 'tree':
            from sklearn import tree
            clf = tree.DecisionTreeClassifier()
        elif model == 'forest':
            from sklearn.ensemble import RandomForestClassifier
            clf = RandomForestClassifier(max_depth=2, random_state=0)
        elif model == 'ann':
            from sklearn.neural_network import MLPClassifier
            clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                                hidden_layer_sizes=(12, 20), random_state=1)
        # execute model
        clf = clf.fit(train_x, train_y)
        predicted=clf.predict(test_x)
        vp, fn, fp, vn = confusion_matrix(test_y, predicted, labels=[1,0]).reshape(-1)
        acuracia = (vp+vn) / (vp+fn+fp+vn)
        acc_shots.append(acuracia)
    return acc_shots


tree =  modelExperiments(train_x, train_y, test_x, test_y, 'tree')
forest =  modelExperiments(train_x, train_y, test_x, test_y, 'forest')
ann =  modelExperiments(train_x, train_y, test_x, test_y, 'ann')

results_experiments = pd.DataFrame({'decision_tree':tree, 'random_forest':forest, 'artificial_neural_network':ann})

results_experiments.to_csv('results_experiments.csv')

results_experiments['decision_tree'].mean()
results_experiments['random_forest'].mean()
results_experiments['artificial_neural_network'].mean()
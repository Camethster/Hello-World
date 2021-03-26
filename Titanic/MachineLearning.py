# %%
import pandas as pd
import altair as alt
import pickle
import numpy as np
from pprint import pprint
import altair_saver
from imblearn.over_sampling import RandomOverSampler
from  tabulate import tabulate 
import matplotlib.pyplot as plt


# %%
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
#%%
url = "https://gist.githubusercontent.com/michhar/2dfd2de0d4f8727f873422c5d959fff5/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv"



# %%
# Cleaning Data
titanic = pd.read_csv(url)
titanic.info()

# Remove Y and other identifier data
titanic["Y"] = titanic.Survived
titanic.drop(["Survived","PassengerId","Name", "Ticket"],inplace=True,axis=1)


titanic.Cabin.head(20)
# Add new rows
titanic["CabinStr"] = titanic.Cabin.astype("string")
titanic = pd.concat([titanic.CabinStr.str.extract(r"(?P<Floor>.)(?P<CabinNum>[0-9]+)",expand=False),titanic],axis=1)

titanic.info()

# %%
#  Remove Na or Impute
titanic.Floor.fillna("Unknown",inplace=True)
titanic.Embarked.dropna(inplace=True)
titanic.Age.fillna(method="ffill",inplace=True)
rng = np.random.default_rng()
titanic.info()
# %%
# Change Datatypes Na Remove
titanic.replace("Age",titanic.Age.round(0),inplace=True)
titanic.replace("Fare",titanic.Fare.round(2),inplace=True)
titanic.replace("Pclass",titanic.Pclass.astype("category"),inplace = True)
titanic = titanic.astype({"Floor" : 'object',
        "CabinNum" : 'float64',
        "SibSp"  : 'float64',
        "Parch" : 'float64',
        "Pclass" : 'object'},copy=True)
titanic = titanic.drop(["CabinStr","Cabin"],axis=1)
titanic.CabinNum.fillna(0,inplace=True)
titanic.dropna()
# %%
# Test & Train Split Pipeline()
ec = OneHotEncoder()
norm = Normalizer()

X = pd.DataFrame(np.concatenate(
    [ec.fit_transform(titanic.select_dtypes(include="object")).toarray(),
norm.transform(titanic.select_dtypes(exclude="object").drop("Y",axis=1))],axis=1),)
X.columns = np.concatenate([ec.get_feature_names(),titanic.select_dtypes(exclude="object").drop("Y",axis=1).columns.tolist()])
Y = titanic.Y
X_train, X_test, y_train, y_test = train_test_split(X,Y)

# %%
# Model
clf = GradientBoostingClassifier(n_estimators=1000,random_state=16)
clf.fit(X_train,y_train)
clf.score(X_test,y_test)

# %%
y_pred = clf.predict(X_test)
met = pd.DataFrame(metrics.classification_report(y_test,y_pred,output_dict=True))
confusion_matrix(y_test,y_pred)


# %%
guess = pd.DataFrame({"Floor" : ,"CabinNum" : ,"Pclass" : ,"Sex" : ,"Age" : , "SibSp" : , "Parch" : , "Fare" :, "Embarked" : })
# %%
X_guess = pd.DataFrame(np.concatenate(
    [ec.fit_transform(guess.select_dtypes(include="object")).toarray(),
norm.transform(guess.select_dtypes(exclude="object").drop("Y",axis=1))],axis=1),)
X.columns = np.concatenate([ec.get_feature_names(),guess.select_dtypes(exclude="object").drop("Y",axis=1).columns.tolist()])

clf.predict(X_guess)
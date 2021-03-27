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
from sklearn import svm
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import  RandomForestClassifier 
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
ro = RandomOverSampler()

X = pd.DataFrame(np.concatenate(
    [ec.fit_transform(titanic.select_dtypes(include="object")).toarray(),
norm.fit_transform(titanic.select_dtypes(exclude="object").drop("Y",axis=1))],axis=1),)
X.columns = np.concatenate([ec.get_feature_names(),titanic.select_dtypes(exclude="object").drop("Y",axis=1).columns.tolist()])
Y = titanic.Y
X_new, y_new = ro.fit_resample(X,Y)
X_train, X_test, y_train, y_test = train_test_split(X_new,y_new)

# %%
# Model
clf = GradientBoostingClassifier(n_estimators=10000,random_state=16)
clf.fit(X_train,y_train)
clf.score(X_test,y_test)

clf_svm = svm.NuSVC(gamma='auto',random_state=16)
clf_svm.fit(X_train,y_train)

clf_MLP = MLPClassifier(solver='lbfgs', hidden_layer_sizes={2,15}, max_iter = 10000,alpha=1e-5, random_state=16)
clf_MLP.fit(X_train,y_train)

clf_forest = RandomForestClassifier(n_estimators=10000,random_state=16)
clf_forest.fit(X_train,y_train)

# %%
mlp_y_pred = clf_MLP.predict(X_test)
svm_y_pred = clf_svm.predict(X_test)
y_pred = clf.predict(X_test)
forest_y_pred = clf_forest.predict(X_test)
met = pd.DataFrame(metrics.classification_report(y_test,y_pred,output_dict=True))
met_SVM = pd.DataFrame(metrics.classification_report(y_test,svm_y_pred,output_dict=True))
met_mlp = pd.DataFrame(metrics.classification_report(y_test,mlp_y_pred,output_dict=True))
met_forest = pd.DataFrame(metrics.classification_report(y_test,forest_y_pred,output_dict=True))
print(confusion_matrix(y_test,y_pred))
print(confusion_matrix(y_test,svm_y_pred))
print(confusion_matrix(y_test,mlp_y_pred))
print(confusion_matrix(y_test,forest_y_pred))
print(met)
print(met_SVM)
print(met_mlp)
print(met_forest)
# %%
guess = dict.fromkeys(ec.get_feature_names(),0)
guess.update(dict.fromkeys(titanic.select_dtypes(exclude='object').drop('Y',axis=1).columns.tolist(),0))
guess.update({'x0_E' : [1.0],'CabinNum' : [83.00], 'x1_1'  : [1.0],'x2_female' : [1.0], 'x3_C' :  [1.0],"Age" : [20.0], "SibSp" : [4.0], "Parch" : [2.0], "Fare" : [0.0]})
guess_x =  pd.DataFrame.from_dict(guess,orient='columns')
enc_num_x = pd.DataFrame(norm.transform(guess_x[guess_x.columns[-5:]]),columns=["CabinNum","Age","SibSp","Parch","Fare"])
guess_x[guess_x.columns[:-5]].combine_first(enc_num_x)

#guess_x.replace(to_replace=["CabinNum","Age","SibSp","Parch","Fare"],value=enc_num_x)
   
# %%

print(clf.predict(guess_x)[0])
print(clf_svm.predict(guess_x)[0])
print(clf_MLP.predict(guess_x)[0])
print(clf_forest.predict(guess_x)[0])

# %%

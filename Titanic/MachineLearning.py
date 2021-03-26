# %%
import pandas as pd
import altair as alt
import pickle
import numpy as np
from pprint import pprint
import altair_saver
from imblearn.over_sampling import RandomOverSampler
from  tabulate import tabulate 
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
clf = GradientBoostingClassifier(n_estimators=1000)
clf.fit(X_train,y_train)
clf.score(X_test,y_test)

# %%
y_pred = clf.predict(X_test)
met = pd.DataFrame(metrics.classification_report(y_test,y_pred,output_dict=True))
print(met)
# %%
# Oversampling method
ro = RandomOverSampler()
# %%
X = bank_e.drop(['Y','y_yes','y_no',],axis=1).drop(cat.columns,axis=1)
y = bank_e.filter(regex = 'Y')
X_new, y_new = ro.fit_resample(X,y)
X_train, X_test, y_train, y_test = train_test_split(
    X_new, y_new, test_size=0.3, random_state=16)
print(X.median())
print(X.info())
X.head()
y_new.value_counts()
# %%
# Random Forest

rand_tree_clf = RandomForestClassifier(n_estimators=1000, random_state=16)
rand_tree_clf.fit(X_train,y_train)

Y_pred = rand_tree_clf.predict(X_test)
met = pd.DataFrame(metrics.classification_report(y_test,Y_pred,output_dict=True))
print(met)
Normal_tree = pickle.dumps(rand_tree_clf)
# %%

value = pd.DataFrame({"Value"  :rand_tree_clf.feature_importances_ ,
                "Features" : X.columns })
# %%
alt.Chart(value).encode(alt.X("Value"),alt.Y("Features",sort='-x')).mark_bar()
# %%
# bad times
# low emp_varation rate
# low Euborism3m
# low consumer confidence
# low consumer price index
# low employment rate
bank_bad = bank_e.query("euribor3m < @bank.euribor3m.median()")
bank_bad = bank_bad.query("emp_var_rate < @ bank.emp_var_rate.median()")
bank_bad = bank_bad.query("cons_conf_idx < @bank.cons_conf_idx.median()")
#bank_bad = bank_bad.query("cons_price_idx < @bank.cons_price_idx.median()")
bank_bad = bank_bad.query("nr_employed < @bank.nr_employed.median()")
bank_bad.info()
# good times
# %%
print(bank_e.query("cons_price_idx > @bank.cons_price_idx.median()").cons_price_idx.value_counts())
bank_good= bank.query("euribor3m > @bank.euribor3m.median()")
bank_good = bank_good.query("emp_var_rate > @ bank.emp_var_rate.median()")
bank_good = bank_good.query("cons_conf_idx > @bank.cons_conf_idx.median()")
#bank_good = bank_good.query("cons_price_idx > @bank.cons_price_idx.median()")
bank_good = bank_good.query("nr_employed > @bank.nr_employed.median()")
bank_good.info()
# %%
X_b = bank_bad.drop(['Y','y_no','y_yes'],axis=1).drop(cat.columns,axis=1)
y_b = bank_bad.filter(regex = 'Y')
X_b_new, y_b_new = ro.fit_resample(X_b,y_b)
X_b_train, X_b_test, y_b_train, y_b_test = train_test_split(
    X_b_new, y_b_new, test_size=0.3, random_state=16)
print(X_b.median())
print(X_b.info())
X_b.head()
y_b_new.value_counts()

# %%
rand_tree_bad_clf = RandomForestClassifier(n_estimators=1000, random_state=16)
rand_tree_bad_clf.fit(X_b_train,y_b_train)

y_b_pred = rand_tree_bad_clf.predict(X_b_test)
bad_met =  pd.DataFrame(metrics.classification_report(y_b_test,y_b_pred,output_dict=True))
print(bad_met)
Bad_tree = pickle.dumps(rand_tree_bad_clf)
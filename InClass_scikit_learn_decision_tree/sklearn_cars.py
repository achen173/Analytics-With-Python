import pandas as pd
from sklearn import tree
from sklearn.model_selection import cross_val_score

df_all = pd.read_csv('mtcars.csv')
y = df_all['cyl']
df_all.drop(columns='cyl')
del df_all["model"]

clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, df_all, y)
print(scores)

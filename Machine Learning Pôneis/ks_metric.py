# %% 
import pandas as pd
from sklearn import model_selection
from sklearn import ensemble
from sklearn import pipeline

from feature_engine import imputation

import scikitplot as skplt


df = pd.read_csv('dados_pontos.csv', sep=';')
features = df.columns[3:-1]
target = 'flActive'

# %%


X_train, X_test, y_train, y_test = model_selection.train_test_split(df[features],
                                                                    df[target],
                                                                    test_size=0.2,
                                                                    random_state=42,
                                                                    stratify=df[target])

print("Tx Resposta treino: ", y_train.mean())
print("Tx Resposta teste: ", y_test.mean())

# %%
X_train.isna().sum()

# %%
imput_max = imputation.ArbitraryNumberImputer(arbitrary_number=999, variables=['avgRecorrencia'])

clf = ensemble.RandomForestClassifier(random_state=42)

params = {
    'n_estimators': [200, 300, 400, 500],
    'min_samples_leaf': [10, 20, 50, 100]
}

grid = model_selection.GridSearchCV(clf, param_grid=params, scoring='roc_auc', n_jobs=-1)

model = pipeline.Pipeline([
    ('imput', imput_max),
    ('model', grid)
])

model.fit(X_train, y_train)

# %%

y_test_proba = model.predict_proba(X_test)
y_test_proba

# %%

df = pd.DataFrame({
    "f1Active": y_test,
    "proba_modelo": y_test_proba[:,1]
})

# df.to_excel("../Machine Learning Pôneis/dados_ks.xlsx", index=False)
# %%

skplt.metrics.plot_ks_statistic(y_test, y_test_proba)
# %%
model_s = pd.Series({
    "model": model,
    "features": features,
    "auc_test": auc
})

model_s.to_pickle("modelo_rf.pkl")
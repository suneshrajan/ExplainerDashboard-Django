#Importing Libraries & Packages
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from explainerdashboard import RegressionExplainer, ClassifierExplainer, ExplainerDashboard
from sklearn.model_selection import train_test_split
from explainerdashboard.datasets import titanic_survive
import sys
import json

df = pd.DataFrame(json.loads(sys.argv[1])).fillna(0)
target = sys.argv[2]
p_type = sys.argv[3]

if p_type == 'regression':
    x = df.drop(columns=[target])
    y = df[[target]]

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    model = RandomForestRegressor(n_estimators=50, max_depth=5)
    model.fit(X_train, y_train.values.ravel())

    explainer = RegressionExplainer(model, X_test, y_test)
    db = ExplainerDashboard(explainer, 
                            title="Diabetes Prediction", # defaults to "Model Explainer "
                            whatif=False,
                            )

elif p_type == 'classification':
    X_train = df
    y_train = df[target]
    X_test = df.head(8)
    y_test = df.head(8)[target]

    X_train1, y_train1, X_test1, y_test1 = titanic_survive()

    # X_train, y_train, X_test, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    model = RandomForestClassifier(n_estimators=20, max_depth=2)
    model.fit(X_train, y_train)

    explainer = ClassifierExplainer(
                    model, X_test, y_test,
                    # optional:
                    # cats=['Sex', 'Deck', 'Embarked'],
                    labels=['is_member', 'is_not_member']
                    )

    db = ExplainerDashboard(explainer, title="Titanic Explainer",
                        whatif=False, # you can switch off tabs with bools
                        shap_interaction=False,
                        decision_trees=False)

db.run(host='13.233.161.81', port=5055, use_waitress=True)
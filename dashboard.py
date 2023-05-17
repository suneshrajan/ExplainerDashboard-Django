#Importing Libraries & Packages
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from explainerdashboard import RegressionExplainer, ExplainerDashboard
from sklearn.model_selection import train_test_split
import sys
import json

x = pd.DataFrame(json.loads(sys.argv[1]))
y = pd.DataFrame(json.loads(sys.argv[2]))

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

model = RandomForestRegressor(n_estimators=50, max_depth=5)
model.fit(X_train, y_train.values.ravel())

explainer = RegressionExplainer(model, X_test, y_test)

db = ExplainerDashboard(explainer, 
                        title="Diabetes Prediction", # defaults to "Model Explainer "
                        whatif=False,
                        )
db.run(host='127.0.0.1', port=9001, use_waitress=True)
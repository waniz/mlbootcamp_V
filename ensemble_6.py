import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import xgboost as xgb
from FEATURES import AddFeatures

from mlxtend.classifier import EnsembleVoteClassifier

pd.set_option('display.max_columns', 16)
pd.set_option('display.width', 1000)
plt.style.use('ggplot')
warnings.filterwarnings('ignore')

train = pd.read_csv('data/train.csv', index_col=0)
test = pd.read_csv('data/test.csv', index_col=0)

add_features = AddFeatures(train, test)
add_features.add_bmi_sist_dist_map()
add_features.add_f_score()
add_features.add_ap_features()
add_features.del_features()

train = add_features.train
test = add_features.test

Y = train['cardio'].values
train.drop('cardio', axis=1, inplace=True)
X = train


clf_0_params = {
    'learning_rate': 0.007,
    'max_depth': 5,
    'nthread': 4,
    'silent': 1,
    'subsample': 0.73,
    'reg_lambda': 0.73,
    'gamma': 0.126,
    'min_child_weight': 90.8,
    'colsample_bytree': 0.89,
    'n_estimators': 821,
}
clf_0 = xgb.XGBClassifier(**clf_0_params)

clf_1_params = {
    'learning_rate': 0.0074,
    'max_depth': 5,
    'nthread': 4,
    'silent': 1,
    'subsample': 0.72,
    'reg_lambda': 0.75,
    'gamma': 0.159,
    'min_child_weight': 85.5,
    'colsample_bytree': 0.84,
    'n_estimators': 825,
}
clf_1 = xgb.XGBClassifier(**clf_1_params)

clf_2_params = {
    'learning_rate': 0.0021,
    'max_depth': 5,
    'nthread': 4,
    'silent': 1,
    'subsample': 0.6,
    'reg_lambda': 0.89,
    'gamma': 0.1,
    'min_child_weight': 49.8,
    'colsample_bytree': 0.8,
    'n_estimators': 2790,
}
clf_2 = xgb.XGBClassifier(**clf_2_params)

clf_3_params = {
    'learning_rate': 0.0065,
    'max_depth': 5,
    'nthread': 4,
    'silent': 1,
    'subsample': 0.621,
    'reg_lambda': 0.726,
    'gamma': 0.053,
    'min_child_weight': 30.8,
    'colsample_bytree': 0.905,
    'n_estimators': 958,
}
clf_3 = xgb.XGBClassifier(**clf_3_params)

clf_4_params = {
    'learning_rate': 0.0068,
    'max_depth': 5,
    'nthread': 4,
    'silent': 1,
    'subsample': 0.69,
    'reg_lambda': 0.88,
    'gamma': 0.15,
    'min_child_weight': 67,
    'colsample_bytree': 0.77,
    'n_estimators': 904,
}
clf_4 = xgb.XGBClassifier(**clf_4_params)

# (0, 1, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21)
# (0, 1, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22) - RF
# (3, 4, 5, 6, 7, 8, 9, 10, 11, 19, 20, 22, 23)

# best_columns = [
#     'gender', 'height', 'ap_hi', 'ap_lo', 'smoke', 'alco', 'active', 'age_y',
#     'ch_1', 'ch_2', 'ch_3', 'gl_1', 'gl_2', 'gl_3',
#     'bmi', 'sist_formula', 'map', 'F_score', 'ap_log'
# ]

best_columns = [
    'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active',
    'age_y', 'bmi', 'sist_formula', 'map', 'F_score'
]


pipeline = EnsembleVoteClassifier(clfs=[clf_0, clf_1, clf_2, clf_3, clf_4], weights=[1, 1, 1, 1, 1], voting='soft')
pipeline.fit(train[best_columns], Y)

y_pred = pipeline.predict_proba(test[best_columns])
pd.Series(y_pred[:, 1]).to_csv('answer.csv', index=False)

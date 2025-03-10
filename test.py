models = {
                "Random Forest": 'RandomForestClassifier(verbose=1)',
                "Decision Tree": 'DecisionTreeClassifier()',
                "Gradient Boosting": 'GradientBoostingClassifier(verbose=1)',
                "Logistic Regression": 'LogisticRegression(verbose=1)',
                "AdaBoost": 'AdaBoostClassifier()',
            }

#print(models , '\n')

#print(list(models.values()))



params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }

for i in range(len(list(models))):
    model = list(models.values())[i]
    para = params[list(models.keys())[i]]

    print(para)
    break
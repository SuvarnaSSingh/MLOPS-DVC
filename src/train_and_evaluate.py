# load train and test files 
# train alogorithm 
# save metrics 
# save parameters 

import os 
import pandas as pd 
import sys
import numpy as np
import warnings
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import  read_params
import argparse
import joblib
import json



def eval_metrics (actual ,predicted):

    rmse = np.sqrt(mean_squared_error(actual, predicted))
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    return rmse, mae, r2
  

def train_and_evaluate(config_path):
    config=read_params(config_path)


    train_data_path=config["split_data"]["train_path"]
    test_data_path=config["split_data"]["test_path"]
    random_State=config["base"]["random_state"]
    model_dir=config["model_dir"]
    alpha=config["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio=config["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    target=config["base"]["target_col"]

    train=pd.read_csv(train_data_path,sep=",")
    test=pd.read_csv(test_data_path,sep=",")

    train_y=train[target]
    test_y=test[target]

    train_x=train.drop(target,axis=1)
    test_x=test.drop(target,axis=1)

    lr= ElasticNet(alpha=alpha,l1_ratio=l1_ratio,random_state=random_State)

    

    lr.fit(train_x,train_y)
    predicted_qualities=lr.predict(test_x)
    (rmse,mae,r2)=eval_metrics(test_y,predicted_qualities)

    print("Elastic Model (alpha=%f ,l1_ratio=%f) :" %(alpha,l1_ratio))
    print("RMSE: %s" %rmse)
    print( "Mae : %s " %mae)
    print("R2 score %s :"%r2)

    scores_file =config["reports"]["scores"]
    parame_file=config["reports"]["params"]

    with open(scores_file,"w") as f:
        scores={
            "rmse":rmse,
            "mae":mae,
            "r2":r2
        }

        json.dump(scores,f,indent=4)

    with open(parame_file,"w") as f:
        param={
            "alpha":alpha,
            "l1_ratio":l1_ratio,
          
        }    
        json.dump(param,f,indent=4) 

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")

    joblib.dump(lr, model_path)

if __name__=="__main__":
    args=argparse.ArgumentParser()
    args.add_argument("--config",default="params.yaml")
    parsed_arg=args.parse_args()
    train_and_evaluate(config_path=parsed_arg.config)
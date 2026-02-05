from airflow import DAG
from airflow.operators.python import PythonOperator   # define task based on python function
from datetime import datetime

# Task 1
def preprocess_data():
	print("Preprocessing Data")

# Task 2
def train_model():
	print("Training model")

# Task 3
def evaluate_model():
	print("Evaluate Model")

# Define DAG
with DAG(
	'ml_pipeline',
	start_date=datetime(2026,1,6),
	schedule='@weekly'
) as dag:
	
    # Define Task
	preprocess=PythonOperator(task_id="preprocess_task_id",python_callable=preprocess_data)
	train=PythonOperator(task_id="train_task_id",python_callable=train_model)
	evaluate=PythonOperator(task_id="evaluate_task_id",python_callable=evaluate_model)
	
    # set dependecies
	preprocess >> train >> evaluate
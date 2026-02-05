from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def start_number(ti):
    ti.xcom_push(key='current_value',value=10)
    print("Starting number 10")

def add_five(ti):
    current_val=ti.xcom_pull(key='current_value',task_ids='start_task')
    new_value=current_val+5
    ti.xcom_push(key='current_value',value=new_value)
    print(f"ADD 5:{current_val}+5={new_value}")

def multiply_by_two(ti):
    current_value=ti.xcom_pull(key='current_value',task_ids='add_five_task')
    new_value=current_value*2
    ti.xcom_push(key='current_value',value=new_value)
    print(f"Multiply by 2: {current_value}*2={new_value}")

def subtract_three(ti):
    current_value=ti.xcom_pull(key='current_value', task_ids='multiply_by_two_task')
    new_value=current_value-3
    ti.xcom_push(key='current_value',value=new_value)
    print(f"Subtract 3: {current_value} - 3 = {new_value}")

def square_number(ti):
    current_value=ti.xcom_pull(key='current_value',task_ids="subtract_three_task")
    new_value=current_value**2
    ti.xcom_push(key='current_value',value=new_value)
    print(f"Square: {current_value}**2 = {new_value}")

with DAG(
    dag_id='math_sequence_dag',
    start_date=datetime(2026,2,1),
    schedule='@once',
    catchup=False
) as dag:
    
    start_task=PythonOperator(
        task_id='start_task',
        python_callable=start_number
    )

    add_five_task=PythonOperator(
        task_id='add_five_task',
        python_callable=add_five
    )

    multiply_by_two_task=PythonOperator(
        task_id='multiply_by_two_task',
        python_callable=multiply_by_two
    )

    subtract_three_task=PythonOperator(
        task_id='subtract_three_task',
        python_callable=subtract_three
    )

    square_number_task=PythonOperator(
        task_id='square_number_task',
        python_callable=square_number
    )
    

    start_task >> add_five_task >> multiply_by_two_task >> subtract_three_task >> square_number_task
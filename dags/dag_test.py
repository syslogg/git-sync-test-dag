from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

with DAG(
    dag_id="kubernetes_pod_operator_example",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["kubernetes"],
) as dag:
    # A primeira tarefa que executa um Pod com um comando simples
    task1 = KubernetesPodOperator(
        task_id="primeira_tarefa",
        namespace="default",  # Altere para o seu namespace do Kubernetes
        image="python:3.9-slim",  # Imagem Python padrão
        cmds=["python", "-c"],
        arguments=["print('Executando a primeira tarefa. Argumento: Olá do Pod 1!')"],
        do_xcom_push=False, # Não é necessário enviar dados entre as tarefas, mas é uma opção
    )

    # A segunda tarefa, que depende da primeira
    task2 = KubernetesPodOperator(
        task_id="segunda_tarefa",
        namespace="default",
        image="python:3.9-slim",
        cmds=["python", "-c"],
        arguments=["print('Executando a segunda tarefa. Argumento: Este é o Pod 2!')"],
    )

    # A terceira tarefa, que depende da segunda
    task3 = KubernetesPodOperator(
        task_id="terceira_tarefa",
        namespace="default",
        image="python:3.9-slim",
        cmds=["python", "-c"],
        arguments=["print('Executando a terceira tarefa. Argumento: O Pod 3 está online!')"],
    )

    # A quarta tarefa, que depende da terceira
    task4 = KubernetesPodOperator(
        task_id="quarta_tarefa",
        namespace="default",
        image="python:3.9-slim",
        cmds=["python", "-c"],
        arguments=["print('Executando a quarta e última tarefa. Argumento: Missão Pod 4!')"],
    )

    # Definindo as dependências entre as tarefas
    task1 >> task2 >> task3 >> task4
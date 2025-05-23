FROM apache/airflow:2.9.1-python3.10

COPY airflow_service/requirements.txt /workdir/
COPY for_pip_install/* /workdir/

WORKDIR /workdir

RUN pip install --upgrade pip

RUN pip uninstall keras
RUN pip uninstall tensorflow
# RUN pip cache purge

RUN pip install ./train_and_valid_model-0.2.15-py3-none-any.whl
RUN pip install ./preprocess_data-0.1.16-py3-none-any.whl

RUN pip install -r /requirements.txt


import sys
import os
import logging
import traceback
from rmq_custom_pack import rpc_producer
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO, filename=f"py_log_producer_{os.environ.get('PROD_NUM')}.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

CSV_FILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'csv_files')

PROD_NUM=os.environ.get('PROD_NUM')
FILENAME=f"train_FD001.csv"
TIME_SLEEP = 0

HOST=os.environ.get('HOST')
PORT=os.environ.get('PORT')
USER=os.environ.get('USER')
PASSWORD=os.environ.get('PASSWORD')

# print(f"[HOST]: {HOST}, [PORT]: {PORT}, [USER]: {USER}, [PASSWORD]: {PASSWORD}")
logging.info(f"[HOST]: {HOST}, [PORT]: {PORT}, [USER]: {USER}, [PASSWORD]: {PASSWORD}")

REPO_URL=os.environ.get('REPO_URL')
TOKEN=os.environ.get('TOKEN')
URL_PATH_STORAGE=os.environ.get('URL_PATH_STORAGE')

EXCHANGE=os.environ.get('EXCHANGE')
EXCHANGE_TYPE=os.environ.get('EXCHANGE_TYPE')
QUEUE_REQUEST=os.environ.get('QUEUE_REQUEST')
QUEUE_RESPONSE=os.environ.get('QUEUE_RESPONSE')
ROUTING_KEY_REQUEST=f"{os.environ.get('ROUTING_KEY_REQUEST')}{PROD_NUM}"
ROUTING_KEY_RESPONSE=f"{os.environ.get('ROUTING_KEY_RESPONSE')}{PROD_NUM}"

# print(f"""[EXCHANGE]: {EXCHANGE}, 
#              [EXCHANGE_TYPE]: {EXCHANGE_TYPE}, 
#              [QUEUE_REQUEST]: {QUEUE_REQUEST}, 
#              [QUEUE_RESPONSE]: {QUEUE_RESPONSE}, 
#              [ROUTING_KEY_REQUEST]: {ROUTING_KEY_REQUEST}, 
#              [ROUTING_KEY_RESPONSE]: {ROUTING_KEY_RESPONSE}""")
logging.info(f"""[EXCHANGE]: {EXCHANGE}, 
             [EXCHANGE_TYPE]: {EXCHANGE_TYPE}, 
             [QUEUE_REQUEST]: {QUEUE_REQUEST}, 
             [QUEUE_RESPONSE]: {QUEUE_RESPONSE}, 
             [ROUTING_KEY_REQUEST]: {ROUTING_KEY_REQUEST}, 
             [ROUTING_KEY_RESPONSE]: {ROUTING_KEY_RESPONSE}""")


def main():
    try:
        # print('An instance of the class must be obtained')
        logging.info('An instance of the class must be obtained')
        producer = rpc_producer.Producer(host=HOST,
                                port=PORT,
                                user=USER,
                                password=PASSWORD,
                                exchange=EXCHANGE,
                                exchange_type=EXCHANGE_TYPE,
                                queue_request=QUEUE_REQUEST,
                                queue_response=QUEUE_RESPONSE,
                                r_key_request=ROUTING_KEY_REQUEST,
                                r_key_response=ROUTING_KEY_RESPONSE)
        # print('Received an instance of the class')
        logging.info('Received an instance of the class')
    except Exception as e:
        print(traceback.format_exc())
        logging.exception(e)
        logging.error(traceback.format_exc())

    try:
        producer_handler_res = producer.producer_handler(prod_num=PROD_NUM,
                                                         csv_files_dir=CSV_FILES_DIR,
                                                         filename=FILENAME,
                                                         time_sleep=TIME_SLEEP)
        # print(f"consumer_handler_res: {producer_handler_res['basic_consume_res']}")
        logging.info(f"consumer_handler_res: {producer_handler_res['data_publish_res']}")
        print(f"consumer_handler_res: {producer_handler_res['data_publish_res']}")
    except Exception as e:
        # print(traceback.format_exc())
        logging.exception(e)
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    main()
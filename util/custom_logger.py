import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler


def set_logger(log_dir_path):
    # 현재 파일 경로 및 파일명 찾기
    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_file = os.path.basename(__file__)
    current_file_name = current_file[:-3] + ".log".__str__()  # xxxx.py
    log_filename = '{}'.format(current_file_name)
    config_filepath = os.path.join(current_dir, '../conf/logging.conf')

    # 로그 저장할 폴더 생성
    # log_dir = '{}/logs'.format(current_dir)
    log_dir = '{}/logs'.format(log_dir_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    str_log_file_name = 'logs/' + log_filename
    logging.config.fileConfig(config_filepath, disable_existing_loggers=False,
                              defaults={"str_log_file_name": str_log_file_name})

    # disable_existing_loggers=False: 기 존재 로거도 계속 사용하도록 한다
    logger = logging.getLogger("log03")

    return logger

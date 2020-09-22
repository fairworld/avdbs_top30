import logging
import logging.config
import os
from logging.handlers import RotatingFileHandler


def set_logger():
    # # Logger
    # logger = logging.getLogger(__name__)
    #
    # # formatter 생성
    # formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
    #
    # # handler 생성(stream, file)
    # streamHandler = logging.StreamHandler()
    # fileHandler = RotatingFileHandler('./'.__str__()+logfilename, maxBytes=1024 * 1024 * 10, backupCount=10)
    #
    # # logger instance에 formatter 설정
    # streamHandler.setFormatter(formatter)
    # fileHandler.setFormatter(formatter)
    #
    # # logger instance에 handler 설정
    # logger.addHandler(streamHandler)
    # logger.addHandler(fileHandler)
    #
    # # logger 설정
    # logger.setLevel(level=logging.DEBUG)

    # 현재 파일 경로 및 파일명 찾기
    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_file = os.path.basename(__file__)
    current_file_name = current_file[:-3] + ".log".__str__()  # xxxx.py
    log_filename = '{}'.format(current_file_name)

    # 로그 저장할 폴더 생성
    log_dir = '{}/logs'.format(current_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    str_log_file_name = 'logs/' + log_filename
    logging.config.fileConfig("conf/logging.conf", disable_existing_loggers=False, defaults={"str_log_file_name": str_log_file_name})
    # disable_existing_loggers=False: 기 존재 로거도 계속 사용하도록 한다
    logger = logging.getLogger("log03")

    return logger

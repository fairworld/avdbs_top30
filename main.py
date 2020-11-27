import os
import re

import find_titles as ft
import find_link as fl
import download_qbittorrent as dq
from util import custom_logger_v2

if __name__ == '__main__':
    # logger 설정
    filename = re.sub('.py', '.log', os.path.basename(__file__))
    log_dir = os.path.dirname(os.path.realpath(__file__))
    logger = custom_logger_v2.set_logger(log_dir, filename)

    logger.info("1. 품번 검색을 시작합니다.")
    ft.find_titles(logger)
    logger.info("2. 품번별 링크 검색을 시작합니다.")
    fl.find_link(logger)
    logger.info("3. 검색된 링크에서 다운로드를 시작합니다.")
    dq.download(logger)
    logger.info("작업이 완료되었습니다.")

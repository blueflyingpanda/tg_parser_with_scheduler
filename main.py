#!/usr/bin/env python

from tg_app_info import TelegramAppInfoFromJson
from tg_parser import TelegramChatParserToCsvStatistics
from tg_scheduler import TelegramParserScheduler
from keywords_parser import KeywordsParserFromTxt
import logging
import datetime
import pytz

utc = pytz.UTC

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.warning('This will get logged to a file')

CHAT_NAME = "Чат Теплица.Курсы"


if __name__ == "__main__":

    app_info = TelegramAppInfoFromJson()
    logging.info("Ladybug")
    app_info.read_config(conf="tg_id_and_hash.json")  # get api_id and api_hash
    logging.info("Config read")
    kw_parser = KeywordsParserFromTxt()
    kw_parser.read_keywords(keywords_file="keywords.txt")
    with open('start_date.txt') as file:
        sdate = file.readline().strip()
        start_date = datetime.datetime.strptime(sdate, '%d/%m/%y').replace(tzinfo=utc)
    logging.info(kw_parser.keywords)
    chat_parser = TelegramChatParserToCsvStatistics(app_info, CHAT_NAME,
                                                    keywords=kw_parser.keywords,
                                                    table_path="chat_data.csv",
                                                    tmp_path="tmp.csv",
                                                    start_date=start_date
                                                    )

    logging.info("sh")
    scheduler = TelegramParserScheduler(TelegramParserScheduler.DAY, chat_parser)
    logging.info("before")
    scheduler.run_parser()

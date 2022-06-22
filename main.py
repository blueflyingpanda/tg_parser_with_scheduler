#!/usr/bin/env python

from tg_app_info import TelegramAppInfoFromJson
from tg_parser import TelegramChatParserToCsvStatistics
from tg_scheduler import TelegramParserScheduler
from keywords_parser import KeywordsParserFromTxt
import logging

logging.basicConfig(filename='/home/tg_parser_Teplitsa/app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.warning('This will get logged to a file')

CHAT_NAME = "Чат Теплица.Курсы"


if __name__ == "__main__":

    app_info = TelegramAppInfoFromJson()
    logging.info("Ladybug")
    app_info.read_config(conf="/home/tg_parser_Teplitsa/tg_id_and_hash.json")  # get api_id and api_hash
    logging.info("Config read")
    kw_parser = KeywordsParserFromTxt()
    kw_parser.read_keywords(keywords_file="/home/tg_parser_Teplitsa/keywords.txt")
    logging.info(kw_parser.keywords)
    chat_parser = TelegramChatParserToCsvStatistics(app_info, CHAT_NAME,
                                                    keywords=kw_parser.keywords,
                                                    table_path="/home/tg_parser_Teplitsa/chat_data.csv",
                                                    json_path="/home/tg_parser_Teplitsa/chat_data.json"
                                                    )

    logging.info("sh")
    scheduler = TelegramParserScheduler(TelegramParserScheduler.DAY, chat_parser)
    logging.info("before")
    scheduler.run_parser()

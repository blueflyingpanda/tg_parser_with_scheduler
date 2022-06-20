from tg_app_info import TelegramAppInfoFromJson
from tg_parser import TelegramChatParserToCsvStatistics
from tg_scheduler import TelegramParserScheduler
from keywords_parser import KeywordsParserFromTxt


CHAT_NAME = "Тест"


if __name__ == "__main__":

    app_info = TelegramAppInfoFromJson()
    app_info.read_config(conf="tg_id_and_hash.json")  # get api_id and api_hash

    kw_parser = KeywordsParserFromTxt()
    kw_parser.read_keywords(keywords_file="keywords.txt")

    chat_parser = TelegramChatParserToCsvStatistics(app_info, CHAT_NAME,
                                                    keywords=kw_parser.keywords,
                                                    table_path="chat_data.csv",
                                                    json_path="chat_data.json"
                                                    )

    scheduler = TelegramParserScheduler(TelegramParserScheduler.DAY, chat_parser)
    scheduler.run_parser()

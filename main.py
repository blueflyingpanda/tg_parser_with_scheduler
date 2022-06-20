from tg_app_info import TelegramAppInfoFromJson
from tg_parser import TelegramChatParserToCsvStatistics
from tg_scheduler import TelegramParserScheduler


CHAT_NAME = "Тест"


if __name__ == "__main__":

    app_info = TelegramAppInfoFromJson()
    app_info.read_config(conf="tg_id_and_hash.json")  # get api_id and api_hash

    chat_parser = TelegramChatParserToCsvStatistics(app_info, CHAT_NAME,
                                                    keywords={"отчетдня", "отчет_дня"},
                                                    table_path="chat_data.csv")

    scheduler = TelegramParserScheduler(TelegramParserScheduler.DAY, chat_parser)
    scheduler.run_parser()

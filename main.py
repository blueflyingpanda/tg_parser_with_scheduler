from tg_app_info import TelegramAppInfoFromJson
from tg_parser import TelegramChatParserToCsv
from tg_scheduler import TelegramParserScheduler


CHAT_NAME = "Журналистика данных"


if __name__ == "__main__":

    app_info = TelegramAppInfoFromJson()
    app_info.read_config(conf="tg_id_and_hash.json")  # get api_id and api_hash

    chat_parser = TelegramChatParserToCsv(app_info, CHAT_NAME, keywords={"спасибо"}, table_path="chat_data.csv")

    scheduler = TelegramParserScheduler(TelegramParserScheduler.DAY, chat_parser)
    scheduler.run_parser()

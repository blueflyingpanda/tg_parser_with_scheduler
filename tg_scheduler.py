from time import sleep, time
from tg_parser import TelegramChatParser

class TelegramParserScheduler:

    """Schedules the parser"""

    SECOND = 1
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY

    def __init__(self, period_in_seconds: int, parser: TelegramChatParser) -> None:
        self._period_in_seconds = period_in_seconds
        self._next_time_to_parse = self.current_time
        self._parser = parser

    def run_parser(self):

        INTERVAL_IN_SECONDS = self.HOUR

        while True:
            if self.current_time >= self._next_time_to_parse:
                self._next_time_to_parse = self.current_time + self._period_in_seconds
                self._parser.parse(self._period_in_seconds)
                self._parser.save()
            sleep(INTERVAL_IN_SECONDS)

    @property
    def current_time(self):
        return time()
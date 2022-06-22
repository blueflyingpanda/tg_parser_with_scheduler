from abc import ABC, abstractmethod
from pathlib import Path


class KeywordsParser(ABC):

    keywords: set = set()

    @abstractmethod
    def read_keywords(self, keywords_file: Path):
        pass


class KeywordsParserFromTxt(KeywordsParser):

    def read_keywords(self, keywords_file: str):
        with open(keywords_file) as file:
            for line in file:
                self.keywords.add(line.strip())

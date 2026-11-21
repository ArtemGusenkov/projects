from typing import TypedDict, Literal
from pydantic import Field

class ModMessageState(TypedDict):
    question: str
    question_type: Literal['quotes','news','commodities','recommendation','other','not_finance'] | None = None
    history: list[dict[str, str]]
    answer: str
    ticker: str

class ClassifierAnswer(TypedDict):
    question_type: Literal['quotes','news','commodities','recommendation','other','not_finance']

class TickerFind(TypedDict):
    ticker: str

class StocksAnswer(TypedDict):
    answer: str
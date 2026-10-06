from typing import TypedDict, Literal

class ModMessageState(TypedDict):
    question: str
    question_type: Literal['quotes','news','commodities','recommendation','other','not_finance'] | None = None
    history: list[dict[str, str]]
    answer: str

class ClassifierAnswer(TypedDict):
    question_type: Literal['quotes','news','commodities','recommendation','other','not_finance']
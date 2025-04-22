from enum import Enum


class SymbolStatus(Enum):
    TRADING = "TRADING"
    BREAK = "BREAK"
    HALT = "HALT"
    AUCTION = "AUCTION"
    DORMANT = "DORMANT"



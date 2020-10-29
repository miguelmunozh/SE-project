from enum import Enum

class SeverityCategoryCode(int,Enum):
    I:int = 10
    II:int = 7
    III:int = 4

    @staticmethod
    def getMember(value: int):
        for member in SeverityCategoryCode:
            if member.value == value:
                return member
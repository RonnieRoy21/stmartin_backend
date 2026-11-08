

from pydantic import BaseModel

class Counsellor(BaseModel):
    name:str


class ScheduleModel(BaseModel):
    counsellors:Counsellor
    day:str
    time:str
    date:int
    month:str
    year:int
    is_cancelled:bool




from pydantic import BaseModel


class EventModel(BaseModel):

    name: str
    date: str
    venue: str
    description: str
    time: str

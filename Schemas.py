from pydantic import BaseModel


class ModerateResponseOK(BaseModel):
    status: str

class ModerateResponseRejected(BaseModel):
    status: str
    reason: str
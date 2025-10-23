from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class ZendeskTicket(BaseModel):
    id:str
    subject:str
    description:str
    priority:str
    status:str
    assignee_id:str
    requester_id:str
    created_at:str
    updated_at:str
    type:str
    tags:str
    url:str
from pydantic import BaseModel


class GetActivityDetail(BaseModel):
    id: str
    server_id: str
    server_name: str
    action: str
    detail: str
    timestamp: str
    
    @classmethod
    def from_doc(cls, doc: dict) -> "GetActivityDetail":
        from utils.datetime_utils import format_datetime
        return cls(
            id=str(doc["_id"]),
            server_id=str(doc["server_id"]),
            server_name=doc["server_name"],
            action=doc["action"],
            detail=doc["detail"],
            timestamp=format_datetime(doc["timestamp"]),
        )
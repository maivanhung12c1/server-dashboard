import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

_IPV4_RE = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)
_IPV6_RE = re.compile(r"^[0-9a-fA-F:]{2,39}$")
_VALID_STATUSES = {"Online", "Offline"}


class CreateServerParam(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    ip_address: str = Field(..., min_length=7, max_length=45)
    country: str = Field(..., min_length=2, max_length=100)
    os: str = Field(..., min_length=1, max_length=100)
    os_version: str = Field(..., min_length=1, max_length=100)
    platform: str = Field(..., min_length=1, max_length=100)
    arch: str = Field(..., min_length=1, max_length=50)
    status: str = Field(default="Online")

    @field_validator("ip_address")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        v = v.strip()
        if _IPV4_RE.match(v) or _IPV6_RE.match(v):
            return v
        raise ValueError(f"Invalid IP address: {v!r}")
    
    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        if v not in _VALID_STATUSES:
            raise ValueError(f"Status must be one of: {_VALID_STATUSES}")
        return v
    
    
class UpdateServerParam(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    ip_address: Optional[str] = Field(None, min_length=7, max_length=45)
    country: Optional[str] = Field(None, min_length=2, max_length=100)
    os: Optional[str] = Field(None, min_length=1, max_length=100)
    os_version: Optional[str] = Field(None, min_length=1, max_length=100)
    platform: Optional[str] = Field(None, min_length=1, max_length=100)
    arch: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = None
    
    @field_validator("ip_address", mode="before")
    @classmethod
    def validate_ip(cls, v):
        if v is None:
            return v
        v = str(v).strip()
        if _IPV4_RE.match(v) or _IPV6_RE.match(v):
            return v
        raise ValueError(f"Invalid IP address: {v!r}")

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, v):
        if v is None:
            return v
        if v not in _VALID_STATUSES:
            raise ValueError(f"Status must be one of: {_VALID_STATUSES}")
        return v
    
    
class GetServerDetail(BaseModel):
    id: str
    name: str
    ip_address: str
    country: str
    os: str
    os_version: str
    platform: str
    arch: str
    status: str
    created_at: str
    updated_at: str
    
    @classmethod
    def from_doc(cls, doc: dict) -> "GetServerDetail":
        from utils.datetime_utils import format_datetime
        return cls(
            id=str(doc["_id"]),
            name=doc["name"],
            ip_address=doc["ip_address"],
            country=doc["country"],
            os=doc["os"],
            os_version=doc["os_version"],
            platform=doc["platform"],
            arch=doc["arch"],
            status=doc["status"],
            created_at=format_datetime(doc["created_at"]),
            updated_at=format_datetime(doc["updated_at"]),
        )
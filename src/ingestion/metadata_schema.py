from pydantic import BaseModel
from typing import Literal

ALL_DEPTS = ["finance", "marketing", "hr", "engineering", "clevel", "general", "employee"]


class DocumentMetadata(BaseModel):
    doc_id: str
    chunk_id: str
    title: str
    department: str
    # Per-department boolean access flags (Chroma $eq filter compatible)
    dept_finance: bool = False
    dept_marketing: bool = False
    dept_hr: bool = False
    dept_engineering: bool = False
    dept_clevel: bool = False
    dept_general: bool = False
    dept_employee: bool = False
    classification: Literal["public", "internal", "confidential", "restricted"]
    doc_type: str
    source_file: str
    chunk_index: int
    total_chunks: int
    created_date: str = ""

    @classmethod
    def from_access_roles(cls, access_roles: list[str], **kwargs) -> "DocumentMetadata":
        flags = {f"dept_{d}": (d in access_roles) for d in ALL_DEPTS}
        return cls(**flags, **kwargs)

    def to_chroma_dict(self) -> dict:
        return self.model_dump()

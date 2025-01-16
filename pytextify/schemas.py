from typing import Optional

from pydantic import BaseModel


class ImageSchema(BaseModel):
    image_base64: str


class TaskSchema(BaseModel):
    task_id: str
    status: str


class TaskResultSchema(TaskSchema):
    result: Optional[list] = None

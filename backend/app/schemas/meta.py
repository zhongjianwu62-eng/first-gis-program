from pydantic import BaseModel


class MetaResponse(BaseModel):
    project_name: str
    study_area: str
    data_version: str
    stage: str

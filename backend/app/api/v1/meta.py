from fastapi import APIRouter

from app.schemas.meta import MetaResponse

router = APIRouter()


@router.get("/meta", response_model=MetaResponse)
def get_meta() -> MetaResponse:
    return MetaResponse(
        project_name="厦门市思明区路网结构与可步行性分析平台",
        study_area="福建省厦门市思明区",
        data_version="not-loaded",
        stage="D6 scaffold",
    )

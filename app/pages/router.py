from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/pages',
    tags=['Фронтенд']
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels=Depends()
):
    return templates.TemplateResponse(
        request=request,
        name="hotels.html",
        context={"request": request}
    )

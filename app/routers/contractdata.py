from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


router = APIRouter(prefix='/contractdata')
templates = Jinja2Templates(directory="app/templates/")


@router.get("/", response_class=HTMLResponse)
def get_contractdata(request: Request):
    return templates.TemplateResponse(request, "pages/contractdata.html")

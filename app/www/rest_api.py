from fastapi import FastAPI, Request
import urllib
import config
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import DroneSdk.sdk

app_fastapi = config.app_fastapi

class CustomURLProcessor:
    def __init__(self):
        self.path = ""
        self.request = None

    def url_for2(self, request: Request, name: str):
        return  f"{request.base_url}{name}"

    def url_for(self, request: Request, name: str, **params: str):
        self.path = request.url_for(name, **params)
        self.request = request
        return self



from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
templates.env.globals['CustomURLProcessor'] = CustomURLProcessor
app_fastapi.mount("/static", StaticFiles(directory="static"), name="static")
app_fastapi.mount("/images", StaticFiles(directory="static/images"), name="images")
@app_fastapi.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item2.html", {"request": request, "id": id})

@app_fastapi.get("/joystick", response_class=HTMLResponse)
async def joystick(request: Request):
    return templates.TemplateResponse("joystick.html", {"request": request, "id": id})

if __name__=="__main__":
    import uvicorn
    uvicorn.run("rest_api:app_fastapi",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)

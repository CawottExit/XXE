import traceback

from fastapi import FastAPI, Request, APIRouter, UploadFile, File
from xml.dom.pulldom import START_ELEMENT, parse, parseString
from fastapi.templating import Jinja2Templates
from lxml import etree
templates = Jinja2Templates(directory="templates")
import cgi

app = FastAPI()
api_router = APIRouter()


@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request})

@app.post("/")
async def post_root(file: UploadFile = File(...)):
    """
    try:

            print(file)
            content = file.file.read().decode()
            doc = parseString(content)
            for event, node in doc:
                doc.expandNode(node)
            print(str(doc))
    except Exception as e:
        return {"message": f"There was an error uploading the file {e}"}
    finally:
        file.file.close()
    """
    html = ""
    parsed_xml = None
    parser = etree.XMLParser(no_network=False)  # to enable network entity. see xmlparser-info.txt
    try:
        content = file.file.read()
        doc = etree.fromstring(content, parser)
        parsed_xml = etree.tostring(doc)
        print(repr(parsed_xml))
    except:
        print("Cannot parse the xml")
        html += "Error:\n<br>\n" + traceback.format_exc()
    if (parsed_xml):
        html += "Result:\n<br>\n" + str(parsed_xml)
        return {html}
    """
    doc = parse(file)
    for event, node in doc:
        doc.expandNode(node)
    return templates.TemplateResponse(
        "index.html", {'doc': str(doc)})
    """

@app.post('/pullxml')
def pulldom(request: Request):
    doc = parse(request)
    for event, node in doc:
        doc.expandNode(node)
    return(str(doc))
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

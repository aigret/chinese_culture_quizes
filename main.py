
# from enum import Enum
from typing import Union, Any
from fastapi import FastAPI, Header,  Request 
from fastapi.templating import Jinja2Templates
from fastapi.responses import  HTMLResponse
from fastapi.staticfiles import StaticFiles

from jinja2 import Environment, FileSystemLoader, select_autoescape


import pandas as pd

import numpy as np


env = Environment(
    loader = FileSystemLoader('templates'),
    autoescape=select_autoescape()
)

def extract_choices(s:str) -> {}:
    """
    extract the choices from a string contains A. B. C. ...
    use re
    return a dict of option
    """
    import re
    ptn = re.compile('[ABCDEF]\.?')
    l= ptn.split(s)
    l.remove('')
    ablist = list('ABCDEF')
    return dict(zip(ablist[:len(l)], l))


raw_data = pd.read_csv('t2.csv')
raw_data.columns = ['item_id','Q','C','answer']

raw_data.C = raw_data.C.apply(extract_choices)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"User-Agent": Header(default=None)}



@app.get("/items/", response_class=HTMLResponse)
async def read_items (request: Request):
    
    data = raw_data.to_dict(orient='records')
    template = Jinja2Templates(directory="templates")
    # template = env.get_template('items.html')
    # return template.render(items = data)
    return template.TemplateResponse("items.html", {"request": request, "items":data})
    

     

@app.get("/items/{item_id}", response_class=HTMLResponse)
async def read_item(item_id: int, q: Union[int, None] = None, request: Request = None):
   
    data = raw_data.to_dict(orient='records')
 
    # item = data[item_id]
    template = env.get_template('item.html')
    # item_list = ["127.0.0.1:8000/items/"+str(e) for e in range(len(data))]
    # return template.render(item)
    return template.render(item = data[item_id])


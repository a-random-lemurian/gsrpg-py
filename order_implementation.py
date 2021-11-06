import json
from main import GSRPG_DATA_FILE_PATH

gsrpg = json.load(open(GSRPG_DATA_FILE_PATH,'r',encoding='UTF-8'))

def new_building(type: str, quantity: int):
    pass
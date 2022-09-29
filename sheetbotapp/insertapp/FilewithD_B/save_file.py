from .file_to_desk import Saveindeck
from .file_to_DB import save_in_DB
def save_file(data:dict):
    data = Saveindeck(data)
    sql = save_in_DB(data)
    if sql == False:
        return 'Fell to save in DB'
    else:
        return sql
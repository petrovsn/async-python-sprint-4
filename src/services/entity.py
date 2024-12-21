from models.url_record import UrlRecord as UrlRecordModel
from .repository import RepositoryDB

class RepositoryEntity(RepositoryDB[UrlRecordModel]): #, EntityCreate, EntityUpdate
    pass

entity_crud = RepositoryEntity(UrlRecordModel) 
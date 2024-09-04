from services.models import ServiceModel
from utils.repository import SQLAlchemyRepository


class ServiceRepository(SQLAlchemyRepository):
    model = ServiceModel

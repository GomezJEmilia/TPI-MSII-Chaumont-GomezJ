from .repository import InMemoryRequestRepository
from .service import RequestService


def create_service():
    return RequestService(InMemoryRequestRepository())

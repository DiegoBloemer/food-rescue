from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..db import get_session
from ..schemas import ClaimCreate, ClaimRead
from ..services.claim_service import ClaimService

router = APIRouter(prefix="/claims", tags=["claims"])


def get_claim_service(
    session: Session = Depends(get_session),
) -> ClaimService:
    return ClaimService(session)


@router.post("", response_model=ClaimRead)
def create_claim(
    payload: ClaimCreate,
    service: ClaimService = Depends(get_claim_service),
):
    return service.create_claim(payload)
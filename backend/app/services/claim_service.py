from fastapi import HTTPException
from sqlmodel import Session, select

from ..models import Claim, Listing, NGO
from ..schemas import ClaimCreate


class ClaimService:
    def __init__(self, session: Session):
        self.session = session

    def create_claim(self, payload: ClaimCreate) -> Claim:
        listing = self.session.get(Listing, payload.listing_id)
        if listing is None:
            raise HTTPException(status_code=404, detail="Listing not found")

        if listing.status != "OPEN":
            raise HTTPException(
                status_code=400,
                detail="Listing is not open for claims"
            )

        ngo = self.session.get(NGO, payload.ngo_id)
        if ngo is None:
            raise HTTPException(status_code=404, detail="NGO not found")

        duplicate = self.session.exec(
            select(Claim).where(
                Claim.listing_id == payload.listing_id,
                Claim.ngo_id == payload.ngo_id
            )
        ).first()

        if duplicate is not None:
            raise HTTPException(status_code=409, detail="Duplicate claim")

        claim = Claim(**payload.model_dump())
        listing.status = "CLAIMED"

        self.session.add(claim)
        self.session.add(listing)
        self.session.commit()
        self.session.refresh(claim)

        return claim
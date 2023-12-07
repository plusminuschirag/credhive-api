from fastapi import APIRouter, Depends, HTTPException, Request, status
from .authentication.authenticate import verify_token
from data.validators.credit_data import CreditData, PutCreditData
from data.models.credit_model import CreditModel
from clients.rate_limiting_client import limiter

router = APIRouter()


@router.get("/", summary="Get All Credits", tags=["Credits"])
@limiter.limit("5/minute")
async def get_credits(request: Request, current_user: str = Depends(verify_token)):
    """
    Retrieve all credit entries.

    This endpoint returns a list of all credit entries in the system.
    The response is rate-limited to 5 requests per minute.
    """
    all_credit_data = CreditModel.get_all_credits()
    if not all_credit_data:  # Checking if the list is empty
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No credits found")
    return {"data": all_credit_data}


@router.get("/{id}", summary="Get Credit By ID", tags=["Credits"])
@limiter.limit("5/minute")
async def get_credit_by_id(id: str, request: Request, current_user: str = Depends(verify_token)):
    """
    Retrieve a specific credit entry by its ID.
    The response is rate-limited to 5 requests per minute.
    """
    id_data = CreditModel.get_id_credit(id=id)
    if not id_data:
        raise HTTPException(status_code=404, detail="Credit ID not found")
    return {"data": id_data}


@router.post("/", summary="Add New Credit", tags=["Credits"])
@limiter.limit("3/minute")
async def add_new_credit(credit_data: CreditData, request: Request, current_user: str = Depends(verify_token)):
    """
    Add a new credit entry to the system.

    This endpoint is rate-limited to 3 requests per minute.
    """
    # Logic to add new credit
    # saved = save_credit(credit_data)
    saved, message = CreditModel.save_credit(credit_data)
    if not saved:
        raise HTTPException(status_code=400, detail=message)
    return {"saved": credit_data}


@router.put("/{id}", summary="Update Credit", tags=["Credits"])
@limiter.limit("10/minute")
async def update_credit(
    id: str, credit_data: PutCreditData, request: Request, current_user: str = Depends(verify_token)
):
    """
    Update an existing credit entry by its ID.
    """
    updated = CreditModel.update_credit_data(id, credit_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Credit ID not found for update")
    return {"updated": updated}


@router.delete("/{id}", summary="Delete Credit", tags=["Credits"])
@limiter.limit("3/minute")
async def delete_credit(id: str, request: Request, current_user: str = Depends(verify_token)):
    """
    Delete a credit entry from the system by its ID.
    """
    deleted = CreditModel.delete_credit_by_id(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Credit ID not found for deletion")
    return {"deleted_credit_id": id}

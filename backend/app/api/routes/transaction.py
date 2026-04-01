from datetime import date
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.core.db import get_db
from app.services.transaction_service import ( 
    create_transaction, 
    get_transaction, 
    list_transactions, 
    update_transaction, 
    delete_transaction
)
from app.models.user import User
from app.core.dependencies import get_current_user
from app.models.transaction import TransactionCategory, TransactionType
from app.services.exceptions import NoFieldToPatchError

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransactionResponse)
def create_transaction_route(payload: TransactionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transaction = create_transaction(db, user, payload)
    return transaction

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TransactionResponse])
def list_transactions_route(
    type: Optional[TransactionType] = None,
    category: Optional[TransactionCategory] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)
    ):
        
    transactions = list_transactions(
        db, 
        user, 
        type,
        category,
        start_date,
        end_date,
        limit,
        offset
    )
    
    return transactions

@router.get("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=TransactionResponse)
def get_transaction_route(transaction_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    transaction = get_transaction(db, user, transaction_id)
    if transaction is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar a transação."
        )
    return transaction

@router.patch("/{transaction_id}", status_code=status.HTTP_200_OK, response_model=TransactionResponse)
def patch_transaction_route(transaction_id: UUID, payload: TransactionUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        transaction = update_transaction(db, user, transaction_id, payload)
        if transaction is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Não foi possível encontrar a transação."
            )
        return transaction
    
    except NoFieldToPatchError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Não foi recebido nenhum campo para atualizar."
        )

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_route(transaction_id: UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    is_deleted = delete_transaction(db, user, transaction_id)
    if is_deleted is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Não foi possível encontrar a transação."
        )
    return

from datetime import date, datetime, time, timedelta, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.transaction import Transaction, TransactionCategory, TransactionType
from app.schemas.transactions import TransactionCreate, TransactionUpdate
from app.services.exceptions import NoFieldToPatchError

def create_transaction(db: Session, user: User, data: TransactionCreate) -> Transaction:
    
    new_transaction = Transaction(
        user_id = user.id,
        type=data.type,
        amount=data.amount,
        description=data.description,
        occurred_at=data.occurred_at,
        category=data.category
    )
    db.add(new_transaction)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(new_transaction)
    return new_transaction


def list_transactions(
        db: Session,
        user: User,
        type: Optional[TransactionType],
        category: Optional[TransactionCategory],
        start_date: Optional[date],
        end_date: Optional[date],
        limit: int = 20,
        offset: int = 0
    ) -> List[Transaction]:
        query = db.query(Transaction).filter(Transaction.user_id == user.id)
        
        if type:
            query = query.filter(Transaction.type == type)
        
        if category:
            query = query.filter(Transaction.category == category)

        if start_date:
            start_dt = datetime.combine(
                                        start_date, 
                                        time.min, 
                                        tzinfo=timezone.utc
                                        )
            
            query = query.filter(Transaction.occurred_at >= start_dt)

        if end_date:
            end_dt_exclusive = datetime.combine(
                                        end_date + timedelta(days=1), 
                                        time.min, 
                                        tzinfo=timezone.utc
                                        )
            query = query.filter(Transaction.occurred_at < end_dt_exclusive)
        
        result = (
            query
            .order_by(Transaction.occurred_at.desc())
            .offset(offset).limit(limit)
            .all()
            )
        
        return result
             

def get_transaction(db: Session, user: User, transaction_id: UUID) -> Transaction:
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.user_id == user.id
        )
        .first()
    )
    return transaction

    

def update_transaction(db: Session, user: User, transaction_id: UUID, data: TransactionUpdate) -> Transaction | None:
    
    transaction = get_transaction(db, user, transaction_id)
    if not transaction:
        return None
    
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise NoFieldToPatchError("Nenhum campo preenchido para atualizar.")
    
    for key, value in updates.items():
        setattr(transaction, key, value)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise 
    db.refresh(transaction)
    return transaction

def delete_transaction(db: Session, user: User, transaction_id: UUID) -> bool | None:
    transaction = get_transaction(db, user, transaction_id)
    if not transaction:
        return None
    
    db.delete(transaction)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    return True
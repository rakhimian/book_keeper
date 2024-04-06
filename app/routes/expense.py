from ..models import expense as expense_model
from ..schemas import expense as expense_schema
from fastapi import status, Depends, APIRouter, HTTPException, Response
from ..repository.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.user.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/expenses',
    tags=["Expenses"]
)

user_repository = UserRepository()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[expense_schema.Expense])
def get_expenses(db: Session = Depends(get_db),
                 current_user: int = Depends(user_repository.get_current_user),
                 limit: int = 10,
                 skip: int = 0,
                 search: Optional[str] = "",
                 amount_from: Optional[int] = 0,
                 amount_to: Optional[int] = 1000):
    # Create filters dynamically based on parameters
    filters = [
        expense_model.Expense.comment.contains(search),
        expense_model.Expense.owner_id == current_user.id
    ]

    if amount_from is not None:
        filters.append(expense_model.Expense.amount >= amount_from)
    if amount_to is not None:
        filters.append(expense_model.Expense.amount <= amount_to)

    # Apply filters to the query
    expenses = (db.query(expense_model.Expense)
                .filter(*filters)
                .limit(limit)
                .offset(skip)
                .all())

    return expenses


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=expense_schema.Expense)
def create_expense(expense: expense_schema.ExpenseCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(user_repository.get_current_user)):
    try:
        new_expense = expense_model.Expense(owner_id=current_user.id, **expense.dict())

        db.add(new_expense)
        db.commit()
        db.refresh(new_expense)

        return new_expense

    except IntegrityError as e:
        # Check if the error is related to the foreign key constraint violation
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{id}", response_model=expense_schema.Expense)
def get_expense(id: int, db: Session = Depends(get_db), current_user: int = Depends(user_repository.get_current_user)):
    expense = db.query(expense_model.Expense).filter(expense_model.Expense.id == id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"expense with id: {id} was not found"
        )

    if expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return expense


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(id: int, db: Session = Depends(get_db),
                   current_user: int = Depends(user_repository.get_current_user)):
    expense_query = db.query(expense_model.Expense).filter(expense_model.Expense.id == id)

    expense = expense_query.first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"expense with id: {id} does not found"
        )

    if expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    expense_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=expense_schema.Expense)
def update_expense(id: int, updated_expense: expense_schema.ExpenseCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(user_repository.get_current_user)):
    expense_query = db.query(expense_model.Expense).filter(expense_model.Expense.id == id)

    expense = expense_query.first()

    if expense is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"expense with id: {id} does not found"
        )

    if expense.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    try:
        expense_query.update(updated_expense.dict(), synchronize_session=False)
        db.commit()

        return expense_query.first()

    except IntegrityError as e:
        # Check if the error is related to the foreign key constraint violation
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")



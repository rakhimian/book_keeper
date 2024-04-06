from ..models import budget as budget_model
from ..schemas import budget as budget_schema
from fastapi import status, Depends, APIRouter, HTTPException, Response
from ..repository.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.user.user_repository import UserRepository
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/budgets',
    tags=["Budgets"]
)

user_repository = UserRepository()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[budget_schema.Budget])
def get_budgets(db: Session = Depends(get_db),
                current_user: int = Depends(user_repository.get_current_user),
                limit: int = 10,
                skip: int = 0,
                amount_from: Optional[int] = 0,
                amount_to: Optional[int] = 1000):
    # Create filters dynamically based on parameters
    filters = [
        budget_model.Budget.owner_id == current_user.id
    ]

    if amount_from is not None:
        filters.append(budget_model.Budget.amount >= amount_from)
    if amount_to is not None:
        filters.append(budget_model.Budget.amount <= amount_to)

    # Apply filters to the query
    budgets = (db.query(budget_model.Budget)
               .filter(*filters)
               .limit(limit)
               .offset(skip)
               .all())

    return budgets


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=budget_schema.Budget)
def create_budget(budget: budget_schema.BudgetCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(user_repository.get_current_user)):
    try:
        new_budget = budget_model.Budget(owner_id=current_user.id, **budget.dict())

        db.add(new_budget)
        db.commit()
        db.refresh(new_budget)

        return new_budget

    except IntegrityError as e:
        # Check if the error is related to the foreign key constraint violation
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


@router.get("/{id}", response_model=budget_schema.Budget)
def get_budget(id: int, db: Session = Depends(get_db), current_user: int = Depends(user_repository.get_current_user)):
    budget = db.query(budget_model.Budget).filter(budget_model.Budget.id == id).first()

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"budget with id: {id} was not found"
        )

    if budget.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return budget


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget(id: int, db: Session = Depends(get_db),
                  current_user: int = Depends(user_repository.get_current_user)):
    budget_query = db.query(budget_model.Budget).filter(budget_model.Budget.id == id)

    budget = budget_query.first()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"budget with id: {id} does not found"
        )

    if budget.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    budget_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=budget_schema.Budget)
def update_budget(id: int, updated_budget: budget_schema.BudgetCreate, db: Session = Depends(get_db),
                  current_user: int = Depends(user_repository.get_current_user)):
    budget_query = db.query(budget_model.Budget).filter(budget_model.Budget.id == id)

    budget = budget_query.first()

    if budget is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"budget with id: {id} does not found"
        )

    if budget.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    try:
        budget_query.update(updated_budget.dict(), synchronize_session=False)
        db.commit()

        return budget_query.first()

    except IntegrityError as e:
        # Check if the error is related to the foreign key constraint violation
        if "foreign key constraint" in str(e).lower():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category does not exist")
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

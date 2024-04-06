from ..models import category as category_model
from ..schemas import category as category_schema
from fastapi import status, Depends, APIRouter, HTTPException, Response
from ..repository.database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository.user.user_repository import UserRepository

router = APIRouter(
    prefix='/categories',
    tags=["Categories"]
)

user_repository = UserRepository()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[category_schema.Category])
def get_categories(db: Session = Depends(get_db), current_user: int = Depends(user_repository.get_current_user),
                   limit: int = 10,
                   skip: int = 0, search: Optional[str] = ""):
    categories = (db.query(category_model.Category)
                  .filter(category_model.Category.name.contains(search))
                  .filter(category_model.Category.owner_id == current_user.id)
                  .limit(limit)
                  .offset(skip)
                  .all())

    return categories


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=category_schema.Category)
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db),
                current_user: int = Depends(user_repository.get_current_user)):
    new_category = category_model.Category(owner_id=current_user.id, **category.dict())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@router.get("/{id}", response_model=category_schema.Category)
def get_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(user_repository.get_current_user)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id: {id} was not found"
        )

    if category.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    return category


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db),
                    current_user: int = Depends(user_repository.get_current_user)):
    category_query = db.query(category_model.Category).filter(category_model.Category.id == id)

    category = category_query.first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id: {id} does not found"
        )

    if category.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    category_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=category_schema.Category)
def update_category(id: int, updated_category: category_schema.CategoryCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(user_repository.get_current_user)):
    category_query = db.query(category_model.Category).filter(category_model.Category.id == id)

    category = category_query.first()

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"category with id: {id} does not found"
        )

    if category.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    category_query.update(updated_category.dict(), synchronize_session=False)
    db.commit()

    return category_query.first()

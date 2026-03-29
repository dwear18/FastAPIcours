from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func


from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.schemas import ReviewResponse, ReviewCreate
from app.models.users import User as UserModel
from app.db_depends import get_async_db
from app.auth import get_current_buyer, get_current_user


router = APIRouter(
    prefix="/reviews", 
    tags=["reviews"]
)


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product.rating = avg_rating


@router.get("/", response_model=list[ReviewResponse])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """     
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return reviews.all()


@router.get("/products/{product_id}", response_model=list[ReviewResponse])
async def get_reviews_by_product(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает все активые отзывы конкретного товара.
    """
    product = await db.scalar(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found or inactive")
    reviews = await db.scalars(
        select(ReviewModel).where(ReviewModel.product_id == product_id, ReviewModel.is_active == True)
    )
    return reviews.all()


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, 
                        db: AsyncSession = Depends(get_async_db), 
                        current_user: UserModel = Depends(get_current_buyer)
                        ):
    """
    Создаёт новый отзыв, привязанный к текущему покупателю (только для 'buyer').
    """
    product = await db.scalar(
        select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True)
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Product not found or inactive")
    
    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    await update_product_rating(db, review.product_id)
    return db_review

@router.delete("/{review_id}")
async def delete_review(review_id: int,
                        db: AsyncSession = Depends(get_async_db),
                        current_user: UserModel = Depends(get_current_user)
                        ):
    """
    Выполняет мягкое удаление отзыва, если он принадлежит текущему покупателю.
    """
    review = await db.scalar(
        select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True)
    )
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )       
    review.is_active = False

    await db.commit()
    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}
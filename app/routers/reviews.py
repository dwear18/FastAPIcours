from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func


from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.schemas import ReviewResponse, ReviewCreate
from app.db_depends import get_async_db


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
    await db.commit()
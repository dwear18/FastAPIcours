from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.products import Product as ProductModel
from app.models.categories import Category as CategoryModel
from app.schemas import Product as ProductSchema, ProductCreate
from app.db_depends import get_db

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

async def check_product_id(product_id: int, db: Session = Depends(get_db)):
    product = db.scalars(
        select(ProductModel)
        .where(ProductModel.id == product_id)
        .where(ProductModel.is_active)
    ).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found or inactive"
        )
    return product

async def check_category_id(category_id: int, db: Session = Depends(get_db)):
    category = db.scalars(
        select(CategoryModel)
        .where(CategoryModel.id == category_id)
        .where(CategoryModel.is_active)
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive"
        )
    return category

async def check_category_from_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Вспомогательная функция для проверки категории из тела запроса."""
    category = db.scalars(
        select(CategoryModel)
        .where(CategoryModel.id == product.category_id)
        .where(CategoryModel.is_active)
    ).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive"
        )
    return category

@router.get("/", response_model=list[ProductSchema])
async def get_all_products(db: Session = Depends(get_db)):
    """Возвращает список всех товаров."""
    stmt = select(ProductModel).where(ProductModel.is_active)
    products = db.scalars(stmt).all()
    return products

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    _ = Depends(check_category_from_product)
    ):
    """Создает новый товар."""
    db_product = ProductModel(**product.model_dump(), is_active=True)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/category/{category_id}", response_model=list[ProductSchema])
async def get_products_by_category(
    category_id: int, 
    db: Session = Depends(get_db),
    category = Depends(check_category_id)
):
    """Возвращает список товаров в указанной категории по её ID."""
    products = db.scalars(
        select(ProductModel)
        .where(ProductModel.category_id == category_id)
        .where(ProductModel.is_active)
    ).all()
    return products

@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product = Depends(check_product_id),
    db: Session = Depends(get_db),
    ):
    """Возвращает один товар в указанной категории по её ID с проверкой активности категории."""
    category = db.scalars(
        select(CategoryModel)
        .where(CategoryModel.id == product.category_id)
        .where(CategoryModel.is_active)
    ).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category not found or inactive"
        )
    return product


@router.put("/{product_id}", response_model=ProductSchema, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    product: ProductCreate,
    db: Session = Depends(get_db),
    check_product = Depends(check_product_id),
    check_сategory = Depends(check_category_from_product)
    ):
    """Обновляет товар по его ID."""
    db.execute(
        update(ProductModel)
        .where(ProductModel.id == product_id)
        .values(**product.model_dump())
    )
    db.commit()

    # Получаем обновленный товар
    updated_product = db.scalars(
        select(ProductModel)
        .where(ProductModel.id == product_id)
        .where(ProductModel.is_active)
    ).first()

    db.refresh(updated_product)

    return updated_product

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    check_product = Depends(check_product_id)):
    """Удаляет товар по его ID."""
    db.execute(update(ProductModel).where(ProductModel.id == product_id).values(is_active=False))
    db.commit()

    return {"status": "success", "message": "Product marked as inactive"}
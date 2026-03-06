from fastapi import APIRouter

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)

@router.get("/")
async def get_all_categories():
    """
    Возвращает список всех категорий товаров.
    """
    return {"message": "Список всех категорий (заглушка)"}

@router.post("/")
async def create_category():
    """
    Создаем новую категорию.
    """
    return {"message": "Категория создана (заглушка)"}

@router.put("/{category_id}")
async def update_category(category_id: int):
    """
    Обнавляет категорию по ID.
    """
    return {"message": f"Категория с ID {category_id} обнавлена заглушка"}

@router.delete("/{category_id}")
async def delete_category(category_id: int):
    """
    Удалает категорию по её ID.
    """
    return {"message": f"Категория а ID {category_id} удалена (заглушка)"}

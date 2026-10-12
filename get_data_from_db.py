
from __future__ import annotations

from config import logger, settings as cfg

from db.create_connection import engine
from db.models import _TABLE_MODELS, TableName

from sqlalchemy import select
from sqlalchemy.orm import Session

from dataclasses import dataclass
from typing import Any


@dataclass
class Food:
    id: int
    name: str
    meal_type: str | None
    company: str | None
    kcal: int | None
    fats: float | None
    protein: float | None
    carbs: float | None
    fiber: float | None
    default_servings: float | None
    is_ingredient: bool = False
    ingredients: list[MealIngredient] = None
    
@dataclass
class MealIngredient:
    name: str
    quantity: float | None
    unit: str | None
    

def get_table_data(engine) -> dict[str, dict[str, list]]:
    data: dict[str, list] = {}
    with Session(engine) as session:
        for table_name, model in _TABLE_MODELS.items():
            result = session.scalars(select(model))
            data[table_name.value] = [row_to_dict(row) for row in result]
    return data

def row_to_dict(row) -> dict[str, Any]:
    row_data: dict[str, Any] = {}
    for column in row.__table__.columns:
        row_data[column.name] = getattr(row, column.name)
    return row_data

def add_ingredient_flag(row: dict[str, Any], table_name: str) -> dict[str, Any]:
    row["is_ingredient"] = table_name == TableName.INGREDIENTS.value
    return row

def transform_none_value(value: Any, none_char: str) -> Any:
    return none_char if value is None else value

def clean_and_merge_foods(
    tables: dict[str, dict[str, list]], 
    sort_by: str, 
    none_char: str | None
) -> list:
    foods = []
    for table_name, d in tables.items():
        for row in d:
            row = add_ingredient_flag(row, table_name)
            if none_char:
                row = {k: transform_none_value(v, none_char) for k, v in row.items()}
            foods.append(row)
    if sort_by in foods[0]:
        foods.sort(key=lambda x: x[sort_by])
    return foods
                
                






    





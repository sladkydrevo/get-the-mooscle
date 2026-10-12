from __future__ import annotations

import os
from dataclasses import dataclass
from enum import StrEnum, auto
from decimal import Decimal
from pathlib import Path

import csv

from sqlalchemy.orm import Session

from config import logger, settings as cfg

from db.models import Meal, Ingredient, TableName, CSVData
from db.create_connection import engine

_UNKNOWN_VALUES = frozenset({"", "-", "–"})
_MEAL_TYPES = frozenset(["breakfast", "main", "snack", "side", "drink", "other"])


def clean_cell(value: str) -> str:
    value = value.strip()
    if value.lower() in _UNKNOWN_VALUES:
        return ""
    return value
    
def to_int(value: str) -> int | None:
    return int(value) if value else None


def to_decimal(value: str) -> Decimal | None:
    return Decimal(value) if value else None


def row_to_meal(row: list[str]) -> Meal:
    return Meal(
        name=row[1],
        meal_type=row[2] or "other",
        company=row[3] or None,
        kcal=to_int(row[4]),
        fats=to_decimal(row[5]),
        protein=to_decimal(row[6]),
        carbs=to_decimal(row[7]),
        fiber=to_decimal(row[8]),
        default_servings=to_decimal(row[9]) or Decimal("1"),
    )
    
def row_to_ingredient(row: list[str]) -> Ingredient:
    return Ingredient(
        name=row[1],
        kcal=to_int(row[2]),
        fats=to_decimal(row[3]),
        protein=to_decimal(row[4]),
        carbs=to_decimal(row[5]),
        fiber=to_decimal(row[6]),
    )
    

def csv_to_items(file_path: Path | str) -> CSVData:
    try:
        name = Path(file_path).stem
        table_type = TableName.MEALS if name == "meals" else TableName.INGREDIENTS
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            result = []
            for row in reader:
                cleaned_row = list(map(clean_cell, row))
                if table_type == TableName.MEALS:
                    item = row_to_meal(cleaned_row)
                elif table_type == TableName.INGREDIENTS:
                    item = row_to_ingredient(cleaned_row)
                result.append(item)
        logger.info(f"Successfully read CSV file: {file_path}")
        return CSVData(name=name, table_type=table_type, data=result)
    except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            raise

def get_data(folder_path: Path | str) -> list[CSVData]:
    data: list[CSVData] = []
    for file_path in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_path)
        data.append(csv_to_items(file_path))
    return data


def ingest(data: CSVData) -> None:
    try:
        with Session(engine) as session:
            session.add_all(data.data) 
            session.commit()
    except Exception as e:
        logger.error(f"Error inserting items: {e}")
        

    

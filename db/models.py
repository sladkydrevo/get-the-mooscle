from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from enum import StrEnum, auto
from dataclasses import dataclass


class TableName(StrEnum):
    MEALS = auto()
    INGREDIENTS = auto()
    MEAL_INGREDIENTS = auto()
    DAILY_ENTRIES = auto()


@dataclass
class CSVData:
    name: str
    table_type: TableName
    data: list
    

class Base(DeclarativeBase):
    pass


class Ingredient(Base):
    __tablename__ = TableName.INGREDIENTS

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    kcal: Mapped[int | None]
    fats: Mapped[Decimal | None]
    protein: Mapped[Decimal | None]
    carbs: Mapped[Decimal | None]
    fiber: Mapped[Decimal | None]


class Meal(Base):
    __tablename__ = TableName.MEALS

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))

    meal_type: Mapped[str] = mapped_column(String(10), default="other")
    company: Mapped[str | None] = mapped_column(String(20))

    kcal: Mapped[int | None]
    fats: Mapped[Decimal | None]
    protein: Mapped[Decimal | None]
    carbs: Mapped[Decimal | None]
    fiber: Mapped[Decimal | None]

    default_servings: Mapped[Decimal] = mapped_column(default=1)

    ingredients: Mapped[list["MealIngredient"]] = relationship(back_populates="meal")


class MealIngredient(Base):
    __tablename__ = TableName.MEAL_INGREDIENTS

    id: Mapped[int] = mapped_column(primary_key=True)

    meal_id: Mapped[int] = mapped_column(ForeignKey("meals.id"))
    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredients.id"))

    ingredient_name: Mapped[str] = mapped_column(String(40))
    amount: Mapped[Decimal]
    unit: Mapped[str] = mapped_column(String(10))

    meal: Mapped[Meal] = relationship(back_populates="ingredients")
    ingredient: Mapped[Ingredient | None] = relationship()


class DailyEntry(Base):
    __tablename__ = TableName.DAILY_ENTRIES

    id: Mapped[int] = mapped_column(primary_key=True)

    meal_id: Mapped[int | None] = mapped_column(ForeignKey("meals.id"))
    ingredient_id: Mapped[int | None] = mapped_column(ForeignKey("ingredients.id"))

    name: Mapped[str] = mapped_column(String(40))

    date: Mapped[date]
    amount: Mapped[Decimal]
    unit: Mapped[str] = mapped_column(String(10))

    meal: Mapped[Meal | None] = relationship()
    ingredient: Mapped[Ingredient | None] = relationship()
    
    
_TABLE_MODELS = {
    TableName.MEALS: Meal,
    TableName.INGREDIENTS: Ingredient,
    TableName.MEAL_INGREDIENTS: MealIngredient,
    TableName.DAILY_ENTRIES: DailyEntry,
}
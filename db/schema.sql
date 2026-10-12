CREATE DATABASE IF NOT EXISTS foodies;
USE foodies;

CREATE TABLE IF NOT EXISTS meals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,

    meal_type ENUM(
        "breakfast",
        "main",
        "snack",
        "side",
        "drink",
        "other"
    ) NOT NULL DEFAULT "other",

    company VARCHAR(255),
    
    kcal SMALLINT UNSIGNED,
    fats DECIMAL(6,2),
    protein DECIMAL(6,2),
    carbs DECIMAL(6,2),
    fiber DECIMAL(6,2),

    default_servings DECIMAL(6,2) NOT NULL DEFAULT 1
);


CREATE TABLE IF NOT EXISTS ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,

    kcal SMALLINT UNSIGNED,
    fats DECIMAL(6,2),
    protein DECIMAL(6,2),
    carbs DECIMAL(6,2),
    fiber DECIMAL(6,2)
);


CREATE TABLE IF NOT EXISTS meal_ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,

    meal_id INT NOT NULL,
    ingredient_id INT NULL,

    ingredient_name VARCHAR(255) NOT NULL,

    amount DECIMAL(8,2) NOT NULL,
    unit VARCHAR(30) NOT NULL,

    CONSTRAINT fk_meal_ingredients_meal
        FOREIGN KEY (meal_id)
        REFERENCES meals(id),

    CONSTRAINT fk_meal_ingredients_ingredient
        FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id)
);


CREATE TABLE IF NOT EXISTS daily_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,

    date DATE NOT NULL,

    ingredient_id INT NULL,
    meal_id INT NULL,

    amount DECIMAL(6,3) NOT NULL DEFAULT 1,
    unit VARCHAR(30) NOT NULL,

    CONSTRAINT fk_daily_entries_ingredient
        FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id),

    CONSTRAINT fk_daily_entries_meal
        FOREIGN KEY (meal_id)
        REFERENCES meals(id),

    CONSTRAINT chk_daily_entry_source
        CHECK (
            (ingredient_id IS NOT NULL AND meal_id IS NULL)
            OR
            (ingredient_id IS NULL AND meal_id IS NOT NULL)
        )
);


CREATE TABLE IF NOT EXISTS daily_entry_ingredients (
    id INT AUTO_INCREMENT PRIMARY KEY,

    daily_entry_id INT NOT NULL,
    ingredient_id INT NULL,

    ingredient_name VARCHAR(255) NOT NULL,

    amount DECIMAL(8,2) NOT NULL,
    unit VARCHAR(30) NOT NULL,

    CONSTRAINT fk_daily_entry_ingredients_entry
        FOREIGN KEY (daily_entry_id)
        REFERENCES daily_entries(id),

    CONSTRAINT fk_daily_entry_ingredients_ingredient
        FOREIGN KEY (ingredient_id)
        REFERENCES ingredients(id)
);
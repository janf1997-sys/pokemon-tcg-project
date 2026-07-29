DROP TABLE IF EXISTS my_collection CASCADE;
DROP TABLE IF EXISTS catalog CASCADE;
DROP TABLE IF EXISTS card_catalog CASCADE;
DROP TABLE IF EXISTS tcg_sets CASCADE;
DROP TABLE IF EXISTS sets CASCADE;
DROP TABLE IF EXISTS pokedex CASCADE;




CREATE TABLE pokedex (
    pokedex_id INT PRIMARY KEY,
    generation INT,
    pokemon_name VARCHAR(50) NOT NULL
);

CREATE TABLE tcg_sets (
    set_id VARCHAR(20) PRIMARY KEY,
    set_name VARCHAR(100),
    base_set INT,
    master_set INT
);

CREATE TABLE card_catalog (
    catalog_id SERIAL PRIMARY KEY,
    set_id VARCHAR(20) REFERENCES tcg_sets(set_id),
    pokedex_id INT REFERENCES pokedex(pokedex_id),
    card_name VARCHAR(100) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    image_url VARCHAR(255)
);
CREATE TABLE my_collection (
    collection_id SERIAL PRIMARY KEY,
    catalog_id INT REFERENCES card_catalog(catalog_id),
    amount INT DEFAULT 1,
    card_language VARCHAR(10) 
);
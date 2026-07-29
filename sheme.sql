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
    set_id VARCHAR(20),
    pokedex_id INT,
    card_name VARCHAR(100) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    image_url VARCHAR(255),
    FOREIGN KEY (set_id) REFERENCES tcg_sets(set_id),
    FOREIGN KEY (pokedex_id) REFERENCES pokedex(pokedex_id)
);
CREATE TABLE my_collection (
    collection_id SERIAL PRIMARY KEY,
    catalog_id INT,
    amount INT DEFAULT 1,
    card_language VARCHAR(10),
    FOREIGN KEY (catalog_id) REFERENCES card_catalog(catalog_id) 
);
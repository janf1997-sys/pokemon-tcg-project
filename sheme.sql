CREATE TABLE pokedex (
    pokedex_id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE sets (
    set_id VARCHAR(20) PRIMARY KEY,
    set_name VARCHAR(100),
    base_set INT,
    master_set INT
);

CREATE TABLE catalog (
    catalog_id SERIAL PRIMARY KEY,
    set_id VARCHAR(20) REFERENCES sets(set_id),
    pokedex_id INT REFERENCES pokedex(pokedex_id),
    card_name VARCHAR(100) NOT NULL,
    card_number VARCHAR(20) NOT NULL,
    image_url VARCHAR(255)
);
CREATE TABLE my_collection (
    collection_id SERIAL PRIMARY KEY,
    catalog_id INT REFERENCES catalog(catalog_id),
    amount INT DEFAULT 1,
    language VARCHAR(10) 
);
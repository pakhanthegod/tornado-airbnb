--liquibase formatted sql

--changeset nvoxland:1
CREATE TYPE user_role AS ENUM ('user', 'staff');

CREATE TABLE users (
        id SERIAL NOT NULL, 
        first_name VARCHAR NOT NULL, 
        last_name VARCHAR NOT NULL, 
        email VARCHAR NOT NULL, 
        password VARCHAR NOT NULL, 
        avatar VARCHAR, 
        date DATE, 
        role user_role NOT NULL, 
        PRIMARY KEY (id)
);

CREATE TABLE houses (
        id SERIAL NOT NULL, 
        user_id INTEGER, 
        description TEXT, 
        address TEXT, 
        max_person_number INTEGER, 
        price NUMERIC(10, 2), 
        is_reviewed BOOLEAN, 
        latitude FLOAT, 
        longitude FLOAT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES users (id)
);

CREATE TABLE orders (
        id SERIAL NOT NULL, 
        house_id INTEGER NOT NULL, 
        user_id INTEGER NOT NULL, 
        date_from TIMESTAMP WITH TIME ZONE NOT NULL, 
        date_to TIMESTAMP WITH TIME ZONE NOT NULL, 
        rating INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(house_id) REFERENCES houses (id), 
        FOREIGN KEY(user_id) REFERENCES users (id)
);
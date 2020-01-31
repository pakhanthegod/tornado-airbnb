--liquibase formatted sql

--changeset nvoxland:1
CREATE TYPE user_role AS ENUM('customer', 'staff');

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  first_name varchar(128) NOT NULL,
  last_name varchar(128) NOT NULL,
  email varchar(255) NOT NULL,
  password bytea NOT NULL,
  avatar varchar(255) NULL,
  birthdate date NOT NULL,
  role user_role DEFAULT 'customer' NOT NULL
);

CREATE TABLE IF NOT EXISTS houses (
  id SERIAL PRIMARY KEY,
  description text NOT NULL,
  address text NOT NULL,
  max_person_number integer NOT NULL,
  price numeric(10,2) NOT NULL,
  is_reviewed boolean DEFAULT FALSE NOT NULL,
  reviewed timestamptz NULL,
  latitude float,
  longitude float,
  rating integer DEFAULT 0 NOT NULL,

  user_id integer REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
  id SERIAL PRIMARY KEY,
  book_from timestamptz NOT NULL,
  book_to timestamptz NOT NULL,
  rating integer,

  house_id integer REFERENCES houses(id) ON DELETE CASCADE,
  user_id integer REFERENCES users(id) ON DELETE CASCADE
);

CREATE FUNCTION reviewed_update() RETURNS trigger AS $body$
  BEGIN
    IF NEW.is_reviewed = TRUE THEN
      INSERT INTO houses (reviewed) VALUES (CURRENT_TIMESTAMP);
    END IF;

    RETURN NEW;
  END;
$body$ LANGUAGE plpgsql;

CREATE TRIGGER reviewed_time_update
  AFTER UPDATE ON houses
  FOR EACH ROW
  EXECUTE PROCEDURE reviewed_update();

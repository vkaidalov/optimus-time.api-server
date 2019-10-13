CREATE DATABASE optimus_time;
CREATE USER optimus_time_admin WITH PASSWORD 'optimus_time';
ALTER ROLE optimus_time_admin SET client_encoding TO 'utf8';
ALTER ROLE optimus_time_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE optimus_time_admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE optimus_time TO optimus_time_admin;
ALTER USER optimus_time_admin CREATEDB;
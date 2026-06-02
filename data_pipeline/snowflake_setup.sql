-- =============================================================================
-- SNOWFLAKE SETUP  (run ONCE, in a Snowflake worksheet, as ACCOUNTADMIN)
-- -----------------------------------------------------------------------------
-- Creates the warehouse / database / schema / role this dbt project expects.
-- These names match ~/.dbt/profiles.yml. After this runs, dbt can connect,
-- load the seed CSVs, and build the models.
-- =============================================================================

use role accountadmin;

-- A "warehouse" is the compute that runs queries. XSMALL is cheapest;
-- auto_suspend stops it after 60s idle so you don't burn trial credits.
create warehouse if not exists dbt_wh
    with warehouse_size = 'xsmall'
    auto_suspend = 60
    auto_resume = true;

create database if not exists dbt_db;
create role if not exists dbt_role;

grant usage on warehouse dbt_wh to role dbt_role;
grant all on database dbt_db to role dbt_role;

-- Give YOUR user the role. Run `select current_user();` to find your username,
-- then replace <YOUR_USERNAME> below.
grant role dbt_role to user <YOUR_USERNAME>;

-- Create the schema dbt writes into (seeds + models land here).
use role dbt_role;
use warehouse dbt_wh;
use database dbt_db;
create schema if not exists dbt_db.dbt_schema;

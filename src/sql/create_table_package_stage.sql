-- create the table if not exists
create table if not exists package_stage (
     package_id text
    ,name text
    ,price_currency text
    ,price_initial text
    ,price_final text
    ,price_discount_percent text
    ,price_individual text
    ,platforms_windows text
    ,platforms_mac text
    ,platforms_linux text
    ,release_date_coming_soon text
    ,release_date_date text
    ,load_ts integer
    ,_hash text
)
;

-- create an index on the tables primary keys
create unique index if not exists ix_package_stage_pk on package_stage (package_id, load_ts);

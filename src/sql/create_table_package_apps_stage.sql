-- create the table if not exists
create table if not exists package_apps_stage (
     package_id integer
    ,app_id integer
    ,name text
    ,load_ts integer
    ,_hash text
)
;

-- create an index on the tables primary keys
create unique index if not exists ix_package_apps_stage_pk on package_apps_stage (package_id, app_id, load_ts);
create index if not exists ix_package_apps_stage_app_id on package_apps_stage (app_id);

insert into package_stage (
     package_id
    ,name 
    ,price_currency 
    ,price_initial 
    ,price_final 
    ,price_discount_percent 
    ,price_individual
    ,platforms_windows
    ,platforms_mac
    ,platforms_linux
    ,release_date_coming_soon
    ,release_date_date 
    ,load_ts
    ,_hash
)
with stage as (
	select
         package_id
        ,_hash
		,row_number() over (partition by package_id order by load_ts desc) as rwnr
	from package_stage
)
select
     r.package_id 
    ,r.name 
    ,r.price_currency 
    ,r.price_initial 
    ,r.price_final 
    ,r.price_discount_percent 
    ,r.price_individual
    ,r.platforms_windows
    ,r.platforms_mac
    ,r.platforms_linux
    ,r.release_date_coming_soon
    ,r.release_date_date 
    ,r.load_ts 
    ,r._hash
from package_raw r
left join stage s
	on r.package_id = s.package_id
	and r._hash = s._hash
	and s.rwnr = 1
where s.package_id is null
;
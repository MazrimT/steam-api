insert into package_apps_stage (
     package_id
    ,app_id
    ,name
    ,load_ts
    ,_hash
)
with stage as (
	select
		 package_id
		,app_id
		,_hash
		,row_number() over (partition by package_id, app_id order by load_ts desc) as rwnr
	from package_apps_stage
)
select
     r.package_id
    ,r.app_id
    ,r.name
    ,r.load_ts
    ,r._hash
from package_apps_raw r
left join stage s
	on r.package_id = s.package_id
	and r.app_id = s.app_id
	and r._hash = s._hash
	and s.rwnr = 1
where s.package_id is null
;

# Download package information from Steam api

Application gathers "package" information from steam based on predetermined packageids and stores in sqlite database.

* Reads package_ids from src/data/input_packages.json  
* downloads data from API for these package_ids
* transform data to flat structure for package and package_apps
* saves data to respective _raw tables in the database (using _suffix but could just as well have been different schemas)
* runs query to create _stage table if not exists
* inserts from _raw to _stage only rows that have been modified based on a _hash
* exports full tables from _stage and saves as src/data/[table].csv
  
## setup
  
create a new virtual environment  
``` python -m venv venv ```  
  
activate virtual environment  
win: ``` venv\Scripts\actvate ```  
*nix: ``` source venv\bin\activate ```
  
update pip  
``` python -m pip install --upgrade pip ```  
  
install requirements  
``` python -m pip install -r requirements.txt ```  
  
put package ids in src/data/input_packages.json file  
  
## run
  
run application  
``` python src/app.py ```  

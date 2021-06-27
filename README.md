# Parser-by-Python
python parther program

This is parsing program to parse xml and csv files to json files and save to mongodb ..

# Installation
1 - install pip and xmltodict ($ pip install xmltodict)
2 - install mongoDB (https://docs.mongodb.com/manual/tutorial/) Ubuntu: (https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)
3 - install pymongo library (allows interaction with the MongoDB database through Python)
  ($ pip install pymongo)
4 - Create DB  : Trufla >> start mongo and open shell then : 
  a - use trufla
  b - create user admin for trufla db :
    db.createUser({	user: "trufla_admin", pwd: "P@ssw0rd",roles:[{role: "userAdmin" , db:"trufla"}]})
  c - create two collections (xml , csv)

# Run Script 
Open terminal
case 1 : (xml)
$ python3 parser.py -format xml -customers_file 'path-to-customers-file.xml'
case 2 : (csv)
$ python3 parser.py -format csv -customers_file 'path-to-customers-file.csv' -vehicles_file 'path-to-vehicles_file.csv'

# Finally
You will recieve json output file in same directory of input file ..
and then check trufla db collections (xml and csv) to make sure files are kept in right way .

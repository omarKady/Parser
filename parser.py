import argparse, xmltodict, os, time, json, csv
from pymongo import MongoClient 

class BaseParser:
    def __init__(self, customers_file, vehicles_file = None):
        self.customers_file = customers_file
        self.vehicles_file = vehicles_file

    def parse_to_json(self):
        raise NotImplementedError

    def output_file_naming(self, customers_file):
        file_name = os.path.basename(self.customers_file)
        file_name_without_extension = os.path.splitext(file_name)[0]
        output_file_with_extension = file_name_without_extension + '.json'
        ts = time.time()
        final_output_file_name = str(ts) + '_' + output_file_with_extension
        return final_output_file_name


    def output_file_path(self, customers_file):
        dirnam = os.path.dirname(self.customers_file)
        file_name = self.output_file_naming(customers_file)
        json_file_path = dirnam + '/' + file_name
        return json_file_path

    def send_json_to_mongodb(self, converted_json, colloction_type):
        myclient = MongoClient("mongodb://localhost:27017/")
        db = myclient["trufla"]
        Collection = db[colloction_type]
        with open(converted_json) as file:
            file_data = json.load(file)
            
        if isinstance(file_data, list):
            Collection.insert_many(file_data)  
        else:
            Collection.insert_one(file_data)
        

class XMLParser(BaseParser):
    def __init__(self, customers_file, vehicles_file = None):
        super().__init__(customers_file, vehicles_file)
        self.parse_to_json(customers_file)

    # TODO : read input file (Customers) : transform xml to dict
    def read_input_file(self, customers_file):
        xml_file = open(self.customers_file, "r")
        my_obj = xmltodict.parse(xml_file.read())
        py_dict = json.dumps(my_obj, indent=4)
        return py_dict

    # TODO : save : transform dict to json and write
    def parse_to_json(self, customers_file):
        file_path = self.output_file_path(customers_file)
        python_dict = self.read_input_file(customers_file)
        with open(file_path, "w") as my_file:
            my_file.write(python_dict)
        self.send_json_to_mongodb(file_path, 'xml')

class CSVParser(BaseParser):
    def __init__(self, customers_file, vehicles_file = None):
        super().__init__(customers_file, vehicles_file)
        self.parse_to_json(customers_file, vehicles_file)

    # TODO : read input file (Customers) : transform csv to dict
    def read_input_file(self, customers_file, vehicles_file):
        customers_list = []
        with open(customers_file, "r") as csv_file:
            c_reader = csv.DictReader(csv_file)
            for row in c_reader:
                customers_list.append(dict(row))

        vehicles_list = []
        with open(vehicles_file, "r") as csv_file:
            v_reader = csv.DictReader(csv_file)
            for row in v_reader:
                vehicles_list.append(dict(row))

        return customers_list, vehicles_list

    # merge two dict in one that has all customer data plus vehicles and transform in one dict
    def merge_customer_dict_with_vehicles(self, customers, vehicles):
        for customer in customers:
            customer_id = customer["id"]
            customer_vehicles = []
            for vehicle in vehicles:
                if vehicle["owner_id"] == customer_id:
                    customer_vehicles.append(vehicle)
            customer.update({"vehicle": customer_vehicles})
        return customers

    

    # TODO : save : transform dict to json and write
    def parse_to_json(self, customers_file, vehicles_file):
        file_path = self.output_file_path(customers_file)
        customers, vehicles = self.read_input_file(customers_file, vehicles_file)
        final_customers_with_vehicles = self.merge_customer_dict_with_vehicles(customers, vehicles)
        converted_json = json.dumps(final_customers_with_vehicles, indent=4)
        with open(file_path, "w") as my_file:
            my_file.write(converted_json)
        self.send_json_to_mongodb(file_path, 'csv')


if __name__ == "__main__":
    # TODO: parsing args
    parse = argparse.ArgumentParser()
    parse.add_argument("-format")
    parse.add_argument("-customers_file")
    parse.add_argument("-vehicles_file")
    args = parse.parse_args()
    format = args.format.lower()
    customers_file = args.customers_file
    vehicles_file = args.vehicles_file

    if format == 'xml':
        xml_parser = XMLParser(customers_file)
    elif format == 'csv':
        csv_parser = CSVParser(customers_file, vehicles_file)
    else:
        print("Not Supported ... This program support only xml and csv")

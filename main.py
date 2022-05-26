from jmespath import search
from licensing.methods import Customer, Key
import os
import requests
import csv
from readenv import customer_operations_token, key_operations_token



def getCustomers(search_data) :
    
    search_key = ''
    if 'email' in search_data :
        search_key = 'email'
    if 'name' in search_data :
        search_key = 'name'
    if 'company' in search_data :
        search_key = 'company'
    
    print(f"search_data {search_data} search_key {search_key} search_data[search_key] {search_data[search_key]}")
    
    PARAMS = {'search' : search_data[search_key], 'token' : customer_operations_token}
    URL = 'https://api.cryptolens.io/api/customer/GetCustomers'
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    if 'customers' not in json_res :
        return []
    customers = json_res['customers']
    
    
    # If customer is searched by email
    if 'email' in search_data :
        custs = []
        for cust in customers :
            if cust['email'] == search_data[search_key]:
                custs.append(cust)
        return custs
    
    
    # If customer is searched by name
    if 'name' in search_data :
        custs = []
        for cust in customers :
            if cust['name'] == search_data[search_key]:
                custs.append(cust)
        return custs
    
    
    return customers

def createCustomers(csv_file, product_id) :
    customers = []
    with open(csv_file) as file:
        csvreader = csv.DictReader(file)
        for cust in csvreader:
            customers.append(cust)


    for cust in customers:
        createCustomerResult = createCustomer(
            {
                "name" : cust['name'], 
                "company" : cust['company'], 
                "email" : cust['email']
            }
        )
        create_res = createCustomerResult[1]
        if create_res == False:
            print(f"Cannot create customer with: "
                  "name {cust['name']} "
                  "email {cust['email']} "
                  "company {cust['company']} ")
            continue
        
        customer_id = createCustomerResult[0]['customerId']
        create_key_res = Key.create_key(key_operations_token, 
                                        product_id, 
                                        period=cust['period'], 
                                        f1=bool(int(cust['f1'])), 
                                        f2=bool(int(cust['f2'])), 
                                        f3=bool(int(cust['f3'])), 
                                        f4=bool(int(cust['f4'])),
                                        f5=bool(int(cust['f5'])),
                                        f6=bool(int(cust['f6'])),
                                        f7=bool(int(cust['f7'])),
                                        f8=bool(int(cust['f8'])),
                                        customer_id=customer_id, 
                                        max_no_of_machines=0)
        
        # print(res_customer[0], create_key_res)
        print(f"f1 f2 f3 {cust['f1']} {cust['f2']} {cust['f3']}")
        
        cust_first_element = createCustomerResult[0]
        customer_secret = cust_first_element['secret']
        cust_id = cust_first_element['customerId']
        
        
        key_first_element = create_key_res[0]#
        serial = key_first_element['key']#  ok
        print(f'customer created with: id {cust_id} secret {customer_secret} attached_serial: {serial}')
        a = 0
























def createCustomer(customerData):
    
    # Check if user exists with provided email
    existing_customers = getCustomers({'email' : customerData["email"]})
    if len(existing_customers) != 0:
        print(f"User with mail {customerData['email']} already exists")
        return False

    # Check if user exists with provided user
    existing_customers = getCustomers({'name' : customerData["name"]})
    if len(existing_customers) != 0:
        print(f"User with name {customerData['name']} already exists")
        return False
    
    res_customer = Customer.add_customer(customer_operations_token, 
                      name = customerData["name"], 
                      email = customerData["email"], 
                      company_name = customerData["company"],
                      enable_customer_association = True)
    print(f"res_customer {res_customer}")
    data = res_customer[0]
    if data:
        return ({"customerId" : data['customerId'],  "secret" : data['secret']}, True)
    else:
        return ({}, False)


def deleteCustomer(email):
    
    # Get Customers with provided mail
    customers = getCustomers({'email' : email})
    if len(customers) != 1:
        print(f"User with email {email} does not exist")
        return False
    
    customer = customers[0]
    customerId = customer["id"]
    
    PARAMS = {'customerId' : customerId, 'token' : customer_operations_token}
    URL = 'https://api.cryptolens.io/api/customer/RemoveCustomer'
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    print(f"json_res is {json_res}")
    a = 0
    
#Create Customer
"""
result = createCustomer({"name" : 'name', 
                     "company" : 'company', 
                     "email" : 'alekogureshidze@gmail.com',
                     "period" : 30,	
                     "f1" :  False,	
                     "f2" :  False,	
                     "f3" :  False,	
                     "f4" :  False,	
                     "f5" :  False,	
                     "f6" :  False,	
                     "f7" :  False,	
                     "f8" :  False
                     })
"""


def revokeKey(productId, key):
    PARAMS = {'productId' : productId, 
              'key' : key, 
              'customerId' : 0,  
              'token' : key_operations_token}
    URL = "https://api.cryptolens.io/api/key/ChangeCustomer"
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()

    res = Key.block_key(key_operations_token, productId, key)
    a = 0
    

def createLicense(userEmail, license, product_id):
    customers = getCustomers({"email": userEmail})
    if len(customers) != 1:
        print(f"User with email {userEmail} does not exist")
        return False
    customer_id = customers[0]['customerId']
    
    create_key_res = Key.create_key(key_operations_token, 
                                    product_id, 
                                    period=license['period'], 
                                    f1=bool(int(license['f1'])), 
                                    f2=bool(int(license['f2'])), 
                                    f3=bool(int(license['f3'])), 
                                    f4=bool(int(license['f4'])),
                                    f5=bool(int(license['f5'])),
                                    f6=bool(int(license['f6'])),
                                    f7=bool(int(license['f7'])),
                                    f8=bool(int(license['f8'])),
                                    customer_id=customer_id, 
                                    max_no_of_machines=0)


revokeKey(15301, 'GJEMJ-HXAZD-KXXRO-ZYKRW')


# Delete Customer  
# deleteCustomer('name@gmail.com')  
    
    
# Create Customers
# createCustomers('customers.csv', 15301)

# print(f"result is {result}")


# customers = getCustomers({"email": "alekogureshidze@gmail.com"})
# print(f"customers is {customers}")


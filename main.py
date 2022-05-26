from licensing.methods import Customer, Key
import requests
import csv
from readenv import customer_operations_token, key_operations_token, product_id, max_no_of_machines
from flask import Flask, request
app = Flask(__name__)


features_map = {
    "f1" : "feature1",
    "f2" : "feature2",
    "f3" : "feature3",
    "f4" : "feature4",
    "f5" : "feature5",
    "f6" : "feature6",
    "f7" : "feature7",
    "f8" : "feature8"
}

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"



@app.route('/getCustomers', methods = ['GET'])
def getCustomers():
    if request.method == 'GET':
        res = _getCustomers()
        return {"customers" : res}

        
@app.route('/getCustomer', methods = ['GET'])
def getCustomer():
    if request.method == 'GET':
        email = request.args.get("email")
        res = _getCustomer(email)
        return {"customers" : res}

@app.route('/createCustomer', methods = ['GET'])
def createCustomer():
    if request.method == 'GET':
        customerData = {}
        customerData["name"] = request.args.get("name") 
        customerData["email"] = request.args.get("email")
        customerData["company"] = request.args.get("company")
        customerData["productId"] = request.args.get("productId")
        customerData["period"] = request.args.get("period")
        customerData["f1"] = request.args.get("f1")
        customerData["f2"] = request.args.get("f2")
        customerData["f3"] = request.args.get("f3")
        customerData["f4"] = request.args.get("f4")
        customerData["f5"] = request.args.get("f5")
        customerData["f6"] = request.args.get("f6")
        customerData["f7"] = request.args.get("f7")
        customerData["f8"] = request.args.get("f8")
        result = _createCustomer(customerData)
    return result

@app.route('/deleteUser', methods = ['GET'])
def deleteCustomer():
    if request.method == 'GET':
        res = _deleteCustomer(request.args.get("email"))
        return res

@app.route('/revokeKey', methods = ['GET'])
def revokeKey():
    if request.method == 'GET': 
        productId = request.args.get("productId")
        key = request.args.get("key")
        res = _revokeKey(productId, key)
        return res

@app.route('/createLicense', methods = ['GET'])
def createLicense():
    if request.method == 'GET': 
        res = _createLicense(request.args.get("email"), request.args)
        return res

def _getCustomerLicenses(customerId):
    PARAMS = {'customerId' : customerId, 
              'token' : customer_operations_token}
    URL = "https://api.cryptolens.io/api/customer/GetCustomerLicenses"
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    if json_res["result"] == 0:
        return (True, json_res["licenseKeys"])
    else :
        return (False, [])

def _getCustomers():
    PARAMS = {'token' : customer_operations_token}
    URL = 'https://api.cryptolens.io/api/customer/GetCustomers'
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    if 'customers' not in json_res :
        return {"result": True, "customers" : []}
    customers = json_res['customers']
    for cust in customers:
        res = _getCustomerLicenses(cust["id"])
        if(res[0] == True) :
            licenses = res[1]
            if len(licenses) == 1 :
                license = licenses[0]
                cust["period"],cust["f1"],cust["f2"],cust["f3"],cust["f4"],cust["f5"],cust["f6"],cust["f7"],cust["f8"] = license["period"],license["f1"],license["f2"],license["f3"],license["f4"],license["f5"],license["f6"],license["f7"],license["f8"]
    return {"result": True, "customers" : [customers]}


def _getCustomer(email) :
    PARAMS = {'search' : email, 'token' : customer_operations_token}
    URL = 'https://api.cryptolens.io/api/customer/GetCustomers'
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    if 'customers' not in json_res :
        return []
    customers = json_res['customers']
    
    
    # If customer is searched by email
    custs = []
    for cust in customers :
        if cust['email'] == email:
            res = _getCustomerLicenses(cust["id"])
            if(res[0] == True) :
                licenses = res[1]
                if len(licenses) == 1 :
                    license = licenses[0]
                    cust["period"],cust["f1"],cust["f2"],cust["f3"],cust["f4"],cust["f5"],cust["f6"],cust["f7"],cust["f8"] = license["period"],license["f1"],license["f2"],license["f3"],license["f4"],license["f5"],license["f6"],license["f7"],license["f8"]
            custs.append(cust)
    return custs


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
                                        max_no_of_machines=max_no_of_machines)
        
        # print(res_customer[0], create_key_res)
        print(f"f1 f2 f3 {cust['f1']} {cust['f2']} {cust['f3']}")
        
        cust_first_element = createCustomerResult[0]
        customer_secret = cust_first_element['secret']
        cust_id = cust_first_element['customerId']
        
        
        key_first_element = create_key_res[0]#
        serial = key_first_element['key']#  ok
        print(f'customer created with: id {cust_id} secret {customer_secret} attached_serial: {serial}')
        a = 0


def _createCustomer(customerData):
    
    # Check if user exists with provided email
    existing_customers = _getCustomer(customerData["email"])
    if len(existing_customers) != 0:
        return {"result" : False, "reason" : f"User with mail {customerData['email']} already exists"}

    res_customer = Customer.add_customer(customer_operations_token, 
                      name = customerData["name"], 
                      email = customerData["email"], 
                      company_name = customerData["company"],
                      enable_customer_association = True)
    data = res_customer[0]
    if data:
        create_key_res = Key.create_key(key_operations_token, 
                                        customerData["productId"], 
                                        period=customerData['period'], 
                                        f1=bool(int(customerData['f1'])), 
                                        f2=bool(int(customerData['f2'])), 
                                        f3=bool(int(customerData['f3'])), 
                                        f4=bool(int(customerData['f4'])),
                                        f5=bool(int(customerData['f5'])),
                                        f6=bool(int(customerData['f6'])),
                                        f7=bool(int(customerData['f7'])),
                                        f8=bool(int(customerData['f8'])),
                                        customer_id=data['customerId'], 
                                        max_no_of_machines=max_no_of_machines)
        key_first_element = create_key_res[0]#
        serial = key_first_element['key']#  ok
        return ({"customerId" : data['customerId'],  "secret" : data['secret'], 'serial' : serial}, True)
    
    else:
        return ({"result" : False, "reason" : ""})

    
def _deleteCustomer(email):
    
    # Get Customers with provided mail
    customers = _getCustomer(email)
    if len(customers) != 1:
        return {"result" : False, "reason" : f"User with email {email} does not exist"}
    
    customer = customers[0]
    customerId = customer["id"]
    
    
    # Get licenses associated to customer
    res = _getCustomerLicenses(customerId)
    if(res[0] == True) :
        licenseKeys = res[1]
        if (len(licenseKeys) == 1) :
            licenseKey = licenseKeys[0]
            _revokeKey(licenseKey["productId"], licenseKey['key'])
    
    # Finaly delete customer
    PARAMS = {'customerId' : customerId, 'token' : customer_operations_token}
    URL = 'https://api.cryptolens.io/api/customer/RemoveCustomer'
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()
    print(f"json_res is {json_res}")
    return json_res
      
        
def _revokeKey(productId, key):
    PARAMS = {'productId' : productId, 
              'key' : key, 
              'customerId' : 0,  
              'token' : key_operations_token}
    URL = "https://api.cryptolens.io/api/key/ChangeCustomer"
    r = requests.get(url = URL, params = PARAMS)
    json_res = r.json()

    res = Key.block_key(key_operations_token, productId, key)
    return {"result" : res[0]}
    
def _revokeLicense(email) :
    #Get user which corresponds to email
    res = _getCustomer(email)
    if len(res) != 1:
        return {False, "Cannot find corresponding user"}
    
    customer = res[0]
    customerId = customer['id']
    
    res = _getCustomerLicenses(customerId)
    if(res[0] == True) :
        licenseKeys = res[1]
        if (len(licenseKeys) == 1) :
            licenseKey = licenseKeys[0]
            res = _revokeKey(licenseKey["productId"], licenseKey['key'])
    
    return res

def _createLicense(userEmail, license):
    customers = _getCustomer(userEmail)
    if len(customers) != 1:
        print(f"User with email {userEmail} does not exist")
        return {"result" : False, "reason" : "There are more than 1 users associated with this email address"}
    
    customer_id = customers[0]['id']
    
    res = _getCustomerLicenses(customer_id)
    licenseKeys = res[1]
    if (len(licenseKeys) != 0) :
        return {"result" : False, "reason" : "User Already has Licens(e)s"}
    else :
        period=license.get('period')
        create_key_res = Key.create_key(key_operations_token, 
                                    product_id, 
                                    period=license.get('period'),
                                    f1=bool(int(license.get('f1'))),
                                    f2=bool(int(license.get('f2'))),
                                    f3=bool(int(license.get('f3'))),
                                    f4=bool(int(license.get('f4'))),
                                    f5=bool(int(license.get('f5'))),
                                    f6=bool(int(license.get('f6'))),
                                    f7=bool(int(license.get('f7'))),
                                    f8=bool(int(license.get('f8'))),
                                    customer_id=customer_id, 
                                    max_no_of_machines=max_no_of_machines)
        key_first_element = create_key_res[0]#
        serial = key_first_element['key']
        return {"result" : True, "data" : {"email" : userEmail, 'serial' : serial}}

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
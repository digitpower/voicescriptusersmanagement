import csv
import sys
from licensing.methods import Customer, Key, Helpers
import os
import requests

csv_file = sys.argv[1]

product_id = sys.argv[2]

customers = []
with open(csv_file) as file:
    csvreader = csv.DictReader(file)
    for cust in csvreader:
        customers.append(cust)



# get AUTH_TOKEN from environment
if 'AUTH_TOKEN' not in os.environ:
    print("No AUTH_TOKEN variable present in environment")
    exit(0)
# this token must have addcustomer permission
auth_token = os.environ['AUTH_TOKEN']






# get ADD_CUSTOMER_TOKEN from environment
if 'ADD_CUSTOMER_TOKEN' not in os.environ:
    print("No ADD_CUSTOMER_TOKEN variable present in environment")
    exit(0)
# this token must have addcustomer permission
add_customer_token = os.environ['ADD_CUSTOMER_TOKEN']





# get CREATE_KEY_TOKEN from environment
if 'CREATE_KEY_TOKEN' not in os.environ:
    print("No CREATE_KEY_TOKEN variable present in environment")
    exit(0)
# this token must have addcustomer permission
create_key_token = os.environ['CREATE_KEY_TOKEN']



# get CHANGE_CUSTOMER_TOKEN from environment
if 'CHANGE_CUSTOMER_TOKEN' not in os.environ:
    print("No CHANGE_CUSTOMER_TOKEN variable present in environment")
    exit(0)
# this token must have addcustomer permission
change_customer_token = os.environ['CHANGE_CUSTOMER_TOKEN']




# get ACTIVATE_KEY_TOKEN from environment
if 'ACTIVATE_KEY_TOKEN' not in os.environ:
    print("No ACTIVATE_KEY_TOKEN variable present in environment")
    exit(0)
# this token must have addcustomer permission
activate_key_token = os.environ['ACTIVATE_KEY_TOKEN']


# for cust in customers:
#     res_customer = Customer.add_customer(add_customer_token, 
#                           name = cust['username'], 
#                           email = cust['email'], 
#                           company_name = cust['companyname'],
#                           enable_customer_association = True)
    
    
#     create_key_res = Key.create_key(create_key_token, 
#                                     product_id, 
#                                     period=30, 
#                                     f1=bool(int(cust['f1'])), 
#                                     f2=bool(int(cust['f2'])), 
#                                     f3=bool(int(cust['f3'])), 
#                                     f4=False, 
#                                     f5=False, 
#                                     f6=False, 
#                                     f7=False, 
#                                     f8=False, 
#                                     notes='', 
#                                     block=False, 
#                                     customer_id=0, 
#                                     new_customer=False, 
#                                     add_or_use_existing_customer=False, 
#                                     trial_activation=False, 
#                                     max_no_of_machines=0, 
#                                     no_of_keys=1, 
#                                     name=None, 
#                                     email=None, 
#                                     company_name=None, 
#                                     enable_customer_association=False, 
#                                     allow_activation_management=False)
    
#     # print(res_customer[0], create_key_res)
#     print(f"f1 f2 f3 {cust['f1']} {cust['f2']} {cust['f3']}")
    
#     cust_first_element = res_customer[0]
#     customer_secret = cust_first_element['secret']
#     cust_id = cust_first_element['customerId']
    
    
#     key_first_element = create_key_res[0]
#     serial = key_first_element['key']
    
    
    
#     print(f"customer_secret {customer_secret} serial {serial} cust_id {cust_id}")
    

    
#     # associate customer with serial
#     PARAMS = {'productid' : product_id, 'key': serial, 'customerid' : cust_id, 'token' : change_customer_token}
#     URL = 'https://api.cryptolens.io/api/key/ChangeCustomer'
#     r = requests.get(url = URL, params = PARAMS)
#     data = r.json()
    
#     print(f'data is {data}')




    
records = [{"customer_secret" : '2205f1d1-32e2-4a2e-8edd-5dc4b6b2d63c', "serial" : 'KCJUE-BOEOH-IFURO-QQXHU', "customer_id" : 40978}]
RSAPubKey = "<RSAKeyValue><Modulus>3enJC3UDpjCb4juG5xhYD/iQNfRNar5yzLe091oZVKL9aLTn+0cPMM+OM65Lfikhr87obfl1SJLyTCaLK5ABjy80WqmgnzVZftkSzM3QTdjFj+KiMf/uv6yuTBQnOtJzNrMDXHZVgVfk0bcdNo1mhjIl7aEBOaURNb9WK3ajs49uFKLVDAm0VTI0fv3RqFfSoYeYMI8yRck8DwPSXGaBXOA5G2bv5mVJYMjI9sWBBwzFM9QR/YIs1GbMG1lcGp7kRUiETMcIqkd3VEqXDOo8Fv8qM7QHWfw34vhat817S9cq2ZWZTOnhLFFYkpXcgYZEBA4Amx7qIzFBSTzz26ziMw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>"
for rec in records:
    # getcustomerlicensebysecret
    PARAMS = {'secret' : rec['customer_secret'], 'token' : auth_token}
    URL = 'https://api.cryptolens.io/api/customer/GetCustomerLicensesBySecret'
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    
    first_license_key = data['licenseKeys'][0]
    
    
    # Verify key
    result = Key.activate(token=activate_key_token,\
                   rsa_pub_key=RSAPubKey,\
                   product_id=product_id, \
                   key=first_license_key['key'],\
                   machine_code=Helpers.GetMachineCode())

    if result[0] == None: # or not Helpers.IsOnRightMachine(result[0]):
        # an error occurred or the key is invalid or it cannot be activated
        # (eg. the limit of activated devices was achieved)
        print(f"The license does not work: {result[1]}")
    else:
        # everything went fine if we are here!
        print("The license is valid!")
        license_key = result[0]
        print(f"Feature 1: {license_key.f1} Feature 2: {license_key.f2} Feature 3: {license_key.f3}" )
        print("License expires: " + str(license_key.expires))
    
    
    
    print(f"first_license_key is {first_license_key}")

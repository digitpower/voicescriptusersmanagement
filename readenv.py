import os
# get CUSTOMER_OPERATIONS_TOKEN from environment
if 'CUSTOMER_OPERATIONS_TOKEN' not in os.environ:
    print("No CUSTOMER_OPERATIONS_TOKEN variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# customer_operations_token = os.environ['CUSTOMER_OPERATIONS_TOKEN']
customer_operations_token = "WyIxOTA3MDU1NSIsIk5BTkc3VUxpTitYcVJIU1ZhdTRiaTdYUGxnTFM3SVVGQ0QrbzkyUVgiXQ=="
# customer_operations_token = ''


# get KEY_OPERATIONS_TOKEN from environment
if 'KEY_OPERATIONS_TOKEN' not in os.environ:
    print("No KEY_OPERATIONS_TOKEN variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# key_operations_token = os.environ['KEY_OPERATIONS_TOKEN']
key_operations_token = "WyIxOTA0MDY2OCIsIkI4TGd5U3FTdGJQZnpTT29aeWlyQjhxZFNzSDEzU3gyT3hsZVBqNlYiXQ=="
# key_operations_token = ''



# get COMPANY_NAME from environment
if 'COMPANY_NAME' not in os.environ:
    print("No COMPANY_NAME variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# company_name = os.environ['COMPANY_NAME']
company_name = "company"
# company_name = ''


# get PRODUCT_ID from environment
if 'PRODUCT_ID' not in os.environ:
    print("No PRODUCT_ID variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# product_id = os.environ['PRODUCT_ID']
product_id = 15301
# product_id = ''

# get MAX_NO_OF_MACHINES from environment
if 'MAX_NO_OF_MACHINES' not in os.environ:
    print("No MAX_NO_OF_MACHINES variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# product_id = os.environ['MAX_NO_OF_MACHINES']
max_no_of_machines = 3
# product_id = ''
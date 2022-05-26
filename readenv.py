import os
# get CUSTOMER_OPERATIONS_TOKEN from environment
if 'CUSTOMER_OPERATIONS_TOKEN' not in os.environ:
    print("No CUSTOMER_OPERATIONS_TOKEN variable present in environment")
    exit(0)
customer_operations_token = os.environ['CUSTOMER_OPERATIONS_TOKEN']


# get KEY_OPERATIONS_TOKEN from environment
if 'KEY_OPERATIONS_TOKEN' not in os.environ:
    print("No KEY_OPERATIONS_TOKEN variable present in environment")
    exit(0)
key_operations_token = os.environ['KEY_OPERATIONS_TOKEN']


# get COMPANY_NAME from environment
if 'COMPANY_NAME' not in os.environ:
    print("No COMPANY_NAME variable present in environment")
    exit(0)
company_name = os.environ['COMPANY_NAME']


# get PRODUCT_ID from environment
if 'PRODUCT_ID' not in os.environ:
    print("No PRODUCT_ID variable present in environment")
    exit(0)
product_id = os.environ['PRODUCT_ID']


# get MAX_NO_OF_MACHINES from environment
if 'MAX_NO_OF_MACHINES' not in os.environ:
    print("No MAX_NO_OF_MACHINES variable present in environment")
    exit(0)
max_no_of_machines = os.environ['MAX_NO_OF_MACHINES']

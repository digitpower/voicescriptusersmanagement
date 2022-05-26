# get CUSTOMER_OPERATIONS_TOKEN from environment
if 'CUSTOMER_OPERATIONS_TOKEN' not in os.environ:
    print("No CUSTOMER_OPERATIONS_TOKEN variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# customer_operations_token = os.environ['CUSTOMER_OPERATIONS_TOKEN']
customer_operations_token = "WyIxOTAxNzg2MiIsIndBVW03ZE83bUZKSVFhQnp1eXQ3T0Nua2lBaDNxTkN5eWNxWEMyRVMiXQ=="
# customer_operations_token = ''


# get KEY_OPERATIONS_TOKEN from environment
if 'KEY_OPERATIONS_TOKEN' not in os.environ:
    print("No KEY_OPERATIONS_TOKEN variable present in environment")
    #exit(0)
# this token must have addcustomer permission
# key_operations_token = os.environ['KEY_OPERATIONS_TOKEN']
key_operations_token = "WyIxOTA0MDY2OCIsIkI4TGd5U3FTdGJQZnpTT29aeWlyQjhxZFNzSDEzU3gyT3hsZVBqNlYiXQ=="
# key_operations_token = ''
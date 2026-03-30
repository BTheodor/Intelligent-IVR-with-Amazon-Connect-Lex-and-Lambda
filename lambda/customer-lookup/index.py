import json
import boto3
import os
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME', 'Customers')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    Looks up customer profile in DynamoDB using the caller's phone number.
    Expects event from Amazon Connect.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Extract phone number from Amazon Connect Contact Data
    # ContactData path depends on how Connect invokes Lambda
    customer_endpoint = event.get('Details', {}).get('ContactData', {}).get('CustomerEndpoint', {})
    phone_number = customer_endpoint.get('Address')
    
    if not phone_number:
        return {
            'CustomerFound': 'False',
            'Error': 'No phone number provided'
        }
    
    try:
        response = table.get_item(Key={'PhoneNumber': phone_number})
        
        if 'Item' in response:
            item = response['Item']
            return {
                'CustomerFound': 'True',
                'CustomerName': item.get('CustomerName', 'Valued Customer'),
                'MembershipLevel': item.get('MembershipLevel', 'Standard'),
                'LastInteraction': item.get('LastInteractionDate', 'N/A')
            }
        else:
            # New customer logic
            return {
                'CustomerFound': 'False',
                'MembershipLevel': 'Standard'
            }
            
    except ClientError as e:
        print(f"Error querying DynamoDB: {e.response['Error']['Message']}")
        return {
            'CustomerFound': 'Error',
            'ErrorMessage': 'Database lookup failed'
        }

import json

def lambda_handler(event, context):
    """
    Decides routing queue and priority based on Lex intent and customer data.
    Input: Lex intent name, Customer Membership level.
    """
    print(f"Received event: {json.dumps(event)}")
    
    # Extract parameters from Amazon Connect Contact Data
    # ContactData.Attributes passed in the Connect 'Invoke Lambda' block
    attributes = event.get('Details', {}).get('ContactData', {}).get('Attributes', {})
    
    lex_intent = attributes.get('LexIntent', 'Default')
    membership_level = attributes.get('MembershipLevel', 'Standard')
    
    # Priority handling based on intent and level
    if lex_intent == 'Emergency' or lex_intent == 'SpeakToAgent':
        routing_decision = {
            'QueueName': 'UrgentSupport',
            'Priority': '1'
        }
    elif membership_level in ['Gold', 'Platinum']:
        routing_decision = {
            'QueueName': 'PremiumSupport',
            'Priority': '2'
        }
    elif lex_intent == 'CheckBalance':
        routing_decision = {
            'QueueName': 'AccountServices',
            'Priority': '5'
        }
    else:
        routing_decision = {
            'QueueName': 'StandardSupport',
            'Priority': '10'
        }
        
    print(f"Routing Decision: {routing_decision}")
    
    # Final response to Amazon Connect
    return routing_decision

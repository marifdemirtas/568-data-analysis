import json
import os

def process_conversations():
    # Read the conversations JSON file
    with open('test.conversations-day-2.json', 'r') as f:
        conversations = json.load(f)
    
    # Read the users JSON file
    with open('test.users.json', 'r') as f:
        users = json.load(f)
    
    # Create a mapping of user IDs to usernames
    user_map = {user['_id']['$oid']: user['username'] for user in users}
    
    # Initialize dictionary to store messages by username
    user_messages = {}
    
    # Process each session
    for session in conversations:
        # Get the user ID and tutor
        user_id = session.get('user', {}).get('$oid', 'unknown')
        username = user_map.get(user_id, f'unknown_{user_id}')
        tutor = session.get('metadata', {}).get('llmService', 'unknown')
        
        # Initialize user's message list if not exists
        if username not in user_messages:
            user_messages[username] = []
        
        # Process each message in the session
        for order, message in enumerate(session.get('messages', [])):
            # Extract content and role
            content = message.get('content', '')
            role = message.get('role', '')
            
            # Add to user's message list with order and empty tag
            user_messages[username].append({
                'tutor': tutor,
                'role': role,
                'content': content,
                'order': order,
                'tag': ''  # Add empty tag key
            })
    
    # Save to a new JSON file
    with open('user_messages-day-2.json', 'w') as f:
        json.dump(user_messages, f, indent=2)

if __name__ == '__main__':
    process_conversations()

"""
Test script for Outlook 365 Email Forwarder Skill
This script tests the core functionality of the Outlook client
"""

import os
import sys
from scripts.outlook_client import Outlook365Client

def test_outlook_client():
    """
    Test the Outlook 365 client functionality
    """
    print("Testing Outlook 365 Client...")
    
    # Get credentials from environment variables
    tenant_id = os.getenv("OUTLOOK_TENANT_ID")
    client_id = os.getenv("OUTLOOK_CLIENT_ID")
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET")
    
    if not all([tenant_id, client_id, client_secret]):
        print("Error: Missing required Outlook 365 credentials in environment variables")
        print("Please set OUTLOOK_TENANT_ID, OUTLOOK_CLIENT_ID, and OUTLOOK_CLIENT_SECRET")
        return False
    
    # Create client instance
    client = Outlook365Client(tenant_id, client_id, client_secret)
    
    # Test authentication
    print("1. Testing authentication...")
    if client.authenticate():
        print("   Authentication successful!")
    else:
        print("   Authentication failed!")
        return False
    
    # Test email search
    print("2. Testing email search...")
    try:
        # Search for recent emails
        emails = client.search_emails("from:me", top=5)
        print(f"   Found {len(emails)} emails from 'me'")
        
        if emails:
            # Test getting an email with attachments
            first_email = emails[0]
            email_id = first_email.get("id")
            print(f"3. Testing attachment check on email: {first_email.get('subject', 'Unknown')}")
            
            email_with_attachments = client.get_message_with_detailed_attachments(email_id)
            attachments = email_with_attachments.get("detailed_attachments", [])
            print(f"   Email has {len(attachments)} attachment(s)")
            
            # Print attachment details if any
            for i, attachment in enumerate(attachments):
                print(f"   Attachment {i+1}: {attachment.get('name')} ({attachment.get('contentType')}) - {attachment.get('size')} bytes")
        
        print("All tests passed!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_outlook_client()
    sys.exit(0 if success else 1)
"""
Outlook 365 Email Forwarder Skill
Python script for connecting to Outlook 365 using Microsoft Graph API
"""

import msal
import requests
import json
from typing import Optional, List, Dict, Any

class Outlook365Client:
    """
    A client for interacting with Outlook 365 via Microsoft Graph API
    """
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        """
        Initialize the Outlook 365 client with authentication credentials
        """
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.graph_url = "https://graph.microsoft.com/v1.0"
        
    def authenticate(self) -> bool:
        """
        Authenticate with Microsoft Graph API using client credentials
        """
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret
        )
        
        # Request token for Microsoft Graph
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            return True
        else:
            print(f"Authentication failed: {result.get('error_description')}")
            return False
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the Microsoft Graph API
        """
        if not self.access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.graph_url}{endpoint}"
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        if response.status_code in [200, 201, 204]:
            if response.content:
                return response.json()
            else:
                return {}
        else:
            response.raise_for_status()
    
    def search_emails(self, search_criteria: str, top: int = 10) -> List[Dict]:
        """
        Search for emails based on criteria
        """
        # Construct the search query
        query_params = f"search={search_criteria}&$top={top}"
        endpoint = f"/me/messages?{query_params}"
        
        result = self._make_request("GET", endpoint)
        return result.get("value", []) if result else []
    
    def search_emails_advanced(self, subject: Optional[str] = None, sender: Optional[str] = None, 
                              received_after: Optional[str] = None, received_before: Optional[str] = None,
                              has_attachments: Optional[bool] = None, top: int = 10) -> List[Dict]:
        """
        Advanced search for emails with multiple criteria
        """
        # Build query parameters
        filters = []
        
        if subject:
            filters.append(f"subject eq '{subject.replace("'", "''")}'")
        
        if sender:
            filters.append(f"from/emailAddress/address eq '{sender}'")
        
        if received_after:
            filters.append(f"receivedDateTime ge {received_after}")
        
        if received_before:
            filters.append(f"receivedDateTime le {received_before}")
        
        if has_attachments is not None:
            filters.append(f"hasAttachments eq {str(has_attachments).lower()}")
        
        # Combine filters
        filter_query = " and ".join(filters)
        
        # Build the endpoint
        endpoint = f"/me/messages"
        params = []
        
        if filter_query:
            params.append(f"$filter={filter_query}")
        
        params.append(f"$top={top}")
        params.append("$select=subject,from,receivedDateTime,id,hasAttachments")
        
        endpoint += "?" + "&".join(params)
        
        result = self._make_request("GET", endpoint)
        return result.get("value", []) if result else []

    def search_emails_by_keywords(self, keywords: str, top: int = 10) -> List[Dict]:
        """
        Search for emails using keywords in subject, body, or sender
        """
        # Use the search parameter which performs a full-text search
        endpoint = f"/me/messages?search=\"{keywords}\"&$top={top}&$select=subject,from,receivedDateTime,id,hasAttachments"
        
        result = self._make_request("GET", endpoint)
        return result.get("value", []) if result else []

    def get_attachments_for_message(self, message_id: str) -> List[Dict]:
        """
        Get all attachments for a specific message
        """
        endpoint = f"/me/messages/{message_id}/attachments"
        result = self._make_request("GET", endpoint)
        return result.get("value", []) if result else []

    def download_attachment(self, attachment_id: str, message_id: str) -> Dict:
        """
        Download a specific attachment by ID
        """
        endpoint = f"/me/messages/{message_id}/attachments/{attachment_id}"
        return self._make_request("GET", endpoint)

    def check_attachment_properties(self, attachment: Dict) -> Dict:
        """
        Check properties of an attachment
        """
        return {
            "id": attachment.get("id"),
            "name": attachment.get("name"),
            "contentType": attachment.get("contentType"),
            "size": attachment.get("size"),
            "isInline": attachment.get("isInline", False),
            "attachmentType": attachment.get("@odata.type")  # Usually #microsoft.graph.fileAttachment or #microsoft.graph.itemAttachment
        }

    def get_message_with_detailed_attachments(self, message_id: str) -> Dict:
        """
        Get message details with comprehensive attachment information
        """
        # Get the message
        message = self._make_request("GET", f"/me/messages/{message_id}")
        
        # Get attachments
        attachments = self.get_attachments_for_message(message_id)
        
        # Process attachment details
        detailed_attachments = []
        for attachment in attachments:
            detailed_attachments.append(self.check_attachment_properties(attachment))
        
        message["detailed_attachments"] = detailed_attachments
        return message

    def forward_email_with_attachments(self, message_id: str, to_recipients: List[str], 
                                     comment: str = "", include_attachments: bool = True) -> Dict:
        """
        Forward an email with option to include attachments
        """
        try:
            # Get the original message
            original_message = self._make_request("GET", f"/me/messages/{message_id}")
            
            # Prepare the forward request
            forward_data = {
                "message": {
                    "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in to_recipients]
                },
                "comment": comment
            }
            
            # If we need to include attachments, we need to handle them specially
            if include_attachments and original_message.get("hasAttachments"):
                # Get the attachments
                attachments = self.get_attachments_for_message(message_id)
                
                # For each file attachment, we need to create a new attachment in the forwarded message
                attachment_objects = []
                for attachment in attachments:
                    if attachment.get("@odata.type") == "#microsoft.graph.fileAttachment":
                        # Add the attachment to our forward request
                        attachment_objects.append({
                            "@odata.type": "#microsoft.graph.fileAttachment",
                            "name": attachment.get("name"),
                            "contentType": attachment.get("contentType"),
                            "contentBytes": attachment.get("contentBytes")  # This might not be available directly
                        })
                
                # Add attachments to the message if any
                if attachment_objects:
                    forward_data["message"]["attachments"] = attachment_objects
            
            # Forward the message
            result = self._make_request("POST", f"/me/messages/{message_id}/createForward", forward_data)
            
            # Send the forwarded message
            if "id" in result:
                self._make_request("POST", f"/me/messages/{result['id']}/send", {})
                return {
                    "success": True,
                    "message": f"Email forwarded successfully to {', '.join(to_recipients)}",
                    "original_subject": original_message.get("subject"),
                    "recipient_count": len(to_recipients)
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to create forward draft"
                }
                
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "message": f"HTTP error occurred: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error forwarding email: {str(e)}"
            }

    def reply_to_email(self, message_id: str, recipients: List[str], content: str, 
                      include_original: bool = True) -> Dict:
        """
        Alternative to forwarding - reply to the email with specified recipients added
        """
        try:
            # Get the original message
            original_message = self._make_request("GET", f"/me/messages/{message_id}")
            
            # Prepare reply request
            reply_data = {
                "message": {
                    "toRecipients": [{"emailAddress": {"address": recipient}} for recipient in recipients],
                    "body": {
                        "contentType": "HTML",
                        "content": content
                    }
                }
            }
            
            # Include original message if requested
            if include_original:
                original_content = original_message.get("body", {}).get("content", "")
                reply_data["message"]["body"]["content"] += f"<hr/><p><b>Original Message:</b></p>{original_content}"
            
            # Reply to the message
            self._make_request("POST", f"/me/messages/{message_id}/createReply", reply_data)
            
            return {
                "success": True,
                "message": f"Reply created successfully with {', '.join(recipients)}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error replying to email: {str(e)}"
            }
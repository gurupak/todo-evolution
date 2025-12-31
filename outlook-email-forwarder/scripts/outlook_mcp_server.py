#!/usr/bin/env python3
"""
MCP Server for Outlook 365 Email Forwarder Skill.

This server provides tools to interact with Outlook 365, including email search,
attachment checking, and email forwarding capabilities.
"""

from typing import Optional, List, Dict, Any
from enum import Enum
import os
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession
from mcp.types import Tool, InitializationOptions
import asyncio

# Import our Outlook client
from outlook_client import Outlook365Client  # This would be our implementation from earlier

# Initialize the MCP server
mcp = FastMCP("outlook_email_forwarder")

# Define Pydantic models for input validation
class EmailSearchInput(BaseModel):
    """Input model for searching emails."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    search_criteria: str = Field(
        ..., 
        description="Search criteria for finding emails (e.g., 'subject:Quarterly Report', 'from:manager@company.com')", 
        min_length=1, 
        max_length=500
    )
    top: Optional[int] = Field(
        default=10, 
        description="Maximum number of results to return", 
        ge=1, 
        le=100
    )

class EmailForwardInput(BaseModel):
    """Input model for forwarding emails."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    message_id: str = Field(
        ..., 
        description="ID of the email message to forward", 
        min_length=1
    )
    to_recipients: List[str] = Field(
        ..., 
        description="List of email addresses to forward to", 
        min_items=1
    )
    comment: Optional[str] = Field(
        default="", 
        description="Optional comment to include with the forwarded email"
    )
    include_attachments: Optional[bool] = Field(
        default=True, 
        description="Whether to include attachments in the forwarded email"
    )

class AttachmentCheckInput(BaseModel):
    """Input model for checking email attachments."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    message_id: str = Field(
        ..., 
        description="ID of the email message to check for attachments", 
        min_length=1
    )

# Global client instance
outlook_client: Optional[Outlook365Client] = None

def initialize_client():
    """Initialize the Outlook client with credentials from environment variables."""
    global outlook_client
    
    tenant_id = os.getenv("OUTLOOK_TENANT_ID")
    client_id = os.getenv("OUTLOOK_CLIENT_ID") 
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET")
    
    if not all([tenant_id, client_id, client_secret]):
        raise ValueError("Missing required Outlook 365 credentials in environment variables")
    
    outlook_client = Outlook365Client(tenant_id, client_id, client_secret)
    
    if not outlook_client.authenticate():
        raise Exception("Failed to authenticate with Outlook 365")

@mcp.tool(
    name="outlook_search_emails",
    description="Search for emails in Outlook 365 based on specified criteria.",
    parameters=EmailSearchInput
)
async def search_emails(params: EmailSearchInput) -> str:
    """Search for emails in Outlook 365."""
    global outlook_client
    
    if not outlook_client:
        initialize_client()
    
    try:
        emails = outlook_client.search_emails(params.search_criteria, params.top)
        
        if not emails:
            return f"No emails found matching criteria: {params.search_criteria}"
        
        # Format the results
        result = {
            "found_emails": len(emails),
            "emails": []
        }
        
        for email in emails:
            email_info = {
                "id": email.get("id"),
                "subject": email.get("subject", "No Subject"),
                "sender": email.get("from", {}).get("emailAddress", {}).get("address", "Unknown"),
                "received": email.get("receivedDateTime"),
                "has_attachments": email.get("hasAttachments", False)
            }
            result["emails"].append(email_info)
        
        return f"Found {len(emails)} emails:\n{str(result)}"
    except Exception as e:
        return f"Error searching emails: {str(e)}"

@mcp.tool(
    name="outlook_check_attachments",
    description="Check if a specific email has attachments and get attachment details.",
    parameters=AttachmentCheckInput
)
async def check_attachments(params: AttachmentCheckInput) -> str:
    """Check if an email has attachments."""
    global outlook_client
    
    if not outlook_client:
        initialize_client()
    
    try:
        message_with_attachments = outlook_client.get_message_with_detailed_attachments(params.message_id)
        
        attachments = message_with_attachments.get("detailed_attachments", [])
        
        if not attachments:
            return f"Email {params.message_id} has no attachments."
        
        result = {
            "email_id": params.message_id,
            "attachment_count": len(attachments),
            "attachments": []
        }
        
        for attachment in attachments:
            attachment_info = {
                "id": attachment.get("id"),
                "name": attachment.get("name"),
                "contentType": attachment.get("contentType"),
                "size": attachment.get("size"),
                "isInline": attachment.get("isInline")
            }
            result["attachments"].append(attachment_info)
        
        return f"Email has {len(attachments)} attachment(s):\n{str(result)}"
    except Exception as e:
        return f"Error checking attachments: {str(e)}"

@mcp.tool(
    name="outlook_forward_email",
    description="Forward a specific email to one or more recipients, optionally including attachments.",
    parameters=EmailForwardInput
)
async def forward_email(params: EmailForwardInput) -> str:
    """Forward an email to specified recipients."""
    global outlook_client
    
    if not outlook_client:
        initialize_client()
    
    try:
        result = outlook_client.forward_email_with_attachments(
            params.message_id,
            params.to_recipients,
            params.comment,
            params.include_attachments
        )
        
        return f"Forwarding result: {str(result)}"
    except Exception as e:
        return f"Error forwarding email: {str(e)}"

# Run the server
if __name__ == "__main__":
    import asyncio
    import sys
    
    # Check for required environment variables
    required_env_vars = ["OUTLOOK_TENANT_ID", "OUTLOOK_CLIENT_ID", "OUTLOOK_CLIENT_SECRET"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these environment variables before running the server.")
        sys.exit(1)
    
    # Start the MCP server
    asyncio.run(mcp.run())
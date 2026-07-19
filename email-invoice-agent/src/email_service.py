import os
import base64
from dataclasses import dataclass
from config import *
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from loguru import logger
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


load_dotenv()


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


@dataclass
class EmailAttachment:
    filename: str
    data: bytes
    subject: str
    sender: str


class EmailService:
    def __init__(self):
        self.service = None

    def connect(self):
        credentials = None
        if TOKEN_FILE.exists():
            credentials = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    SCOPES
                )
                credentials = flow.run_local_server(
                    port=0
                )
            TOKEN_FILE.write_text(
                credentials.to_json(),
                encoding="utf-8"
            )
        self.service = build(
            "gmail",
            "v1",
            credentials=credentials
        )
        logger.success("Connected to Gmail API")


    def fetch_unread_pdf_attachments(self) -> List[EmailAttachment]:
        attachments = []
        result = self.service.users().messages().list(
            userId="me",
            q="is:unread"
        ).execute()
        messages = result.get("messages", [])
        logger.info(
            "Found {} unread email(s)",
            len(messages)
        )
        for message in messages:
            email_data = self.service.users().messages().get(
                userId="me",
                id=message["id"]
            ).execute()
            headers = email_data["payload"].get("headers", [])
            subject = self._get_header(
                headers,
                "Subject"
            )
            sender = self._get_header(
                headers,
                "From"
            )
            self._extract_parts(
                email_data["payload"],
                attachments,
                subject,
                sender,
                message["id"]
            )
        return attachments

    def _extract_parts(
            self,
            payload,
            attachments,
            subject,
            sender,
            message_id,
    ):
        if "parts" in payload:
            for part in payload["parts"]:
                self._extract_parts(
                    part,
                    attachments,
                    subject,
                    sender,
                    message_id
                )
        filename = payload.get("filename")
        if filename and filename.lower().endswith(".pdf"):
            attachment_id = payload["body"].get("attachmentId")
            if attachment_id:
                attachment = self.service.users().messages().attachments().get(
                    userId="me",
                    messageId=message_id,
                    id=attachment_id
                ).execute()
                data = base64.urlsafe_b64decode(
                    attachment["data"] + "=="
                )
                attachments.append(
                    EmailAttachment(
                        filename=filename,
                        data=data,
                        subject=subject,
                        sender=sender
                    )
                )
                logger.info(
                    "Downloaded {}",
                    filename
                )


    @staticmethod
    def _get_header(headers, name):
        for header in headers:
            if header["name"].lower() == name.lower():
                return header["value"]

        return ""
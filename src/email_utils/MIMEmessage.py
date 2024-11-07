"""Email message.

Create email message.

Functions:
    create_email_message(subject, message, sender, recipients) -> msg.

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import policy


def create_email_message(
    subject: str,
    message: str,
    sender: str,
    recipients: list,
) -> MIMEMultipart:
    """
    Create email message.

        Parameters:
            subject (str): Message subject.
            message (str): Message to send.
            sender (str): Sender.
            recipients (list): Recipients.

        Returns:
            msg (MIMEMultipart): Email message.

    """
    msg = MIMEMultipart(policy=policy.default)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Bcc"] = ",".join(recipients)
    text = MIMEText(message, "plain", "utf-8")
    msg.attach(text)

    return msg

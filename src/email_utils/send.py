"""Send message.

Send message in email.

Functions:
    send_message(
        subject,
        message,
        senders_recipients,
        limit,
        recipients_part,
        timeout,
    ) -> Message.

"""

import time
from fastapi import HTTPException, status
from sender.utils.MIMEmessage import create_email_message
from sender.utils.smtp_connection import smtp_connect


async def send_message(
    subject: str,
    message: str,
    senders_recipients: list[dict],
    limit: int,
    recipients_part: int,
    timeout: float,
) -> dict:
    """
    Send message in email.

        Parameters:
            subject (str): Message subject.
            message (str): Message to send.
            senders_recipients (list[dict]): senders and recipients.
            limit (int): Limit messages for account.
            recipients_part (int): recipients part for one request.
            timeout (float): Timeout between requests.

        Exceptions:
            HTTPException: Any error, error_code=400

        Returns:
            error_limit (dict): Message limit send messages.
            success (dict): Message success.

    """

    error_limit = {"Message": "Limit send messages for account"}
    success = {"Message": "Success"}

    for send_data in senders_recipients:
        send_data["send_messages"][0] += recipients_part
        if send_data["send_messages"][0] > limit:
            return error_limit

        email = send_data["sender"]
        recipients = send_data["recipients"]
        if "gmail.com" in email["login"]:
            smtp_server = "smtp.gmail.com"
        else:
            smtp_server = "smtp.mail.ru"

        try:
            email_message = create_email_message(
                subject=subject,
                message=message,
                sender=email["login"],
                recipients=recipients,
            )
            print(recipients)  # Print current recipients.

            server = smtp_connect(
                host=smtp_server,
                login=email["login"],
                password=email["password"],
            )
            server.send_message(email_message)
            server.quit()
            time.sleep(timeout)  # Timeout before next request.
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error: {e}"
            ) from e

    return success

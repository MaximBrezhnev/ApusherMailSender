"""Модуль, содержащий функции для отправки почты."""

import time
from email import policy
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from pprint import pprint

from src import constants
from src import file_utils


def send_message(
    subject: str,
    message: str | None,
    message_file_path: str | None,
    senders_and_recipients: list[dict],
) -> None:
    """
    Производит рассылку почты.

    Каждый аккаунт для рассылки отправляет письма указанным получателям. Рассылки с разных аккаунтов
    разделены между собой таймаутом.
    """

    for send_data in senders_and_recipients:
        sender = send_data["sender"]
        recipients = send_data["recipients"]

        if "gmail.com" in sender["login"]:
            smtp_server = "smtp.gmail.com"
        else:
            smtp_server = "smtp.mail.ru"

        try:
            email_message = create_email_message(
                subject=subject,
                message=message,
                message_file_path=message_file_path,
                sender=sender["login"],
                recipients=recipients,
            )

            print(f"Текущий аккаунт для рассылки: {sender['login']}")
            pprint(f"Текущие получатели: {recipients}")

            server = smtp_connect(
                host=smtp_server,
                login=sender["login"],
                password=sender["password"],
            )

            print("Отправка сообщений...")
            server.send_message(email_message)
            server.quit()

            time.sleep(constants.EMAIL_TIMEOUT)

        except Exception as exc:
            print(f"Произошла ошибка при рассылке почты: {exc}")


def create_email_message(
    subject: str,
    message: str | None,
    message_file_path: str | None,
    sender: str,
    recipients: list,
) -> MIMEMultipart:
    """Формирует сообщение для рассылки."""

    msg = MIMEMultipart(policy=policy.default)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["Bcc"] = ",".join(recipients)

    if message:
        text = MIMEText(message, "plain", "utf-8")
    elif message_file_path:
        text = file_utils.load_message_from_file(file_path=message_file_path)

    msg.attach(text)
    return msg


def smtp_connect(
    host: str,
    login: str,
    password: str,
) -> SMTP_SSL:
    """Устанавливает соединение с smtp-сервером."""

    server = SMTP_SSL(host=host, port=SMTP_SSL_PORT)
    server.login(login, password)
    server.auth_plain()

    return server

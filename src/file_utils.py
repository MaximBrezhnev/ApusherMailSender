"""Модуль для работы с файлами."""

import csv
from email.mime.text import MIMEText

from src import constants


def check_csv(filename: str) -> bool:
    """Проверят, что файл имеет формат .csv."""

    return filename.strip('"').endswith(".csv")


def process_file_data(
    senders: str, recipients: str,
) -> list[dict]:
    """
    Извлекает данные из файлов с получателями и отправителями.
    Распределяет получателей между аккаунтами для рассылки.
    """

    # Чтение данных из csv-файлов
    senders_and_recipients = []
    for file in [senders, recipients]:
        with open(file.strip('"'), "r") as f:
            csv_reader = csv.DictReader(f)
            csv_list = [row for row in csv_reader]
            senders_and_recipients.append(csv_list)

    senders, recipients = senders_and_recipients
    recipients = [recipient["recipient"] for recipient in recipients]

    # Распределение получателей между аккаунтами для рассылки
    send_lst = [[0].copy() for _ in range(len(senders))]
    senders_and_recipients.clear()

    while recipients:
        for i, sender in enumerate(senders):
            cur_dict = {
                "sender": sender,
                "recipients": recipients[:constants.EMAIL_RECIPIENTS_PER_REQUEST],
                "send_messages": send_lst[i],
            }
            senders_and_recipients.append(cur_dict)

            recipients = recipients[constants.EMAIL_RECIPIENTS_PER_REQUEST:]
            if not recipients:
                break

    return senders_and_recipients


def load_message_from_file(file_path: str) -> MIMEText:
    """Загружает содержимое файла и возвращает в виде MIMEText."""

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

        if file_path.endswith(".html"):
            return MIMEText(content, "html", "utf-8")
        else:
            return MIMEText(content, "plain", "utf-8")

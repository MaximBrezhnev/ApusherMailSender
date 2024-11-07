"""Decode and filter module.

Decode and filter senders, recipients files.

Functions:
    decode_filter(senders, recipients, recipients_part) -> senders_recipients.

"""

import csv
from fastapi import UploadFile


async def decode_filter(
    senders: UploadFile,
    recipients: UploadFile,
    recipients_part: int,
) -> list:
    """
    Decode and filter sender, recipients files.

        Parameters:
            senders (UploadFile): csv file senders.
            recipients (UploadFile): csv file recipients.
            recipients_part (int): recipients part for one request.

        Returns:
            senders_recipients (list[dict]): senders and recipients dicts.

    """

    senders_recipients = []
    for file in [senders, recipients]:  # Decode csv files.
        content = await file.read()
        csv_data = content.decode("utf-8").splitlines()
        csv_reader = csv.DictReader(csv_data)
        csv_list = [dict_data for dict_data in csv_reader]
        senders_recipients.append(csv_list)
    senders, recipients = senders_recipients
    recipients = [recipient["recipient"] for recipient in recipients]

    # Filter senders and recipients.
    send_lst = [[0].copy() for _ in range(len(senders))]
    senders_recipients.clear()
    while recipients:
        for i, sender in enumerate(senders):
            cur_dict = {
                "sender": sender,
                "recipients": recipients[:recipients_part],
                "send_messages": send_lst[i],
            }
            senders_recipients.append(cur_dict)
            recipients = recipients[recipients_part:]
            if not recipients:
                break

    return senders_recipients

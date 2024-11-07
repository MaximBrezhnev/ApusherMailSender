"""Check csv files.

Check senders and recipients are csv files.

Functions:
    check_csv(senders, recipients) -> None

"""

from fastapi import UploadFile, HTTPException, status


async def check_csv(
    senders: UploadFile,
    recipients: UploadFile,
) -> None:
    """
    Check senders and recipients are csv files.

        Parameters:
            senders (UploadFile): csv file senders.
            recipients (UploadFile): csv file recipients.

        Exceptions:
            HTTPException: Download no csv file, error_code=400

        Returns:
            None

    """

    senders_csv = senders.filename.endswith(".csv")
    recipients_csv = recipients.filename.endswith(".csv")

    if not(senders_csv and recipients_csv):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Download no csv file",
        )

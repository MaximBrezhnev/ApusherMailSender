"""SMTP connection.

Connect and log in to SMTP server.

Functions:
    smtp_connect(host, login, password) -> server.

"""

from smtplib import SMTP_SSL, SMTP_SSL_PORT


def smtp_connect(
    host: str,
    login: str,
    password: str,
) -> SMTP_SSL:
    """
    Connect and log in to SMTP server.

        Parameters:
            host (str): Host address.
            login (str): Account login.
            password (str): Account password.

        Returns:
            server (SMTP_SSL): Server object.

    """

    server = SMTP_SSL(host=host, port=SMTP_SSL_PORT)
    server.login(login, password)
    server.auth_plain()

    return server

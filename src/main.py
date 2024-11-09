"""Основной модуль приложения, через который осуществляется его запуск."""

from src import file_utils
from src import email_utils


def main() -> None:
    """
    Основная функция приложения:
    * Получает необходимые данные из консоли;
    * Проводит валидацию полученных файлов отправителей и получателей;
    * Получает обработанные данные из этих файлов;
    * Вызывает функцию рассылки почты.
    """

    subject = input("Введите тему письма для рассылки: ")

    while True:
        message_format = input(
            "Если сообщение для рассылки будет введено в консоль, введите 1, "
            "если оно будет содержаться в файле, введите 2: "
        )
        if message_format not in ("1", "2", ):
            print("Введено некорректное значение. Повторите попытку ввода")
        else:
            break

    message = None
    message_file_path = None
    if message_format == "1":
        message = input("Введите сообщение для рассылки: ")
    else:
        plain_message_file_path = input(
            "Введите абсолютный путь к файлу (txt или html), содержащему сообщение для рассылки: "
        )
        message_file_path = plain_message_file_path.strip('"')

    while True:
        senders_file = input("Введите абсолютный путь к csv-файлу с аккаунтами, с которых будет идти рассылка: ")
        if not file_utils.check_csv(filename=senders_file):
            print("Некорректный формат файла. Повторите попытку ввода")
        else:
            break

    while True:
        recipients_file = input("Введите абсолютный путь к csv-файлу с получателями рассылки: ")
        if not file_utils.check_csv(filename=recipients_file):
            print("Некорректный формат файла. Повторите попытку ввода")
        else:
            break

    try:
        senders_and_recipients = file_utils.process_file_data(
            senders=senders_file,
            recipients=recipients_file
        )
        email_utils.send_message(
            subject=subject,
            message=message,
            message_file_path=message_file_path,
            senders_and_recipients=senders_and_recipients
        )
    except Exception as exc:
        print(f"Некорректные данные отправителей/получателей: {exc}")

    print("Рассылка почты завершена")


if __name__ == "__main__":
    main()

# О сервисе
Приложение, производящее рассылку с переданных аккаунтов на переданные почты

# Работа приложения:
1. В консоли пользователем вводится тема письма для рассылки
2. Далее выбирается формат сообщения для рассылки, а именно будет ли введено сообщение в консоли или передан путь к файлу с ним (поддерживается txt и html)
3. После этого передается соответствующее выбору значение
4. Далее пользователь вводит в консоль абсолютный путь к файлам с получателями и отправителями рассылки согласно формату `recipients.example.txt` и `senders.example.txt`
5. После чего начинается процесс отправки сообщений: с каждого аккаунта происходит рассылка на определенное количество адресов, после чего аккаунт меняется на следующий

# Запуск проекта
Для запуска проекта без использования exe-файла выполнить следующую команду:
```
python -m src.main
```
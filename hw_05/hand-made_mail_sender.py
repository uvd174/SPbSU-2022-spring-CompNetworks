#! /usr/local/bin/python
import sys
import base64
import socket
import ssl


USERNAME = 'USERNAME'
PASSWORD = 'PASSWORD'

SMTP_server = 'smtp.mail.ru'
SMTP_port = 465
sender = 'SENDER'

destination = sys.argv[1]
content_file_path = sys.argv[2]
is_image = content_file_path.endswith('.jpg')

if is_image:
    with open(content_file_path, 'rb') as content_file:
        content = content_file.read()
        content = base64.b64encode(content).decode('utf-8')
else:
    with open(content_file_path, 'rt') as content_file:
        content = content_file.read()

subject = 'Sent from Python'


def tobase64(string: str):
    return base64.b64encode(string.encode('utf-8')).decode('utf-8')


def send_message_and_check_reply(client_socket, message, code=-1, no_response=False):
    print(f'Command: {message}')
    data = message.encode('utf-8')
    client_socket.sendall(data)

    if no_response:
        return

    response = client_socket.recv(2048).decode('utf-8')
    print(f'Response: {response}')

    if code != -1 and response is not None and not response.startswith(str(code)):
        raise RuntimeError('Wrong response code!')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as smtp_socket:
    secure_socket = ssl.wrap_socket(smtp_socket)
    secure_socket.connect((SMTP_server, SMTP_port))

    initial_response = secure_socket.recv(2048).decode('utf-8')
    print(f"Initial response: {initial_response}")
    if not initial_response.startswith('220'):
        raise RuntimeError('Initial response was wrong!')

    send_message_and_check_reply(secure_socket, f"HELO python_script\r\n", code=250)
    send_message_and_check_reply(secure_socket, f"AUTH LOGIN\r\n", code=334)
    send_message_and_check_reply(secure_socket, f"{tobase64(USERNAME)}\r\n", code=334)
    send_message_and_check_reply(secure_socket, f"{tobase64(PASSWORD)}\r\n", code=235)
    send_message_and_check_reply(secure_socket, f"MAIL FROM: {sender}\r\n", code=250)
    send_message_and_check_reply(secure_socket, f"RCPT TO: {destination}\r\n", code=250)
    send_message_and_check_reply(secure_socket, f"DATA\r\n", code=354)

    message_content = f"""From: {sender}
To: {destination}
Subject: {subject}
"""
    if is_image:
        message_content += """Content-Type: image/jpeg; name=picture.jpg
Content-Transfer-Encoding: base64

"""

    message_content += content + '\r\n'

    send_message_and_check_reply(secure_socket, message_content, no_response=True)
    send_message_and_check_reply(secure_socket, f'.\r\n', code=250)
    send_message_and_check_reply(secure_socket, f'QUIT\r\n', no_response=True)

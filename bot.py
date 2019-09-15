#!/usr/bin/python3

import sys
import socket
import ssl
import datetime
import time

# Connection config
server_ip = ('irc.chat.twitch.tv', 6697)
channel = '#'

# Bot credentials
username = ''
token = 'oauth:'

# Social media
discord = 'https://discord.gg/'
donate_url = ''

# Commands
prefix = '!'
commands = {
    'discord': discord,
    'donate': donate_url,
    'ping': 'pong Kappa',
    'ding': 'dong Kappa'
}


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(sock)
    print(f'Connecting to {ip}...')
    try:
        sock.connect(server_ip)
        print('Connection established!')
    except:
        print('Connection failed!')
        print('Exiting...')
        time.sleep(3)
        sys.exit()

    print(f'Attepting to login to channel {channel}')
    sys_message(sock, f'PASS {token}')
    sys_message(sock, f'NICK {username}')
    sys_message(sock, f'JOIN {channel}')

    while True:
        for line in str(sock.recv(4096)).split('\\r\\n'):
            line = line.split(':', 2)

            if 'PING' in line[0]:
                sys_message(sock, f'PONG :{line[1]}')

            elif len(line) > 2:
                user = (line[1].split('!'))[0]
                msg = line[2]
                timestamp = datetime.datetime.now().strftime('%H:%M')

                if msg[:len(prefix)] == prefix:
                    cmd = msg[len(prefix):].lower()

                    if cmd == 'commands':
                        avail_commands = ', '.join(
                            [prefix + command for command in commands])
                        send_message(sock, avail_commands)
                    elif cmd in commands:
                        send_message(sock, commands.get(cmd))

                print(f'({timestamp}) {user}: {msg}')


def send_message(sock, msg):
    sock.send(bytes(f'PRIVMSG {channel} :{msg}\r\n', 'utf-8'))


def sys_message(sock, msg):
    sock.send(bytes(f'{msg}\r\n', 'utf-8'))


if __name__ == '__main__':
    main()

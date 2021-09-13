import asyncio
import asyncssh


async def send_show(host, username, password, connection_timeout=3):
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
    else:
        return host


async def send_command_to_devices(devices):
    coroutines = [send_show(**device) for device in devices]
    result = await asyncio.gather(*coroutines)
    return result


def get():
    devices = [
        {'host': '192.168.20.254',
         'username': 'admin',
         'password': 'ghKflV@terem'},
        {'host': '192.168.40.254',
         'username': 'admin',
         'password': 'ghKflV@terem'},
        {'host': '192.168.8.254',
         'username': 'admin',
         'password': 'ghKflV@terem'},
    ]
    result = asyncio.run(send_command_to_devices(devices))
    return result


print(get())

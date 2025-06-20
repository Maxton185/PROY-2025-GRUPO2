import usocket
import ujson

def request(method, url, data=None, json=None, headers={}):
    _, _, host, path = url.split('/', 3)
    addr = usocket.getaddrinfo(host, 443)[0][-1]
    s = usocket.socket()
    s.connect(addr)
    s = ussl.wrap_socket(s, server_hostname=host)

    if json is not None:
        data = ujson.dumps(json)
        headers['Content-Type'] = 'application/json'

    s.write('{} /{} HTTP/1.0\r\nHost: {}\r\n'.format(method, path, host))
    for k, v in headers.items():
        s.write('{}: {}\r\n'.format(k, v))
    if data:
        s.write('Content-Length: {}\r\n'.format(len(data)))
    s.write('\r\n')
    if data:
        s.write(data)

    l = s.readline()
    while True:
        line = s.readline()
        if line == b'' or line == b'\r\n':
            break

    return s

def post(url, data=None, json=None, headers={}):
    return request('POST', url, data=data, json=json, headers=headers)

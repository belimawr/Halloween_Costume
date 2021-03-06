import socket
import halloween

class Request:
    def __init__(self):
        self.path = ''
        self.method = ''
        self.body = None
        self.headers = {}
        self.querystring = {}

class HTTPServer:
    def __init__(self, address= '0.0.0.0', port=80, timeout=None, debug=False):
        self._port = port
        self._timeout = timeout
        self._addr = address
        self._DEBUG = debug
        self._socket = None

    def serve_forever(self):
        try:
            self._start_web_server()
        except KeyboardInterrupt:
            self._debug('Closing socket...')
            self._socket.close()
            self._debug('Good Bye ;)')

    def async_server(self):
        self._socket = socket.socket()
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((self._addr, self._port))
        self._socket.listen(1)
        self._socket.setsockopt(socket.SOL_SOCKET, 20, self._async_handler)

    def _start_web_server(self):
        self._socket = socket.socket()
        self._socket.bind((self._addr, self._port))
        self._socket.settimeout(self._timeout)
        self._socket.listen(1)
        self._debug('Listening for requests on port:', self._port)

        while True:
            cl, addr = self._socket.accept()
            cl_file = cl.makefile('rwb')
            status = 200
            try:
                self._parse_request(cl_file)
            except Exception as e:
                status = 500
                print('Internal server error:', e)
            response = 'HTTP/1.0 %s\n\n' % status
            cl.send(bytes(response, 'UTF-8'))
            cl_file.close()
            cl.close()

    def _async_handler(self, listen_sock):
        cl, remote_addr = listen_sock.accept()
        cl_file = cl.makefile('rwb')
        status = 200
        try:
            r = self._parse_request(cl_file)
            handle_request(r)
        except Exception as e:
            status = 500
            print('Internal server error:', e)
        response = 'HTTP/1.0 %s\n\n' % status
        cl.send(bytes(response, 'UTF-8'))
        cl_file.close()
        cl.close()

    def _parse_request(self, cl_file):
        request = Request()

        # Read the first line
        line = cl_file.readline()
        line = line.decode('utf8')

        # Parse the line and get method and path
        split_line = line.split(' ')
        request.method = split_line[0]
        request.path = split_line[1]

        self._parse_query_string(request)
        self._parse_body(request, cl_file)

        self._debug('***********************************')
        self._debug(request.method.upper())
        self._debug(request.path)
        self._debug(request.querystring)
        self._debug(request.headers)
        self._debug(request.body)
        self._debug('***********************************')
        self._debug('Waiting for another request...')
        return request

    def _parse_body(self, request, cl_file):
        if request.headers.get('Content-Length'):
            length = int(request.headers.get('Content-Length'))
            request.body = cl_file.read(length)

    def _parse_query_string(self, request):
        if '?' in request.path:
            path, qs = request.path.split('?')
            qs_dict = {}
            for pair in qs.split('&'):
                k, v = pair.split('=')
                if k in qs_dict:
                    if isinstance(qs_dict[k], list):
                        qs_dict[k].append(v)
                    else:
                        qs_dict[k] = [qs_dict[k]]
                        qs_dict[k].append(v)
                else:
                    qs_dict[k] = v
            request.querystring = qs_dict
            request.path = path

    def _debug(self, *args, **kwargs):
        if self._DEBUG:
            print(*args, **kwargs)

def handle_request(request):
    pp = request.path
    print('command:', pp)
    repeat = request.querystring.get('repeat', '1')
    repeat = int(repeat)
    for _ in range(repeat):
        if request.path == '/blink':
            t = request.querystring.get('times', 2)
            halloween.blink(times=int(t))

        elif request.path == '/all_on':
            delay = request.querystring.get('delay', '0')
            delay = int(delay)
            halloween.all_on(delay)

        elif request.path == '/all_off':
            halloween.all_off()

        elif request.path == '/fade_in':
            delay = request.querystring.get('delay', '0.01')
            delay = float(delay)

            step = request.querystring.get('step', '1')
            step = int(step)

            pins = request.querystring.get('pins', None)

            halloween.fade_in(delay=delay, step=step, pins=pins)

        elif request.path == '/fade_out':
            delay = request.querystring.get('delay', '0.01')
            delay = float(delay)

            step = request.querystring.get('step', '1')
            step = int(step)

            pins = request.querystring.get('pins', None)

            halloween.fade_out(delay=delay, step=step, pins=pins)

        elif request.path == '/fade_blink':
            delay = request.querystring.get('delay', '0.01')
            delay = float(delay)

            step = request.querystring.get('step', '1')
            step = int(step)

            pins = request.querystring.get('pins', None)

            halloween.fade_blink(delay=delay, step=step, pins=pins)

        elif request.path == '/fade_blink_one':
            delay = request.querystring.get('delay', '0.01')
            delay = float(delay)

            step = request.querystring.get('step', '1')
            step = int(step)

            pins = request.querystring.get('pins', None)

            halloween.fade_blink_one(delay=delay, step=step, pins=pins)

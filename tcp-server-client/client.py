import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, ip, port, timeout=None):
        self.connection = socket.create_connection((ip, port), timeout)
        self.ip = ip
        self.port = ip
        self.timeout = timeout

    @staticmethod
    def _make_metrics_dict(response):
        list_of_metrics = response[3:-2].split(b'\n')

        for byte_metric in list_of_metrics:
            list_of_metrics[list_of_metrics.index(byte_metric)] = byte_metric.decode('utf-8')
        print(list_of_metrics)

        metrics_dict = {}

        for string_metric in list_of_metrics:
            metric_list = string_metric.split()
            print(metric_list)
            metric_list.reverse()
            key = metric_list.pop()
            if not metrics_dict.get(key):
                metrics_dict[key] = []
            metric_list.reverse()
            print(metric_list)
            for value in metric_list:
                if metric_list.index(value) % 2 == 1:
                    pair = (int(value), float(metric_list[metric_list.index(value) - 1]))
                    metrics_dict[key].append(pair)
            print(metrics_dict)

        return metrics_dict

    def _receive_data(self):
        response = bytearray()
        data = self.connection.recv(1024)
        response += data
        return response

    def close_connection(self):
        self.connection.close()

    def put(self, key, value, timestamp=time.time()):
        try:
            self.connection.sendall(f'put {key} {float(value)} {int(timestamp)}\n'.encode('utf-8'))
            response = self._receive_data()
            if response == b'error\nwrong command\n\n':
                raise ClientError
        except (socket.error, socket.timeout):
            pass

    def get(self, key):
        try:
            self.connection.sendall(f'get {key}\n'.encode('utf-8'))
            response = self._receive_data()
            if response == b'ok\n\n':
                return {}
            elif response == b'error\nwrong command\n\n':
                raise ClientError
            else:
                return self._make_metrics_dict(response)
        except (socket.error, socket.timeout):
            pass

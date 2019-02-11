import socket
import time


class ClientError(Exception):
    """Общий класс исключений клиента"""
    pass


class ClientSocketError(ClientError):
    """Исключение, выбрасываемое клиентом при сетевой ошибке"""
    pass


class ClientProtocolError(ClientError):
    """Исключение, выбрасываемое клиентом при ошибке протокола"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        # класс инкапсулирует создание соединения
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("error create connection", err)

    def _read(self):
        """Метод для чтения ответа сервера"""
        data = b""
        # накапливаем части строки, пока не встретим "\n\n" в конце команды,
        # что означает конец сообщения в условленном протоколе обмена данными
        # между сервером и клиентом
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError("error recv data", err)

        # преобразовываем байтовую строку в обычную
        decoded_data = data.decode()
        
        # разбираем строку на статус ответа и сами данные метрик
        # разбиваем по первому найденому \n т.к. 
        # следующие разделители строк - разные метрики
        status, metrics = decoded_data.split("\n", 1)
        metrics = metrics.strip()

        # если получили ошибку - бросаем исключение нарушения 
        # протокола взаимодействия
        if status == "error":
            raise ClientProtocolError(payload)

        return metrics

    def put(self, key, value, timestamp=None):
        # если временная unix-метка не передана,
        # создаем ее сами
        timestamp = timestamp or int(time.time())

        # отправляем запрос команды put
        try:
            self.connection.sendall(
                f"put {key} {value} {timestamp}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # разбираем ответ
        self._read()

    def get(self, key):
        # формируем и отправляем запрос команды get
        try:
            self.connection.sendall(
                f"get {key}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # читаем ответ
        metrics = self._read()

        data = {}
        if metrics == "":
            return data

        # разбираем ответ для команды get
        for row in metrics.split("\n"):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))

        return data

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("error close connection", err)

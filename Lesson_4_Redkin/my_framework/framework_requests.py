class GetRequests:
    """Класс для распарсивания get-запросов"""

    @staticmethod
    def parse_input_data(data: str):
        """Преобразует строку в словарь"""
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_request_params(environ):
        """Преобразует строку запроса в словарь"""
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_input_data(query_string)
        return request_params


class PostRequests:
    """Класс для распарсивания post-запросов"""

    @staticmethod
    def parse_input_data(data: str):
        """Преобразует строку в словарь"""
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(environ) -> bytes:
        """Получает данные в виде байт"""
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        """Преобразует байты в словарь"""
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        """Преобразует данные запроса в словарь"""
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data

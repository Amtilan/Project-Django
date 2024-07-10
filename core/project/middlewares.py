"""
Этот код определяет класс промежуточного программного обеспечения Django под названием ElasticApmMiddleware, 
который предназначен для создания отдельных транзакций для каждого запроса и ответа, 
а также для добавления тела ответа в контекст Elastic APM (Мониторинг производительности приложений) для дальнейшего анализа. 
"""


import json
from typing import Callable

from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.urls import (
    resolve,
    Resolver404,
)

import elasticapm


class ElasticApmMiddleware:
    """
    Middleware для создания отдельных транзакций.
    Также добавляет тело ответа в apm
    """
    
    def __init__(self, get_response: Callable):
        self.get_response = get_response
        self._client = elasticapm.get_client()
    """
    Этот метод является конструктором класса. Он принимает один аргумент get_response, который является вызываемым объектом (функцией), 
    обрабатывающим запросы. Конструктор также инициализирует клиента Elastic APM, который будет использоваться для мониторинга.
    """
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        transaction_name = self._create_transaction_name(request)
        self._start_new_transaction(transaction_name)
        response = self.get_response(request)
        self._set_response_body_for_apm(response)
        return response
    """
    Этот метод делает экземпляр класса вызываемым. Он:

    1.Создает имя транзакции на основе запроса.
    2.Запускает новую транзакцию с созданным именем.
    3.Передает запрос следующему компоненту в цепочке промежуточного ПО и получает ответ.
    4.Устанавливает тело ответа в контексте APM.
    5.Возвращает ответ.
    """
    
    def _start_new_transaction(self, transaction_name: str) -> None:
        elasticapm.instrument()
        self._client.begin_transaction("request")
        elasticapm.set_transaction_name(transaction_name)
    """
    1.Инициализирует инструменты для мониторинга.
    2.Начинает новую транзакцию типа "request".
    3.Устанавливает имя транзакции для текущего запроса.
    """
    
    def _set_response_body_for_apm(self, response: HttpResponse) -> None:
        try:
            response_body_unicode = response.content.decode("utf-8")
            response_body = json.loads(response_body_unicode)
        except json.JSONDecodeError:
            response_body = response.content
        except AttributeError:
            response_body = ""
        elasticapm.set_context(data={"response_body": response_body})
    """
    1.Пытается декодировать тело ответа как строку UTF-8 и загрузить его как JSON.
    2.Если это не удается (исключение JSONDecodeError), сохраняет тело ответа как есть.
    3.Если тело ответа не установлено (исключение AttributeError), устанавливает тело ответа как пустую строку.
    4.Добавляет тело ответа в контекст APM.
    """
    
    def _create_transaction_name(self, request: HttpRequest) -> str:
        try:
            current_url = resolve(request.path_info).route
        except Resolver404:
            current_url = request.path

        return f"{request.method} {current_url}"
    """
    1.Пытается разрешить текущий путь запроса и получить маршрут.
    2.Если разрешение не удается (исключение Resolver404), использует исходный путь запроса.
    3.Возвращает строку, содержащую метод запроса (например, GET, POST) и маршрут.
    """
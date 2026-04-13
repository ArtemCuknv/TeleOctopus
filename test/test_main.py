import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app, RenderResponse


@pytest.fixture
def client():
    """Создает тестовый клиент для FastAPI приложения."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_database():
    """Мок для модуля database."""
    with patch('app.main.database') as mock:
        yield mock


@pytest.fixture
def mock_bot():
    """Мок для модуля bot."""
    with patch('app.main.bot') as mock:
        mock.bot_info = AsyncMock()
        yield mock


class TestPublicIndex:
    """Тесты для эндпоинта главной страницы."""

    def test_public_index_returns_html(self, client):
        """Тест проверяет, что главная страница возвращает HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAddBotGet:
    """Тесты для GET /add_bot."""

    def test_get_add_bot_returns_html(self, client):
        """Тест проверяет, что страница добавления бота возвращает HTML."""
        response = client.get("/add_bot")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestSendMessage:
    """Тесты для GET /send_message."""

    def test_get_send_message_returns_html(self, client):
        """Тест проверяет, что страница отправки сообщения возвращает HTML."""
        response = client.get("/send_message")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestSendText:
    """Тесты для POST /send_text."""

    def test_send_text_success(self, client, mock_bot):
        """Тест успешной отправки сообщения."""
        mock_bot.send_message_in_channel = AsyncMock()

        payload = {
            "api_id": "123456",
            "api_hash": "test_api_hash",
            "token": "test_token",
            "chat_id": 123456,
            "message": {"text": "Test message"}
        }

        response = client.post("/send_text", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        mock_bot.send_message_in_channel.assert_called_once()
        call_kwargs = mock_bot.send_message_in_channel.call_args.kwargs
        assert call_kwargs["api_id"] == 123456
        assert call_kwargs["api_hash"] == "test_api_hash"
        assert call_kwargs["bot_token"] == "test_token"
        assert call_kwargs["chat_id_channel"] == 123456
        assert call_kwargs["message"] == {"text": "Test message"}

    def test_send_text_error(self, client, mock_bot):
        """Тест обработки ошибки при отправке сообщения."""
        mock_bot.send_message_in_channel = AsyncMock(side_effect=Exception("Test error"))

        payload = {
            "api_id": "123456",
            "api_hash": "test_api_hash",
            "token": "test_token",
            "chat_id": 123456,
            "message": {"text": "Test message"}
        }

        response = client.post("/send_text", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "Internal Server Error" in data["error"]


class TestAddBotGetEndpoint:
    """Тесты для GET /add_bot (response_model)."""

    def test_get_add_bot_with_form(self, client):
        """Тест GET /add_bot с параметром token (возвращает HTML)."""
        response = client.get("/add_bot", params={"token": "test_token"})

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_get_add_bot_error_handling(self, client):
        """Тест обработки ошибки в GET /add_bot."""
        response = client.get("/add_bot", params={"token": "test_token"})

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestInitDb:
    """Тесты для GET /init_db."""

    def test_init_db_success(self, client, mock_database):
        """Тест успешной инициализации БД."""
        mock_database.create_db = AsyncMock()

        response = client.get("/init_db")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        mock_database.create_db.assert_called_once()

    def test_init_db_error(self, client, mock_database):
        """Тест обработки ошибки при инициализации БД."""
        mock_database.create_db = AsyncMock(side_effect=Exception("DB error"))

        response = client.get("/init_db")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "Internal Server Error" in data["error"]


class TestAddBotPost:
    """Тесты для POST /add_bot_post."""

    def test_add_bot_post_success(self, client, mock_database):
        """Тест успешного добавления бота."""
        mock_database.add_bot = AsyncMock()

        response = client.post("/add_bot_post", data={
            "token": "test_token",
            "api_id": "123456",
            "api_hash": "test_api_hash"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        mock_database.add_bot.assert_called_once()
        call_kwargs = mock_database.add_bot.call_args.kwargs
        assert call_kwargs["token"] == "test_token"
        assert call_kwargs["api_id"] == 123456
        assert call_kwargs["api_hash"] == "test_api_hash"

    def test_add_bot_post_error(self, client, mock_database):
        """Тест обработки ошибки при добавлении бота."""
        mock_database.add_bot = AsyncMock(side_effect=Exception("Add bot error"))

        response = client.post("/add_bot_post", data={
            "token": "test_token",
            "api_id": "123456",
            "api_hash": "test_api_hash"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert "Internal Server Error" in data["error"]


class TestRenderResponse:
    """Тесты для модели RenderResponse."""

    def test_render_response_success(self):
        """Тест создания успешного ответа."""
        response = RenderResponse(status="ok")
        assert response.status == "ok"
        assert response.error is None

    def test_render_response_with_error(self):
        """Тест создания ответа с ошибкой."""
        response = RenderResponse(status="error", error="Some error")
        assert response.status == "error"
        assert response.error == "Some error"

    def test_render_response_with_dict_error(self):
        """Тест создания ответа с ошибкой в виде dict."""
        error_dict = {"code": 500, "message": "Internal error"}
        response = RenderResponse(status="error", error=error_dict)
        assert response.status == "error"
        assert response.error == error_dict


class TestMetricsEndpoint:
    """Тесты для эндпоинта метрик."""

    def test_metrics_endpoint_exists(self, client):
        """Тест проверки доступности эндпоинта метрик."""
        response = client.get("/metrics")
        assert response.status_code == 200


class TestDocsEndpoint:
    """Тесты для эндпоинта документации."""

    def test_docs_endpoint_exists(self, client):
        """Тест проверки доступности Swagger документации."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestOpenApiEndpoint:
    """Тесты для эндпоинта OpenAPI спецификации."""

    def test_openapi_endpoint_exists(self, client):
        """Тест проверки доступности OpenAPI спецификации."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "info" in data
        assert data["info"]["title"] == "TeleOctopus API"
        assert data["info"]["version"] == "0.1"

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str
    africas_talking_username: str
    africas_talking_api_key: str
    test_phone_number: str
    # Event bus (RabbitMQ -> Node socket server)
    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    rabbitmq_exchange: str = "resume.events"
    # Database
    db_connection_str: str

    @property
    def async_db_url(self) -> str:
        """Same DB_CONNECTION_STR, rewritten for the asyncpg driver."""
        url = self.db_connection_str
        for prefix in ("postgresql://", "postgres://"):
            if url.startswith(prefix):
                return "postgresql+asyncpg://" + url[len(prefix):]
        return url

"""Application configuration.

Cross-cutting concern allowed outside the 4-layer Clean Architecture. Injected
into `infrastructure` and `presentation` only — never imported from `domain`
or `application`.
"""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    name: str = "Admirable"
    env: str = "production"
    debug: bool = False
    secret_key: str = Field(min_length=32)
    base_url: str = "http://localhost"
    locale: str = "en"


class DbSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 3306
    user: str = "root"
    password: str = ""
    database: str = "admirable"
    pool_size: int = 10

    @property
    def dsn(self) -> str:
        return (
            f"mysql+asyncmy://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )


class RedisSettings(BaseModel):
    url: str = "redis://127.0.0.1:6379/0"


class TtsSettings(BaseModel):
    voice: str = "en-US-AriaNeural"
    rate: str = "+0%"
    volume: str = "+0%"
    pitch: str = "+0Hz"
    max_chars_per_chunk: int = 3000


class MediaSettings(BaseModel):
    root: str = "media"
    url_prefix: str = "/media/"


class SessionSettings(BaseModel):
    cookie_name: str = "admirable_session"
    lifetime_seconds: int = 7200
    secure: bool = True


class MailSettings(BaseModel):
    driver: str = "log"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    from_address: str = "noreply@admirable.site"
    from_name: str = "Admirable"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        extra="ignore",
    )

    app: AppSettings
    db: DbSettings = Field(default_factory=DbSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    tts: TtsSettings = Field(default_factory=TtsSettings)
    media: MediaSettings = Field(default_factory=MediaSettings)
    session: SessionSettings = Field(default_factory=SessionSettings)
    mail: MailSettings = Field(default_factory=MailSettings)


def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]

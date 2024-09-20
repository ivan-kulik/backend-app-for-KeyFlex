from pydantic import BaseModel, PostgresDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class APIPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"
    users: str = "/users"
    stats: str = "/stats"
    profiles: str = "/profiles"

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.auth, "/jwt", "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class S3Config(BaseModel):
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str
    bucket_url: str


class StatsAmountConfig(BaseModel):
    modes_stats: int = 75
    last_sessions_stats: int = 10


class AccessToken(BaseModel):
    secret_key: str
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class GoogleOAuth2Config(BaseModel):
    GOOGLE_OAUTH_CLIENT_ID: str
    GOOGLE_OAUTH_CLIENT_SECRET: str


class EmailVerificationConfig(BaseModel):
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    api: APIPrefix = APIPrefix()
    db: DatabaseConfig
    s3: S3Config
    amount_of_stats: StatsAmountConfig = StatsAmountConfig()
    access_token: AccessToken
    google_oauth2: GoogleOAuth2Config
    email_verification: EmailVerificationConfig


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CONNECT_MCP_")
    
    aws_region: str = "us-west-2"
    aws_profile: str | None = None
    cache_ttl: int = 300
    rate_limit_rpm: int = 100


settings = Settings()

from pydantic import BaseModel, Field, constr


class LoggerCfg(BaseModel):
    enable: bool
    path: str
    level: constr(to_upper=True)
    encoding: str
    rotation: str
    retention: str
    compression: str
    format_: str = Field(alias="format")


class UvicornCfg(BaseModel):
    host: str
    port: int
    log_level: str


class Cfg(BaseModel):
    logger: LoggerCfg | None = None
    uvicorn: UvicornCfg

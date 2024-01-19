from __future__ import annotations
from functools import cached_property, lru_cache
from pathlib import Path
from typing import Annotated, Any, Type
from fastapi import Depends

from pydantic import (
    Field,
    DirectoryPath,
    FilePath,
    SecretStr,
    ValidationError,
    ValidationInfo,
    ValidatorFunctionWrapHandler,
    WrapValidator,
    computed_field,
)
from pydantic_settings import BaseSettings

ROOT_DIRECTORY = Path(__file__).parent.resolve()


def _create_dir_if_able(
    v: Any, handler: ValidatorFunctionWrapHandler, info: ValidationInfo
) -> DirectoryPath:
    try:
        path_dir = handler(v)
    except ValidationError:
        path_v = Path(v)
        # Means this is a path, but not a directory, raise an error
        assert not path_v.exists(), "working_dir must be a directory"
        path_v.mkdir()
        path_dir = handler(v)

    return path_dir


DataDirectory = Annotated[DirectoryPath, WrapValidator(_create_dir_if_able)]


class ClaimsApiConfig(BaseSettings):
    claims_data_dir: DirectoryPath = "/opt/claims-api"
    claims_database_name: str = "claims.db"
    claims_json_name: str = "claims.json"
    claims_table_name: str = "claims"

    jwt_private_key_path: FilePath = Field(f"/var/secrets/jwt_key")
    jwt_public_key_path: FilePath = Field(f"/var/jwt_key.pub.pem")

    api_host: str = "0.0.0.0"
    api_port: int = 8080
    api_prefix: str = "/api"
    api_audience: str = "claims.imx.com"

    @computed_field
    @property
    def claims_database_path(self) -> DirectoryPath:
        return self.claims_data_dir.joinpath(self.claims_database_name)

    @computed_field
    @property
    def claims_json_path(self) -> DirectoryPath:
        return self.claims_data_dir.joinpath(self.claims_json_name)

    @computed_field
    @cached_property
    def jwt_public_key(self) -> str:
        with open(self.jwt_public_key_path, "r") as pub_key_file:
            pub_key = pub_key_file.read()
        return pub_key

    @computed_field
    @cached_property
    def jwt_private_key(self) -> SecretStr:
        with open(self.jwt_private_key_path, "r") as private_key_file:
            private_key = private_key_file.read()
        return SecretStr(private_key)

    @classmethod
    @lru_cache
    def get_api_config(cls: Type[ClaimsApiConfig]) -> ClaimsApiConfig:
        return cls()


config_dependancy = Depends(ClaimsApiConfig.get_api_config)
AppConfigDependancy = Annotated[ClaimsApiConfig, config_dependancy]

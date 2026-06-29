import re

from pydantic import BaseModel, field_validator, model_validator


class PasswordMixin(BaseModel):
    password: str
    confirm_password: str

    @classmethod
    @field_validator("password")
    def validate_password(cls, pwd: str):
        pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]).{8,}$'
        )
        if not pattern.match(pwd):
            raise ValueError(
                "Password must contain lowercase and uppercase letters, numbers and special characters."
            )
        return pwd

    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match.")
        return self


class PasswordOptionalMixin(BaseModel):
    password: str | None = None
    confirm_password: str | None = None

    @classmethod
    @field_validator("password")
    def validate_password(cls, pwd: str | None):
        if pwd is None:
            return pwd
        pattern = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_\-+=\[\]{};:\'",.<>?/\\|`~]).{8,}$'
        )
        if not pattern.match(pwd):
            raise ValueError(
                "Password must contain lowercase and uppercase letters, numbers and special characters."
            )
        return pwd

    @model_validator(mode="after")
    def validate_confirm_password(self):
        if self.password is not None and self.confirm_password is not None:
            if self.password != self.confirm_password:
                raise ValueError("Passwords don't match.")
        return self

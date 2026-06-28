import re

from pydantic import BaseModel, model_validator, field_validator


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

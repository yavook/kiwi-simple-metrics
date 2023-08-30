from pydantic import BaseModel


class SubModel(BaseModel):
    optional: int = 42
    required: str


class Settings(BaseModel):
    sub: SubModel = SubModel(required="foo")
    sub2: SubModel = SubModel(required="bar")


def main() -> None:
    settings = Settings.model_validate({
        "sub": {"optional": "69"},
    })

    # settings = Settings()

    print(settings.model_dump())


if __name__ == "__main__":
    main()

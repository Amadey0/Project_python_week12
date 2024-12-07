import os
from dataclasses import dataclass
import api.api_keys


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def getenv(var_name: str, cast_to=str) -> str:
    try:
        value = os.environ[var_name]
        return cast_to(value)
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"The value {value} can't be cast to {cast_to}")






@dataclass
class AccuWeatherAPI:
    api_key: str
    location_url: str
    weather_url: str


@dataclass
class Config:
    api: AccuWeatherAPI


def load_config() -> Config:
    load_dotenv()
    config = Config(
        api=AccuWeatherAPI(
            api_key=getenv("API_KEY"),
            location_url=getenv("LOCATION_URL"),
            weather_url=getenv("WEATHER_URL"),
            ),
    )
    return config


config = load_config()

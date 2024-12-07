from flask import Blueprint, render_template, request
from requests.exceptions import HTTPError, InvalidJSONError

from src.services.weather import weather


index_page = Blueprint('index_page', __name__,
                        template_folder='src/templates')


@index_page.route("/", methods=["GET"])
def index_get():
    return render_template("index.html")


@index_page.route("/", methods=["POST"])
def index_post():
	start_location = request.form.get("start_location")
	end_location = request.form.get("end_location")

	if not start_location or not end_location:
		return render_template("index.html", error="Both locations are required")

	try:
		start_weather = weather.get_weather(start_location)
		end_weather = weather.get_weather(end_location)
	except HTTPError:
		return render_template("index.html", error="Wrong request to API service")
	except InvalidJSONError:
		return render_template("index.html", error="No json in API response or another error")

	weather_data = {
		"start_location": start_weather["text"],
		"end_location": end_weather["text"],
		"conditions": f"Start: wind speed - {start_weather['wind']}, {start_weather['temperature']}°C | "
						f"End: wind speed - {end_weather['wind']}, {end_weather['temperature']}°C"
	}

	return render_template("index.html", weather_data=weather_data)

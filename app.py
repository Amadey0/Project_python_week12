from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 'ваш_API_ключ'  # Замените на ваш ключ

@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    
    url = f'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={API_KEY}&q={latitude},{longitude}&language=ru'
    response = requests.get(url)
    
    if response.status_code == 200:
        location_key = response.json()['Key']
        weather_url = f'http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&language=ru&metric=true'
        weather_response = requests.get(weather_url)
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()[0]
            return jsonify({
                'temperature': weather_data['Temperature']['Metric']['Value'],
                'humidity': weather_data['RelativeHumidity'],
                'wind_speed': weather_data['Wind']['Speed']['Metric']['Value'],
                'precipitation_probability': weather_data['PrecipitationProbability']
            })
        else:
            return jsonify({'error': 'Не удалось получить данные о погоде'}), 500
    else:
        return jsonify({'error': 'Не удалось получить данные о местоположении'}), 500

if __name__ == '__main__':
    app.run(debug=True)
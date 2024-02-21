from flask import Flask, request, render_template
import WazeRouteCalculator
import logging

app = Flask(__name__)

logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_address = request.form['start_address']  
        end_address = request.form['end_address']
        start_lat = request.form['start_lat']
        start_lng = request.form['start_lng']
        end_lat = request.form['end_lat']
        end_lng = request.form['end_lng']
        avoid_tolls = 'avoid_tolls' in request.form
        region = 'EU'
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(
                f"{start_lat},{start_lng}",
                f"{end_lat},{end_lng}",
                region,
                avoid_toll_roads=avoid_tolls
            )
            route_info = route.calc_route_info()
            if route_info[0] >= 60:
                hours = int(route_info[0] / 60)
                minutes = int(route_info[0] % 60)
                result = f"De {start_address} à {end_address}, durée estimée: {hours}h{minutes:02d}, Distance: {route_info[1]} km"
            else:
                result = f"De {start_address} à {end_address}, durée estimée: {route_info[0]} minutes, Distance: {route_info[1]} km"
        except Exception as e:
            result = f"Erreur: {str(e)}"

        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

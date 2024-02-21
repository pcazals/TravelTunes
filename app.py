from flask import Flask, request, render_template
import WazeRouteCalculator
import logging

app = Flask(__name__)

# Configuration du logging
logger = logging.getLogger('WazeRouteCalculator.WazeRouteCalculator')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_lat = request.form['start_lat']
        start_lng = request.form['start_lng']
        end_lat = request.form['end_lat']
        end_lng = request.form['end_lng']
        region = 'EU'
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(f"{start_lat},{start_lng}", f"{end_lat},{end_lng}", region)
            route_info = route.calc_route_info()
            result = f"Durée estimée: {route_info[0]} minutes, Distance: {route_info[1]} km"
            print(result)        
        except Exception as e:
            result = f"Erreur: {str(e)}"
            print(result)
        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

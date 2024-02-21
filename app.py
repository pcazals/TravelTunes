from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import WazeRouteCalculator

app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    travel_time = None
    distance = None
    if request.method == 'POST':
        start_address = request.form.get('start_address')
        end_address = request.form.get('end_address')
        region = request.form.get('region', 'EU')
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(start_address, end_address, region)
            route_info = route.calc_route_info()
            travel_time = route_info[0]
            distance = route_info[1]
        except WazeRouteCalculator.WRCError as e:
            travel_time = e
    return render_template('index.html', travel_time=travel_time, distance=distance)

if __name__ == '__main__':
    app.run(debug=True)

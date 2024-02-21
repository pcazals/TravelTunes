from flask import Flask, render_template, request, jsonify
import WazeRouteCalculator
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate-route', methods=['POST'])
def calculate_route():
    from_address = request.form['from']
    to_address = request.form['to']
    avoid_tolls = 'avoidTolls' in request.form
    try:
        route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, 'FR')
        route_info = route.calc_route_info(avoid_tolls)
        return jsonify(route_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

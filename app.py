from flask import Flask, request, render_template
import WazeRouteCalculator

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_address = request.form['start_address']
        end_address = request.form['end_address']
        region = 'EU' 
        try:
            route = WazeRouteCalculator.WazeRouteCalculator(start_address, end_address, region)
            route_info = route.calc_route_info()
            result = f"Durée estimée: {route_info[0]} minutes, Distance: {route_info[1]} km"
        except Exception as e:
            result = f"Erreur: {str(e)}"
        
        return render_template('index.html', result=result)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)

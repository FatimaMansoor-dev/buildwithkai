from flask import Flask, render_template, request
import modules
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_estimated_budget', methods=['POST'])
def get_estimated_budget():
    # Get location from the request data
    data = request.get_json()
    location = data['location']
    
    # Call calculate_estimated_budget function from modules.py
    estimated_budget = modules.calculate_estimated_budget(location)
    return estimated_budget

@app.route('/hotels')
def display_hotels():
    return render_template('hotels.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/displayhotel')
def search_hotels():
    # Get the city from the query string
    city = request.args.get('city')
    details = modules.hotel_details(city)
    return render_template('displayhotels.html', hotel_details=details)

@app.route('/run_voicebot')
def run_voice():
    try:
        subprocess.run(['python', 'voicebot.py'])
        return 'Voicebot executed successfully'
    except Exception as e:
        return f'Error executing voicebot: {str(e)}'
    

@app.route('/generate_travel_plan', methods=['POST'])
def generate_plan():
    '''
    the function gets values of all parameters from input and calls generate
    plan method in modules.py

    return the entire plan
    '''
    
    data = request.get_json()
    src = data['location']
    interest = data['area']
    time = data['time']
    budget = data['budget']
    days = data['days']

    # Call the generate_travel_plan function from modules.py
    travel_plan = modules.generate_travel_plan(budget, days, src, interest, time)

    return travel_plan


if __name__ == '__main__':
    app.run()

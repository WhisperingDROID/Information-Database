from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/vehicle_table')
def vehicle_table():
    make = request.args.get('make')
    model = request.args.get('model')
    year = request.args.get('year')
    vin = request.args.get('vin')
    license = request.args.get('license')

    return render_template('table.html', make=make, model=model, year=year, vin=vin, license=license)

if __name__ == '__main__':
    app.run(debug=True, port=8000)

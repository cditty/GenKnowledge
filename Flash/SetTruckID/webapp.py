from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods = ['POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == 'password':
            return redirect(url_for('success'))
        else:
            return render_template('indexFail.html')

@app.route('/success/')
def success():
    return render_template('truckNbr.html')

/*@app.route('/recordTruck/', methods = ['POST'])
def recordTruck():
    if request.method == 'POST':
        if int(request.form['truckNbr']): # if number
            if len(str(request.form['truckNbr'])) == 4:
                truckNbr = request.form['truckNbr']

                # Need to move the backup file into place 
                # incase this pi was moved to a different truck
                myBackup = '/home/pi/gpsLocate/config.bak'
                myFile = '/home/pi/gpsLocate/config.ini'
                try:
                    with open(myBackup) as f:
                        data = f.read()
                    with open(myFile, 'w') as f:
                        f.write(data)
                except Exception e:
                    f = 'Error reading file: ' + str(e)

                # Time to setup pi for new truck
                try:
                    with open(myFile) as f:
                        data = f.read()
                        data = data.replace('9999', truckNbr)
                    with open(myFile, 'w') as f:
                        f.write(data)
                except Exception, e:
                    f = 'Error reading file: ' + str(e)

                return render_template('truckSuccess.html')
            else:
                return render_template('truckFail.html', error = 'Truck number too large or small.')
    
if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
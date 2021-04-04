from flask import *
import pickle
import numpy as np
import json

__model=None
__columns=None

app=Flask(__name__,template_folder='client/templates',static_folder='client/static')

@app.route('/')
def home():
    return render_template("home.html")

def predict_price(year,km_driven,location,transmission,fuel,owner_type,Brand):
    global __model
    global __columns
    
    if __columns==None:
        with open('model/columns.json','r') as f:
            __columns=json.load(f)['columns']
    if __model==None: 
        with open('model/used_car_price_model.pkl','rb') as file:
            __model=pickle.load(file)
    x=[]
    x=np.zeros(35)
    x[0]=year
    x[1]=km_driven
    location_index=np.where(__columns==location)[0]
    transmission_index=np.where(__columns==transmission)[0]
    fuel_index=np.where(__columns==fuel)[0]
    owner_index=np.where(__columns==owner_type)[0]
    brand_index=np.where(__columns==Brand)[0]
    if location_index>=0:
        x[location_index]=1
    if transmission_index>=0:
        x[transmission_index]=1
    if fuel_index>=0:
        x[fuel_index]=1
    if owner_index>=0:
        x[owner_index]=1
    if brand_index>=0:
        x[brand_index]=1
    return __model.predict([x])[0]

@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method=="POST":
        year=int(request.form['year'])
        km_driven=float(request.form['km_driven'])
        location=request.form['location']
        transmission=request.form['transmission']
        fuel=request.form['fuel']
        owner=request.form['owner']
        brand=request.form['brand']
        
        result={'year':year,'km_driven':km_driven,'location':location,'transmission':transmission,'fuel':fuel,'owner':owner,'brand':brand}
        test=int(predict_price(year,km_driven,location,transmission,fuel,owner,brand))
        return render_template('home.html',prediction="The Price of the car {}".format(test))
        
if __name__=="__main__":
    app.run(debug=True)
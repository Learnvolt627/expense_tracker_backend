from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #this is to diable the warning

#we will create a db object ot connect to the databse
db=SQLAlchemy(app)

#we create a class or model for the expenses 

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True)#unique identity for every expense
    title=db.Column(db.String(100), nullable=False) #name of expense (cant be blank)
    amount=db.Column(db.Float, nullable=False)
    cagtegory=db.Column(db.String(50), nullable=True) #category can be blank
    date=db.Column(db.DateTime , default=datetime.utcnow)#automatically sets the time
@app.route('/health')
def health():
    return {"status": "Api is running"}

if __name__=='__main__':

    #will check if the databse exits ; else create it 
    with app.app_context():
        db.create_all()
        print('database created')
    app.run(debug=True)
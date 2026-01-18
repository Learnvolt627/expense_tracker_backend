from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
from zoneinfo import ZoneInfo



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #this is to disable the warning

#we will create a db object ot connect to the databse
db=SQLAlchemy(app)

#we create a class or model for the expenses 

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True)#unique identity for every expense
    title=db.Column(db.String(100), nullable=False) #name of expense (cant be blank)
    amount=db.Column(db.Float, nullable=False)
    category=db.Column(db.String(50), nullable=True) #category can be blank
    date=db.Column(db.DateTime , default=lambda:datetime.now(ZoneInfo("Asia/Kolkata")))#automatically sets the time
@app.route('/health')
def health():
    return {"status": "Api is running"}
@app.route('/expenses', methods=['POST'])
def add_expenses():
    # get data from request 
    data=request.get_json()
    #create a new expense 
    new_expense=Expense(
        title=data['title'],
        amount=data['amount'],  
        category=data.get('category') #category is optional so get is safer as it can return none
    )

    #we add the new expense to the db and save
    db.session.add(new_expense)
    db.session.commit()

    return{'message': "expense added"} , 201
@app.route('/expenses', methods=['GET'])
def get_expenses():
    #fetch all expenses 
    expenses=Expense.query.all()
    output=[]
    # we covert all databse objects into list of dictionaries
    for expense in expenses:
        expense_data={
            'id':expense.id,
            'title':expense.title,
            'amount':expense.amount,
            'category':expense.category,
            'date':expense.date
        }
        output.append(expense_data)

    return {'expenses': output}, 200

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    #find the expnese with id 
    expense=Expense.query.get(id)
    if not expense:
        return {'message': 'expense not found'}, 404
    
    # get the new data from request 
    data=request.get_json()

    #update if the new info if provided
    if 'title' in data:
        expense.title=data['title']
    if 'amount' in data:
        expense.amount=data['amount']
    if 'category' in data:
        expense.category=data['category']

    #save changes
    db.session.commit()

    return {'message': 'expense updated'}, 200
@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    #find expnse with specific  id
    expense=Expense.query.get(id)

    #if it doesnt exist 
    if not expense:
        return {'message': 'expense not found'}, 404
    #delete the expense
    db.session.delete(expense)
    db.session.commit()

    return {'message': 'expense deleted'}, 200
        

if __name__=='__main__':

    #will check if the databse exits ; else create it 
    with app.app_context():
        db.create_all()
        print('database created')
    app.run(debug=True)
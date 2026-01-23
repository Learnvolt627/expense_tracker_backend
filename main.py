from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import render_template
from ledger import Blockchain, ExpenseBlock # we import both the classes we just made
from flask import jsonify






app=Flask(__name__)


my_ledger=Blockchain()

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

    transaction_data={
        'title': data['title'],
        'amount': data['amount'],
        'category':data.get('category')
    }


    block=my_ledger.add_expense(transaction_data)

    #add to blockchain ledger
    block= my_ledger.add_expense({
        'message': 'New expense added',
        'block_index': block.index,
        'hash': block.current_hash

    })

    #we add the new expense to the db and save
    db.session.add(new_expense)
    db.session.commit()

    return jsonify({
        'message': 'Expense added to ledger',
        'block_index': block.index,
        'hash': block.current_hash,
        'previous_hash': block.previous_hash
    }), 201





@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data=[]
    for block in my_ledger.chain:
        chain_data.append({
            'index': block.index,
            'expense_data': block.expense_data,
            'timestamp': block.timestamp,
            'previous_hash': block.previous_hash,
            'current_hash': block.current_hash
        })
    return jsonify({'length': len(chain_data), 'chain': chain_data}), 200

@app.route('/verify_ledger', methods=['GET'])
def verify_ledger():
    is_valid=my_ledger.is_chain_valid()
    
    if is_valid:
        return jsonify({'status':'Secure' , 'message': 'Ledger is valid'})
    else:
        return jsonify({'status':'Corrupted', 'message': "Tampering detected" })
    
    


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

#temporary code to hack the ledger
@app.route('/hack_ledger',methods=['GET'])
def hack_ledger():
    if len(my_ledger.chain)>1:
        my_ledger.chain[1].expense_data['amount']=6666666
        return jsonify({'message': 'Ledger hacked!'}), 200
    return jsonify({'message': 'Not enough blocks to hack!'}), 400
@app.route('/')
def home():
    return render_template('index.html')
        

if __name__=='__main__':

    #will check if the databse exits ; else create it 
    with app.app_context():
        db.create_all()
        print('database created')
    app.run(debug=True, host='0.0.0.0')
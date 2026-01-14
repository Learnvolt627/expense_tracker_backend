from flask import Flask, request
import sqlite3
app =Flask(__name__)

@app.route('/health')
def health():
    return {'status': 'Yashvardhan'}


@app.route('/expenses',methods=['POST','GET'])
def expenses():
        conn=sqlite3.connect('expenses.db')
        cursor=conn.cursor()

        if request.method=='POST':
            data=request.get_json()

            cursor.execute('insert into expenses (amount, category,date) values(?,?,?)',(data["amount"],data["category"],data["date"]))
            conn.commit()

    
    
       
        cursor.execute('select * from expenses')
        all_expenses=cursor.fetchall()
        results=[]
        for expense in all_expenses:
             results.append({
                    'id':expense[0],
                    'amount':expense[1],
                    'category':expense[2],
                    'date':expense[3]
             }
                  
             )
        return results
        
        
        
    
    




def init_db():
    # we coonect to the database
    conn=sqlite3.connect('expenses.db')
    cursor=conn.cursor()
    # we create teh expenses table if it does not exit
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL
        
    )
    ''')

    #save changes and close 
    conn.commit()
    conn.close()
init_db()

if __name__=='__main__':
    app.run(debug=True)
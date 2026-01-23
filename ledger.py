import hashlib
import json
from datetime import datetime
import os

class ExpenseBlock:
    def __init__(self, index, expense_data, previous_hash, timestamp=None):
        self.index =index
        self.expense_data= expense_data
        self.previous_hash=previous_hash
        self.timestamp=timestamp or str(datetime.now())
        self.current_hash=self.calculate_hash()

    #fucntion to calculate hash
    def calculate_hash(self):
        #we will dump the date into a string so we can hash it 
        #also the requirements are that sor_keys is true , {a:1, b:2} and {b:2, a:1} are same 

        block_string=json.dumps(self.__dict__, sort_keys=True, default=str).encode()

        # this will create the "diigital fingerprint"

        return hashlib.sha256(block_string).hexdigest()
    
    #to convert this into dictionary 
    def to_dict(self):
        return {
            'index': self.index,
            'expense_data': self.expense_data,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
        }


class Blockchain:
    def __init__(self):
        self.chain=[]
        self.file_path='chain_data.json'
        self.create_genesis_block() #the first block with no previous hash

    def create_genesis_block(self):
        genesis_block=ExpenseBlock(0, "Genesis Block", "0")
        self.chain.append(genesis_block)
        self.save_chain()

    def load_chain(self):
        


    def save_chain(self):    

    def add_expense(self, expense_data):
        last_block=self.chain[-1]


        #we create a new block which will also store the last block's hash
        new_block=ExpenseBlock(
            index=len(self.chain),
            expense_data=expense_data,
            previous_hash=last_block.current_hash
        )

        self.chain.append(new_block)
        return new_block
    

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current=self.chain[i]
            previous=self.chain[i-1]


            #first we check if someone modified the current block's data

            if current.current_hash != current.calculate_hash():
                return False
            
            #if the block's previous hash is not equal to the previous block's current hash
            if current.previous_hash != previous.current_hash:
                return False
    
        return True
from web3 import Web3

class Student:
    def __init__(self, id, name, age, courses):
        self.id = id
        self.name = name
        self.age = age
        self.courses = courses

import hashlib

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode('utf-8')).hexdigest()

import time

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def add_block(self, data):
        new_block = Block(len(self.chain), time.time(), data, self.chain[-1].hash)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
def main():
    student_blockchain = Blockchain()

    student1 = Student("001", "Alice", 20, ["Math", "Physics"])
    student_blockchain.add_block(student1.__dict__)

    student2 = Student("002", "Bob", 22, ["Chemistry", "Biology"])
    student_blockchain.add_block(student2.__dict__)

    print("Blockchain valid?", student_blockchain.is_valid())

if __name__ == "__main__":
    main()

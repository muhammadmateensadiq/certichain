import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_certificates = []

        # Create the genesis block
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'certificates': self.pending_certificates,
            'proof': proof,
            'previous_hash': previous_hash,
        }
        self.pending_certificates = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_val = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        for index in range(1, len(chain)):
            block = chain[index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_val = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_val[:4] != '0000':
                return False
            previous_block = block
        return True

    def add_certificate(self, student_name, course, grade):
        self.pending_certificates.append({
            'student': student_name,
            'course': course,
            'grade': grade,
            'timestamp': time()
        })
        return self.get_previous_block()['index'] + 1

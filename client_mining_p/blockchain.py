# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib # hash library -> SHA-256 hash
import json
from time import time
from uuid import uuid4 # uuid -> universally unique identifier

from flask import Flask, jsonify, request # flask is for backend


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            # TODO
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]), # this hashes the last block unless we've provided a previous hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the block to the chain
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        # TODO: Create the block_string
        string_object = json.dumps(block, sort_keys=True) # stringifies json
        block_string = string_object.encode() # encode -> turns it into a byte string (gives a raw string)

        # TODO: Hash this string using sha256
        hash_object = hashlib.sha256(block_string)
        # create a string of hexidecimal characters
        hash_string = hash_object.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hash_string

    @property # decorator -> makes the function a property
    def last_block(self):
        return self.chain[-1]

    # Remove the `proof_of_work` function from the server.
    # def proof_of_work(self, block):
    #     """
    #     Simple Proof of Work Algorithm
    #     Stringify the block and look for a proof.
    #     Loop through possibilities, checking each one against `valid_proof`
    #     in an effort to find a number that is a valid proof
    #     :return: A valid proof for the provided block
    #     """
    #     # TODO
    #     # stringify the block
    #     block_string = json.dumps(block, sort_keys=True)
    #     # find proof
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         # increment proof
    #         proof += 1
    #     return proof

    @staticmethod # decorator -> run it without an instance - dont need to substantiate a blockchain
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        # use SHA-256 hash for 2 completely distinct and seperate tasks: 1. validate the chain, 2. proof of work
        # get the hash in one number
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # Change `valid_proof` to require *6* leading zeroes.
        return guess_hash[:6] == '0' * 6


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
# print(blockchain.chain)
# print(blockchain.hash(blockchain.last_block))


#  Modify the `mine` endpoint to instead receive and validate or reject a new proof sent by a client.
    # * It should accept a POST
    # * Use `data = request.get_json()` to pull the data out of the POST
    #     * Note that `request` and `requests` both exist in this project
    # * Check that 'proof', and 'id' are present
    #     * return a 400 error using `jsonify(response)` with a 'message'
# * Return a message indicating success or failure.  Remember, a valid proof should fail for all senders except the first.
@app.route('/mine', methods=['POST'])
def mine():
    # pull the data out of the POST
    data = request.get_json()
    req_prop = ['id', 'proof']
    # print(data)
    # string_object = json.dumps(blockchain.last_block, sort_keys=True)

    # Check that 'proof', and 'id' are present
    if all(keys in data for keys in req_prop):
        string_object = json.dumps(blockchain.last_block, sort_keys=True)

        if blockchain.valid_proof(string_object, data['proof']):
            previous_hash = blockchain.hash(blockchain.last_block)
            block = blockchain.new_block(data['proof'], previous_hash)

            response = {
                'message': 'SUCCESS: New Block Forged',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }
            return jsonify(response), 200
        else:
            response = {'message': 'FAILURE: Proof is invalid or already submitted'}
    else:
        response = {'message': 'FAILURE: Must submit proof and id'}

    return jsonify(response), 400

# @app.route('/mine', methods=['GET'])
# def mine():
#     # Run the proof of work algorithm to get the next proof
#     proof = blockchain.proof_of_work(blockchain.last_block)

#     # Forge the new Block by adding it to the chain with the proof
#     # get previous hash
#     previous_hash = blockchain.hash(blockchain.last_block)
#     new_block = blockchain.new_block(proof, previous_hash) # save in variable new_block

#     response = {
#         # TODO: Send a JSON response with the new block
#         # return variable new_block
#         'block': new_block
#     }

#     return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

# Add an endpoint called `last_block` that returns the last block in the chain
@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        # Return the last block in the chain
        'last_block': blockchain.last_block,
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
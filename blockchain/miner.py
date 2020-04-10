import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last five digits of hash(p) are equal
    to the first five digits of hash(p')
    - IE:  last_hash: ...AE912345, new hash 12345888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")

    proof = random.randrange(0, 16**5)
    encoded_proof = str(last_proof).encode()
    last_proof_hash = hashlib.sha256(encoded_proof).hexdigest()

    while valid_proof(last_proof_hash, proof) is False:
        proof += 1

    end = timer()
    print(f"{end - start} seconds to find proof")
    return proof

    print("Proof found: " + str(proof) + " in " + str(timer() - start))


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last five characters of
    the hash of the last proof match the first five characters of the hash
    of the new proof?

    IE:  last_hash: ...AE912345, new hash 12345E88...
    """

    guess = str(proof).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return last_hash[-5:] == guess_hash[:5]


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))

import time
import hashlib
from py_ecc.bls import G2ProofOfPossession as BLS
from web3 import Web3
import json

# BLS12-381 curve order
BLS12_381_ORDER = 0x73eda753299d7d483339d80809a1d80553bda402fffe5bfeffffffff00000001

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    raise Exception("Failed to connect to Ganache at http://127.0.0.1:8545")

# Load contract ABI and address
with open('/home/kalp-77/Desktop/bct/build/contracts/UserRequestContract.json') as f:
    user_request_abi = json.load(f)['abi']

with open('/home/kalp-77/Desktop/bct/build/contracts/ResourceResponseContract.json') as f:
    resource_response_abi = json.load(f)['abi']

user_request_address = '0x4dD6d803630D9a4C7395E8FbC99F39aa968e8DD6'
resource_response_address = '0x1e91354EC4C0DCba61D92E7cdA65f800a2940bCA'

user_request_contract = w3.eth.contract(address=user_request_address, abi=user_request_abi)
resource_response_contract = w3.eth.contract(address=resource_response_address, abi=resource_response_abi)

# Simulate consumer submission
def simulate_request(consumer_idx, account, private_key):
    vm_specs = f"2vCPU-4GB-RAM-{consumer_idx}"
    duration = 60  # seconds
    try:
        tx = user_request_contract.functions.submitRequest(vm_specs, duration).build_transaction({
            'from': account,
            'nonce': w3.eth.get_transaction_count(account),
            'gas': 3000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Consumer {consumer_idx} submitted request. Tx Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Error submitting request for consumer {consumer_idx}: {e}")

# Simulate BLS signature aggregation
def simulate_response(request_id, messages, private_keys, account, private_key):
    try:
        signatures = [BLS.Sign(sk, msg.encode()) for sk, msg in zip(private_keys, messages)]
        aggregated_signature = BLS.Aggregate(signatures)
        signer_ids = list(range(len(private_keys)))
        encrypted_data = b"dummy_data"  # Placeholder
        tx = resource_response_contract.functions.postResponse(
            request_id, encrypted_data, aggregated_signature, signer_ids
        ).build_transaction({
            'from': account,
            'nonce': w3.eth.get_transaction_count(account),
            'gas': 3000000,
            'gasPrice': w3.to_wei('20', 'gwei')
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Posted response for request {request_id}. Tx Hash: {tx_hash.hex()}")
    except Exception as e:
        print(f"Error posting response for request {request_id}: {e}")

def run_simulation(num_consumers, latency):
    print(f"Simulating with {num_consumers} consumers, inter-CSP latency {latency}")
    
    # Generate BLS private keys within valid range
    private_keys = [
        int.from_bytes(hashlib.sha256(str(i).encode()).digest(), 'big') % (BLS12_381_ORDER - 1) + 1
        for i in range(num_consumers)
    ]
    
    # Generate public keys (for logging)
    public_keys = [BLS.SkToPk(sk) for sk in private_keys]
    print(f"Generated {len(public_keys)} BLS public keys")
    
    # Use a single account and private key from Ganache
    account = '0x8d16C10105B80D33E24F87574BAC3f1819fB7032'
    private_key = '0x7b87de9a0290f8066d35eb59347cec9dd352325181a055c43afedd95ff555a5d'
    
    # Submit requests
    for i in range(num_consumers):
        simulate_request(i, account, private_key)
        time.sleep(1)  # Delay for pacing
    
    # Simulate responses with BLS aggregation
    messages = [f"Response_{i}" for i in range(num_consumers)]
    simulate_response(0, messages[:num_consumers], private_keys, account, private_key)

if __name__ == '__main__':
    NUM_CONSUMERS = 4
    LATENCY = '50ms'
    run_simulation(NUM_CONSUMERS, LATENCY)


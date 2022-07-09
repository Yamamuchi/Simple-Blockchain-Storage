from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# For connecting to Rinkeby testnet
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/fe053d003e4d4e0ead43423d6fd2acab")
)
chain_id = 4
my_address = "0x74cacf6c42f4B7fd04BC447F9feCBE21A889508e"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

# Create the contract in Python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# 1. Build a transaction

# 2. Sign a transaction

# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# Working with the contract, always need
# Contract address
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call -> Simulate making the call and getting a return value (calls don not make a state change)
# Transact -> Actually make a state change

# Initial value of favourite number
print(f"Initial value: {simple_storage.functions.retrieve().call()}")
print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Contract updated!")

print(f"Updated value: {simple_storage.functions.retrieve().call()}")

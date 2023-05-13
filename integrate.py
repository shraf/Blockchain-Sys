from web3 import Web3

# Connect to the local Ganache network
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Contract ABI (Application Binary Interface)
abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"addBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"_data","type":"string"}],"name":"addTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_address","type":"address"},{"internalType":"uint256","name":"_stake","type":"uint256"}],"name":"addValidator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"blocks","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"uint256","name":"timestamp","type":"uint256"},{"internalType":"bytes32","name":"previousHash","type":"bytes32"},{"internalType":"bytes32","name":"hash","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"blockIndex","type":"uint256"}],"name":"getBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"string[]","name":"","type":"string[]"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"selectValidatorIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"transactionsPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"validators","outputs":[{"internalType":"address","name":"validatorAddress","type":"address"},{"internalType":"uint256","name":"stake","type":"uint256"},{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"}]
# Contract address
contract_address = "0x392c7a4B925EAdC2a07522659281eC0154E879Dc"

# Create a contract instance
contract = w3.eth.contract(address=contract_address, abi=abi)
# Account address to send the transaction (replace with your own address)
account_address = '0x5363d85330B75d990f3a97bF8E79083aBd0BEC76'

# Private key of the account (replace with your own private key)
private_key = '0xfef8a2b9aa857710f3637fb9d0f0a2146586244cce49609bd5d08a10f4222ca9'


# Get the number of validators
for i in range(16):
    function_call=contract.functions.addTransaction('sharaf'+str(i)).build_transaction({
    'from': account_address,
    'nonce': w3.eth.get_transaction_count(account_address),
    'gas': 2000000,  # Adjust the gas limit according to your contract's needs
    'gasPrice': w3.to_wei('50', 'gwei')  # Adjust the gas price according to your preferences
            })

    # Sign the transaction
    signed_txn = w3.eth.account.sign_transaction(function_call, private_key=private_key)

    # Send the signed transaction
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

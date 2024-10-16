import argparse
import json
import os

from web3 import Web3

from compile import compile_contract
from deploy import deploy_contract

def execute_contract(contract_address, private_key, rpc_url, contract_name):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    with open(f"contracts/{contract_name}.json", "r") as file:
        compiled_sol = json.load(file)

    abi = compiled_sol['contracts'][f'{contract_name}.sol']['abi']
    
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    account = w3.eth.account.privateKeyToAccount(private_key)
    
    nonce = w3.eth.getTransactionCount(account.address)
    store_transaction = contract.functions.store(15).buildTransaction({
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": account.address,
        "nonce": nonce,
    })
    
    signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
    store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
    store_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
    
    stored_value = contract.functions.retrieve().call()
    print(f"Stored value: {stored_value}")

def main():
    parser = argparse.ArgumentParser(description="Compile, deploy, and execute Solidity contract")
    parser.add_argument("--action", choices=["compile", "deploy", "execute", "all"], default="execute", help="Action to perform")
    parser.add_argument("--contract", default="Demo001", help="Contract file name")
    parser.add_argument("--contract-address", default="0x0", help="Deployed contract address")

    args = parser.parse_args()

    rpc_url = 'http://127.0.0.1:8545'
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    private_key_file = os.path.join(os.path.dirname(base_dir), 'eth', 'data', 'accounts.json')
    with open(private_key_file, 'r') as private_key_file:
        private_key = json.load(private_key_file)[0]['private_key']
    
    if args.action == "compile" or args.action == "all":
        print("Compiling contract...")
        compiled_contract = compile_contract(args.contract)
        print("Contract compiled successfully.")
    
    if args.action == "deploy" or args.action == "all":
        print("Deploying contract...")
        contract_address = deploy_contract(args.contract, rpc_url, private_key)
        print(f"Contract deployed at: {contract_address}")
    
    if args.action == "execute" or args.action == "all":
        if not args.contract_address:
            print("Error: Contract address is required for execution.")
            return
        print("Executing contract...")
        execute_contract(args.contract_address, private_key, rpc_url, args.contract)

if __name__ == "__main__":
    main()

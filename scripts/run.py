import argparse
import json

from web3 import Web3

from compile import compile_contract
from deploy import deploy_contract

def execute_contract(contract_address, private_key, rpc_url):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    with open("compiled_code.json", "r") as file:
        compiled_sol = json.load(file)

    abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']
    
    contract = w3.eth.contract(address=contract_address, abi=abi)
    
    account = w3.eth.account.privateKeyToAccount(private_key)
    
    # 示例：调用合约的 store 函数
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
    
    # 调用合约的 retrieve 函数
    stored_value = contract.functions.retrieve().call()
    print(f"Stored value: {stored_value}")

def main():
    parser = argparse.ArgumentParser(description="Compile, deploy, and execute Solidity contract")
    parser.add_argument("action", choices=["compile", "deploy", "execute", "all"], help="Action to perform")
    parser.add_argument("--contract", default="SimpleStorage.sol", help="Contract file name")
    parser.add_argument("--private-key", help="Private key for deployment and execution")
    parser.add_argument("--rpc-url", help="RPC URL for the Ethereum network")
    parser.add_argument("--contract-address", help="Deployed contract address for execution")
    
    args = parser.parse_args()
    
    if args.action == "compile" or args.action == "all":
        print("Compiling contract...")
        compiled_contract = compile_contract(args.contract)
        print("Contract compiled successfully.")
    
    if args.action == "deploy" or args.action == "all":
        if not args.private_key or not args.rpc_url:
            print("Error: Private key and RPC URL are required for deployment.")
            return
        print("Deploying contract...")
        contract_address = deploy_contract(None, args.private_key, args.rpc_url)
        print(f"Contract deployed at: {contract_address}")
    
    if args.action == "execute" or args.action == "all":
        if not args.private_key or not args.rpc_url or not args.contract_address:
            print("Error: Private key, RPC URL, and contract address are required for execution.")
            return
        print("Executing contract...")
        execute_contract(args.contract_address, args.private_key, args.rpc_url)

if __name__ == "__main__":
    main()

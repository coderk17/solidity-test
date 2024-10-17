import argparse
import configparser
import json
import os

from web3 import Web3

from compile import compile_contract
from deploy import deploy_contract

config = configparser.ConfigParser()
config.read('config.ini')
rpc_url = config['ethereum']['rpc_url']
accounts_json_path = config['files']['accounts_json_path']

def execute_contract(private_key, contract_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    with open(os.path.join(base_dir, "data", "abi", f"{contract_name}.json"), "r") as file:
        abi = json.load(file)

    with open(os.path.join(base_dir, "data", "contracts", "contract_addresses.json"), "r") as file:
        contract_addresses = json.load(file)
    contract_address = contract_addresses[contract_name]
    
    contract = w3.eth.contract(address=contract_address, abi=abi)

    module_name = f"contracts.{contract_name}"
    module = __import__(module_name, fromlist=['call'])
    contract_class = getattr(module, contract_name)
    contract_instance = contract_class(w3, private_key)
    contract_instance.call(contract)

def main():
    parser = argparse.ArgumentParser(description="Compile, deploy, and execute Solidity contract")
    parser.add_argument("action", choices=["compile", "deploy", "execute", "all"], default="execute", help="Action to perform")
    parser.add_argument("contract", default="Demo001", help="Contract file name")
    args = parser.parse_args()

    with open(accounts_json_path, 'r') as accounts_file:
        accounts = json.load(accounts_file)
    private_key = accounts[0]['private_key']
    
    if args.action == "compile" or args.action == "all":
        compile_contract(args.contract)
    
    if args.action == "deploy" or args.action == "all":
        deploy_contract(args.contract, private_key)
    
    if args.action == "execute" or args.action == "all":
        execute_contract(private_key, args.contract)

if __name__ == "__main__":
    main()

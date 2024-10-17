import configparser
import json
import os

import argparse
from web3 import Web3

config = configparser.ConfigParser()
config.read('config.ini')
rpc_url = config['ethereum']['rpc_url']
accounts_json_path = config['files']['accounts_json_path']

def deploy_contract(contract_name, private_key):
    # 连接到以太坊网络
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    account = w3.eth.account.privateKeyToAccount(private_key)
    
    # 读取ABI和字节码
    base_dir = os.path.dirname(os.path.dirname(__file__))
    abi_path = os.path.join(base_dir, 'data', 'abi', f'{contract_name}.json')
    bytecode_path = os.path.join(base_dir, 'data', 'bytecode', f'{contract_name}.bin')

    with open(abi_path, 'r') as abi_file:
        abi = json.load(abi_file)
    
    with open(bytecode_path, 'r') as bytecode_file:
        bytecode = bytecode_file.read()

    # 创建合约对象
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # 获取nonce
    nonce = w3.eth.get_transaction_count(account.address)
    
    # 构建交易
    transaction = Contract.constructor().build_transaction({
        "chainId": w3.eth.chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": account.address,
        "nonce": nonce,
    })
    
    # 签名交易
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # 发送交易
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # 等待交易被确认
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"合约已部署到地址: {tx_receipt.contractAddress}")

    # 将部署地址保存到data/contracts/contract_addresses.json
    os.makedirs(os.path.join(base_dir, 'data', 'contracts'), exist_ok=True)
    contract_addresses_file = os.path.join(base_dir, 'data', 'contracts', 'contract_addresses.json')

    if os.path.exists(contract_addresses_file):
        with open(contract_addresses_file, 'r') as file:
            contract_addresses = json.load(file)
    else:
        contract_addresses = {}
    
    contract_addresses[contract_name] = tx_receipt.contractAddress
    
    with open(contract_addresses_file, 'w') as file:
        json.dump(contract_addresses, file)

    return tx_receipt.contractAddress

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="部署智能合约")
    parser.add_argument("contract_name", help="要部署的合约名称")
    args = parser.parse_args()

    with open(accounts_json_path, 'r') as accounts_file:
        accounts = json.load(accounts_file)

    deploy_contract(args.contract_name, accounts[0]['private_key'])

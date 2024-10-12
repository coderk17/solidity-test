import json
import os

import argparse
from web3 import Web3

def deploy_contract(contract_name, private_key, rpc_url):
    # 连接到以太坊网络
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # 读取ABI和字节码
    base_dir = os.path.dirname(os.path.dirname(__file__))
    abi_path = os.path.join(base_dir, 'data', 'abi', f'{contract_name}.json')
    bytecode_path = os.path.join(base_dir, 'data', 'bytecode', f'{contract_name}.bin')

    with open(abi_path, 'r') as abi_file:
        abi = json.load(abi_file)
    
    with open(bytecode_path, 'r') as bytecode_file:
        bytecode = bytecode_file.read()

    # 创建账户对象
    account = w3.eth.account.privateKeyToAccount(private_key)
    
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
    return tx_receipt.contractAddress

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="部署智能合约")
    parser.add_argument("contract_name", help="要部署的合约名称")
    parser.add_argument("--private_key", required=True, help="用于部署的私钥")
    parser.add_argument("--rpc_url", required=True, help="以太坊节点的RPC URL")
    
    args = parser.parse_args()

    deploy_contract(args.contract_name, args.private_key, args.rpc_url)
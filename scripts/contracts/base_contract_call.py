'''
这个模块包含了与智能合约交互的通用功能。

主要包括以下类：
- BaseContractCall: 提供了构建交易、发送交易和调用合约函数的基本方法。

主要功能：
1. 构建并发送交易
2. 调用合约函数

使用方法：
继承BaseContractCall类，并在子类中实现特定合约的调用逻辑。
'''
from abc import ABC, abstractmethod


class Call(ABC):
    @abstractmethod
    def call(self, contract):
        pass


class BaseContractCall(Call):
    def __init__(self, w3, private_key):
        self.w3 = w3
        self.private_key = private_key

    def build_transaction_and_send(self, contract, function_name, args):
        account = self.w3.eth.account.privateKeyToAccount(self.private_key)
        nonce = self.w3.eth.getTransactionCount(account.address)
        transaction = contract.functions[function_name](*args).buildTransaction({
            "chainId": self.w3.eth.chain_id,
            "gasPrice": self.w3.eth.gas_price,
            "from": account.address,
            "nonce": nonce,
        })
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction sent: {receipt}")
        return receipt

    def function_call(self, contract, function_name, args=None):
        if args is None:
            result = contract.functions[function_name]().call()
        else:
            if isinstance(args, list):
                result = contract.functions[function_name](*args).call()
            else:
                result = contract.functions[function_name](args).call()
        return result

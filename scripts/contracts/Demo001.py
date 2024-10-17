from .base_contract_call import BaseContractCall

class Demo001(BaseContractCall):
    def __init__(self, w3, private_key):
        super().__init__(w3, private_key)

    def call(self, contract):
        self.build_transaction_and_send(contract, "setName", ("你好", ))
        stored_value = self.function_call(contract, "getName")
        print(f"Stored value: {stored_value}")

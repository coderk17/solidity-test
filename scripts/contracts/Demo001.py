from .base_contract_call import BaseContractCall

class Demo001(BaseContractCall):
    def __init__(self, w3, private_key):
        super().__init__(w3, private_key)

    def call(self, contract):
        # 获取 publicVariable
        public_var = self.function_call(contract, "publicVariable")
        print(f"publicVariable 值: {public_var}")

        # 获取 privateVariable
        private_var = self.function_call(contract, "getPrivateVariable")
        print(f"privateVariable 值: {private_var}")

        # 获取 internalVariable
        internal_var = self.function_call(contract, "getInternalVariable")
        print(f"internalVariable 值: {internal_var}")

        # 调用 publicFunction
        public_result = self.function_call(contract, "publicFunction")
        print(f"publicFunction 结果: {public_result}")

        # 调用 externalFunction
        external_result = self.function_call(contract, "externalFunction")
        print(f"externalFunction 结果: {external_result}")

        # 调用 pureFunction
        pure_result = self.function_call(contract, "pureFunction", [10, 20])
        print(f"pureFunction 结果: {pure_result}")

        # 调用 viewFunction
        view_result = self.function_call(contract, "viewFunction")
        print(f"viewFunction 结果: {view_result}")

        # 获取常量 CONSTANT_VALUE
        constant_value = self.function_call(contract, "CONSTANT_VALUE")
        print(f"CONSTANT_VALUE: {constant_value}")

        # 获取不可变量 IMMUTABLE_VALUE1 和 IMMUTABLE_VALUE2
        immutable_value1 = self.function_call(contract, "IMMUTABLE_VALUE1")
        immutable_value2 = self.function_call(contract, "IMMUTABLE_VALUE2")
        print(f"IMMUTABLE_VALUE1: {immutable_value1}")
        print(f"IMMUTABLE_VALUE2: {immutable_value2}")

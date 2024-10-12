import os
import json
import sys

from solcx import compile_standard, install_solc

def compile_contract(contract_path):
    contract_path = os.path.abspath(contract_path)
    contract_name = os.path.splitext(os.path.basename(contract_path))[0]
    
    print(f"合约路径: {contract_path}")
    print(f"文件是否存在: {os.path.exists(contract_path)}")
    
    if not os.path.exists(contract_path):
        print(f"错误：找不到文件 '{contract_path}'")
        sys.exit(1)

    with open(contract_path, 'r') as file:
        contract_source = file.read()

    install_solc("0.8.0")

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_path: {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            }
        },
        solc_version="0.8.0",
    )

    # 创建目录
    base_dir = os.path.dirname(os.path.dirname(__file__))
    os.makedirs(os.path.join(base_dir, 'data', 'abi'), exist_ok=True)
    os.makedirs(os.path.join(base_dir, 'data', 'bytecode'), exist_ok=True)

    # 提取并保存ABI
    abi = compiled_sol['contracts'][contract_path][contract_name]['abi']
    abi_file_path = os.path.join(base_dir, 'data', 'abi', f'{contract_name}.json')
    with open(abi_file_path, 'w') as abi_file:
        json.dump(abi, abi_file)

    # 提取并保存字节码
    bytecode = compiled_sol['contracts'][contract_path][contract_name]['evm']['bytecode']['object']
    bytecode_file_path = os.path.join(base_dir, 'data', 'bytecode', f'{contract_name}.bin')
    with open(bytecode_file_path, 'w') as bytecode_file:
        bytecode_file.write(bytecode)

    print(f"已成功编译合约 {contract_name}")
    print(f"ABI 保存至: {abi_file_path}")
    print(f"字节码保存至: {bytecode_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("请提供合约文件名作为参数")
        sys.exit(1)
    
    contract_path = sys.argv[1]
    print(f"提供的合约路径: {contract_path}")
    compile_contract(contract_path)
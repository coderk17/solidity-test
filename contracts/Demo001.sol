// SPDX-License-Identifier: GPL-2.0-only
/**
 * @title Demo001 合约
 * @dev 这个合约演示了 Solidity 中的各种可见性关键字、函数类型和常量的使用。
 * 包含了 public、private、internal 和 external 的变量和函数示例，
 * 以及 pure、view 函数和常量的定义。
 */
pragma solidity ^0.8.0;

contract Demo001 {
    // 可见性关键字示例和注释
    
    // public: 可以被外部访问，自动生成getter函数
    uint256 public publicVariable = 100;
    
    // private: 只能在当前合约内部访问
    uint256 private privateVariable = 200;
    
    // internal: 只能在当前合约及其子合约中访问
    uint256 internal internalVariable = 300;
    
    // external: 只能从合约外部调用，不能在合约内部使用
    function externalFunction() external pure returns (string memory) {
        return "This is an external function";
    }
    
    // 无关键字（默认internal）
    uint256 defaultInternalVariable = 400;
    
    // 函数可见性示例
    function publicFunction() public pure returns (string memory) {
        return "This is a public function";
    }
    
    function privateFunction() private pure returns (string memory) {
        return "This is a private function";
    }
    
    function internalFunction() internal pure returns (string memory) {
        return "This is an internal function";
    }
    // pure 函数示例：不读取也不修改状态
    function pureFunction(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }
    
    // view 函数示例：只读取状态，不修改状态
    function viewFunction() public view returns (uint256) {
        return publicVariable;
    }
    
    // constant 变量示例：编译时确定的常量
    uint256 public constant CONSTANT_VALUE = 1000;
    
    // immutable 变量示例：部署时确定的不可变量
    uint256 public immutable IMMUTABLE_VALUE1;
    uint256 public immutable IMMUTABLE_VALUE2;
    
    constructor(uint256 _value1, uint256 _value2) {
        IMMUTABLE_VALUE1 = _value1;
        IMMUTABLE_VALUE2 = _value2;
    }
}

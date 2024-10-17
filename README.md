# 智能合约编译与部署项目

本项目提供了编译、部署和运行以太坊智能合约的工具。主要包含三个脚本: compile.py、deploy.py 和 run.py。

## 安装依赖

在使用脚本之前,请确保安装了所有必要的依赖:

`pip install -r scripts/requirements.txt`

# 项目结构

## 1. compile.py

compile.py 脚本用于编译智能合约，需要保证合约名和合约文件前缀保持一致。

使用方法:

`python scripts/compile.py [合约名]`

示例:

`python scripts/compile.py Demo001`

## 2. deploy.py

deploy.py 脚本用于部署编译好的智能合约。

使用方法:

`python scripts/deploy.py [合约名称]`

示例:

`python scripts/deploy.py Demo001`

这将部署指定的合约,并输出部署后的合约地址。

## 3. run.py

run.py 脚本用于运行和交互已部署的智能合约。

使用方法:

`python scripts/run.py [执行命令: compile, deploy, execute, all] [合约名称]`

示例:

`python scripts/run.py execute Demo001`

# 项目使用说明

本项目包含了三个主要的脚本文件:run.py、deploy.py 和 compile.py。以下是每个脚本的详细使用说明。

## 1. run.py

run.py 脚本用于运行项目。

使用方法:

```
python scripts/run.py [参数]
```

常用参数:
- `--mode`: 运行模式,可选值为 'dev' 或 'prod'
- `--port`: 指定运行端口号

示例:

```
python scripts/run.py --mode dev --port 8080
```

## 2. deploy.py

deploy.py 脚本用于部署项目。

使用方法:

```
python scripts/deploy.py [参数]
```

常用参数:
- `--env`: 部署环境,可选值为 'staging' 或 'production'
- `--version`: 指定部署版本号

示例:
```
python scripts/deploy.py --env production --version 1.0.0
```

## 3. compile.py

compile.py 脚本用于编译项目。

使用方法:
```
python scripts/compile.py [参数]
```

常用参数:
- `--optimize`: 是否进行优化,可选值为 'true' 或 'false'
- `--output`: 指定输出目录

示例:
```
python scripts/compile.py --optimize true --output ./dist
```

## 注意事项

1. 在运行任何脚本之前,请确保已安装所有必要的依赖。
2. 请根据您的具体项目需求调整参数值。
3. 如遇到任何问题,请查看每个脚本文件中的详细注释或联系技术支持。

## 贡献

如果您想为本项目做出贡献,请遵循以下步骤:
1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 将您的更改推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。

# QQ空间资料下载器

[English Version](./README.md)

## 如何使用？

**推荐使用方式**: 直接跑python脚本

- 创建虚拟环境并激活环境
    ```sh
    python -m venv venv
    # 如果是Mac或者Linux
    source venv/bin/activate
    # 如果是windows
    venv\bin\activate
    ```

- 安装依赖项

    `pip install -r requirements.txt`

- 使用QQ客户端登陆自己的QQ账号，使用**谷歌浏览器**打开QQ空间时，能够自动检测到已登陆的账号信息。这样这个工具不会接触到你QQ账号的敏感信息，PS：我也能少做点工作，哈哈～

- 执行下面的代码

    `python run.py --account <QQ账号> --save <保存数据的文件夹>`

这样，程序就开始自动备份包括*图片/说说/留言板/日志*这些数据。

**注意**: 如果空间数据较多，推荐使用一些工具命令，如`screen`等。这样不会不小心将前台工作给挂了...

**如果上面方式还是不会怎么办？**

提供了打包好的`exe`[文件](https://github.com/tkianai/QQZone.downloader/releases)。


## 为什么有这个？

还记得好多年前，`QQ家园`挺火的。后来腾讯也没提供备份方案，直接就关闭。QQ也是一样，空间里存了不少珍贵的照片和记忆，不想就这样丢失，所以写了这个工具。**趁着现在能用，赶紧的吧，我反正备份好了！**

## 备注

如果对您有帮助，麻烦点一下star吧，让更多人看到，谢谢支持～
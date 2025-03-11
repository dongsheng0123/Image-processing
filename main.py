#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
刘东升的图片处理工具 - 主程序入口

这个程序是一个图片处理工具，提供了多种图片处理功能，包括自动去背景、图像剪裁与缩放等。
该工具采用模块化设计，便于扩展和维护。
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """主程序入口函数"""
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序名称
    app.setApplicationName("刘东升的图片处理工具")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序事件循环
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
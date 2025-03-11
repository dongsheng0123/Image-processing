#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
刘东升的图片处理工具 - 主窗口界面

实现了应用程序的主窗口界面，包括菜单栏、工具栏、状态栏和主要功能区域。
提供了图片选择、功能选择和参数设置等功能。
"""

import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QLabel, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                             QGroupBox, QSlider, QSpinBox, QComboBox, QMessageBox,
                             QSplitter, QScrollArea, QSizePolicy, QCheckBox, QLineEdit)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QSize

# 导入功能模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.background_remover import BackgroundRemover
from modules.image_processor import ImageProcessor


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化成员变量
        self.current_image_path = None
        self.processed_image = None
        self.background_remover = BackgroundRemover()
        self.image_processor = ImageProcessor()
        
        # 设置窗口属性
        self.setWindowTitle("刘东升的图片处理工具")
        self.setMinimumSize(1000, 700)
        
        # 设置应用程序图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 初始化界面
        self._init_ui()
    
    def _init_ui(self):
        """初始化用户界面"""
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 创建左侧面板（功能选择和参数设置）
        left_panel = self._create_left_panel()
        
        # 创建右侧面板（图片显示）
        right_panel = self._create_right_panel()
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 700])
        
        # 添加分割器到主布局
        main_layout.addWidget(splitter)
        
        # 创建菜单栏
        self._create_menu_bar()
        
        # 创建状态栏
        self.statusBar().showMessage("就绪")
    
    def _create_left_panel(self):
        """创建左侧面板"""
        # 创建左侧面板容器
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 创建图片选择组
        image_group = QGroupBox("图片选择")
        image_layout = QVBoxLayout(image_group)
        
        # 添加选择图片按钮
        self.select_image_btn = QPushButton("选择图片")
        self.select_image_btn.clicked.connect(self._on_select_image)
        image_layout.addWidget(self.select_image_btn)
        
        # 添加图片信息标签
        self.image_info_label = QLabel("未选择图片")
        self.image_info_label.setWordWrap(True)
        image_layout.addWidget(self.image_info_label)
        
        # 添加图片选择组到左侧布局
        left_layout.addWidget(image_group)
        
        # 创建功能选择组
        function_group = QGroupBox("功能选择")
        function_layout = QVBoxLayout(function_group)
        
        # 添加功能选择下拉框
        self.function_combo = QComboBox()
        self.function_combo.addItem("自动去背景")
        self.function_combo.addItem("图像剪裁")
        self.function_combo.addItem("图像缩放")
        self.function_combo.currentIndexChanged.connect(self._on_function_changed)
        function_layout.addWidget(self.function_combo)
        
        # 添加功能选择组到左侧布局
        left_layout.addWidget(function_group)
        
        # 创建参数设置组
        self.params_group = QGroupBox("参数设置")
        self.params_layout = QVBoxLayout(self.params_group)
        
        # 初始化参数设置（默认为自动去背景）
        self._init_background_remover_params()
        
        # 添加参数设置组到左侧布局
        left_layout.addWidget(self.params_group)
        
        # 创建操作按钮组
        operation_group = QGroupBox("操作")
        operation_layout = QVBoxLayout(operation_group)
        
        # 添加执行按钮
        self.execute_btn = QPushButton("执行")
        self.execute_btn.clicked.connect(self._on_execute)
        self.execute_btn.setEnabled(False)  # 初始禁用
        operation_layout.addWidget(self.execute_btn)
        
        # 添加保存按钮
        self.save_btn = QPushButton("保存结果")
        self.save_btn.clicked.connect(self._on_save_result)
        self.save_btn.setEnabled(False)  # 初始禁用
        operation_layout.addWidget(self.save_btn)
        
        # 添加操作按钮组到左侧布局
        left_layout.addWidget(operation_group)
        
        # 添加弹性空间
        left_layout.addStretch()
        
        return left_panel
    
    def _create_right_panel(self):
        """创建右侧面板"""
        # 创建右侧面板容器
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 创建图片显示区域
        self.image_scroll_area = QScrollArea()
        self.image_scroll_area.setWidgetResizable(True)
        self.image_scroll_area.setAlignment(Qt.AlignCenter)
        
        # 创建图片标签
        self.image_label = QLabel("请选择图片")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # 将图片标签添加到滚动区域
        self.image_scroll_area.setWidget(self.image_label)
        
        # 添加滚动区域到右侧布局
        right_layout.addWidget(self.image_scroll_area)
        
        return right_panel
    
    def _create_menu_bar(self):
        """创建菜单栏"""
        # 创建文件菜单
        file_menu = self.menuBar().addMenu("文件")
        
        # 添加打开图片动作
        open_action = QAction("打开图片", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_select_image)
        file_menu.addAction(open_action)
        
        # 添加保存结果动作
        save_action = QAction("保存结果", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self._on_save_result)
        save_action.setEnabled(False)  # 初始禁用
        self.save_action = save_action  # 保存引用以便后续启用/禁用
        file_menu.addAction(save_action)
        
        # 添加分隔线
        file_menu.addSeparator()
        
        # 添加退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 创建帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
        
        # 添加关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)
    
    def _init_background_remover_params(self):
        """初始化自动去背景参数设置"""
        # 清空现有参数设置
        self._clear_params_layout()
        
        # 添加模型选择
        model_label = QLabel("模型选择:")
        self.model_combo = QComboBox()
        self.model_combo.addItem("u2net")
        self.model_combo.addItem("u2netp")
        self.model_combo.addItem("u2net_human_seg")
        self.model_combo.addItem("silueta")
        self.model_combo.addItem("isnet-general-use")
        self.params_layout.addWidget(model_label)
        self.params_layout.addWidget(self.model_combo)
        
        # 添加透明度设置
        alpha_label = QLabel("透明度阈值 (0-255):")
        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setRange(0, 255)
        self.alpha_slider.setValue(0)
        self.alpha_value = QLabel("0")
        self.alpha_slider.valueChanged.connect(lambda v: self.alpha_value.setText(str(v)))
        
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(self.alpha_slider)
        alpha_layout.addWidget(self.alpha_value)
        
        self.params_layout.addWidget(alpha_label)
        self.params_layout.addLayout(alpha_layout)
    
    def _init_crop_params(self):
        """初始化图像剪裁参数设置"""
        # 清空现有参数设置
        self._clear_params_layout()
        
        # 添加宽度设置
        width_label = QLabel("宽度 (像素):")
        self.width_spinbox = QSpinBox()
        self.width_spinbox.setRange(1, 10000)
        self.width_spinbox.setValue(100)
        self.params_layout.addWidget(width_label)
        self.params_layout.addWidget(self.width_spinbox)
        
        # 添加高度设置
        height_label = QLabel("高度 (像素):")
        self.height_spinbox = QSpinBox()
        self.height_spinbox.setRange(1, 10000)
        self.height_spinbox.setValue(100)
        self.params_layout.addWidget(height_label)
        self.params_layout.addWidget(self.height_spinbox)
        
        # 添加保持宽高比选项
        self.keep_aspect_ratio = QCheckBox("保持宽高比")
        self.keep_aspect_ratio.setChecked(True)
        self.params_layout.addWidget(self.keep_aspect_ratio)
    
    def _init_resize_params(self):
        """初始化图像缩放参数设置"""
        # 清空现有参数设置
        self._clear_params_layout()
        
        # 添加缩放模式选择
        mode_label = QLabel("缩放模式:")
        self.resize_mode_combo = QComboBox()
        self.resize_mode_combo.addItem("按尺寸缩放")
        self.resize_mode_combo.addItem("按文件大小缩放")
        self.resize_mode_combo.currentIndexChanged.connect(self._on_resize_mode_changed)
        self.params_layout.addWidget(mode_label)
        self.params_layout.addWidget(self.resize_mode_combo)
        
        # 添加尺寸设置（默认显示）
        self.size_params_widget = QWidget()
        size_layout = QVBoxLayout(self.size_params_widget)
        
        # 添加宽度设置
        width_label = QLabel("宽度 (像素):")
        self.resize_width_spinbox = QSpinBox()
        self.resize_width_spinbox.setRange(1, 10000)
        self.resize_width_spinbox.setValue(800)
        size_layout.addWidget(width_label)
        size_layout.addWidget(self.resize_width_spinbox)
        
        # 添加高度设置
        height_label = QLabel("高度 (像素):")
        self.resize_height_spinbox = QSpinBox()
        self.resize_height_spinbox.setRange(1, 10000)
        self.resize_height_spinbox.setValue(600)
        size_layout.addWidget(height_label)
        size_layout.addWidget(self.resize_height_spinbox)
        
        # 添加保持宽高比选项
        self.resize_keep_aspect_ratio = QCheckBox("保持宽高比")
        self.resize_keep_aspect_ratio.setChecked(True)
        size_layout.addWidget(self.resize_keep_aspect_ratio)
        
        # 添加尺寸设置到参数布局
        self.params_layout.addWidget(self.size_params_widget)
        
        # 添加文件大小设置（初始隐藏）
        self.filesize_params_widget = QWidget()
        filesize_layout = QVBoxLayout(self.filesize_params_widget)
        
        # 添加目标文件大小设置
        filesize_label = QLabel("目标文件大小 (KB):")
        self.filesize_spinbox = QSpinBox()
        self.filesize_spinbox.setRange(1, 10000)
        self.filesize_spinbox.setValue(500)
        filesize_layout.addWidget(filesize_label)
        filesize_layout.addWidget(self.filesize_spinbox)
        
        # 添加质量设置
        quality_label = QLabel("图像质量 (1-100):")
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(85)
        self.quality_value = QLabel("85")
        self.quality_slider.valueChanged.connect(lambda v: self.quality_value.setText(str(v)))
        
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_slider)
        quality_layout.addWidget(self.quality_value)
        
        filesize_layout.addWidget(quality_label)
        filesize_layout.addLayout(quality_layout)
        
        # 添加文件大小设置到参数布局（初始隐藏）
        self.params_layout.addWidget(self.filesize_params_widget)
        self.filesize_params_widget.hide()
    
    def _on_resize_mode_changed(self, index):
        """缩放模式改变时的处理函数"""
        if index == 0:  # 按尺寸缩放
            self.size_params_widget.show()
            self.filesize_params_widget.hide()
        else:  # 按文件大小缩放
            self.size_params_widget.hide()
            self.filesize_params_widget.show()
    
    def _clear_params_layout(self):
        """清空参数设置布局"""
        # 清除所有小部件
        while self.params_layout.count():
            item = self.params_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # 递归清除子布局
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
    
    def _on_function_changed(self, index):
        """功能选择改变时的处理函数"""
        if index == 0:  # 自动去背景
            self._init_background_remover_params()
        elif index == 1:  # 图像剪裁
            self._init_crop_params()
        elif index == 2:  # 图像缩放
            self._init_resize_params()
    
    def _on_select_image(self):
        """选择图片按钮点击处理函数"""
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            # 更新当前图片路径
            self.current_image_path = file_path
            
            # 显示图片
            self._display_image(file_path)
            
            # 更新图片信息
            file_info = os.path.getsize(file_path) / 1024  # KB
            self.image_info_label.setText(f"文件: {os.path.basename(file_path)}\n大小: {file_info:.2f} KB")
            
            # 启用执行按钮
            self.execute_btn.setEnabled(True)
            
            # 禁用保存按钮（因为还没有处理结果）
            self.save_btn.setEnabled(False)
            self.save_action.setEnabled(False)
            
            # 更新状态栏
            self.statusBar().showMessage(f"已加载图片: {os.path.basename(file_path)}")
    
    def _display_image(self, image_path=None, image=None):
        """显示图片"""
        if image_path and not image:
            # 从文件加载图片
            pixmap = QPixmap(image_path)
        elif image:
            # 从PIL的Image对象转换为QImage
            if hasattr(image, 'mode'):  # 检查是否为PIL Image对象
                # 将PIL Image转换为QImage
                data = image.tobytes("raw", "RGBA" if image.mode == "RGBA" else "RGB")
                qimage = QImage(
                    data,
                    image.width,
                    image.height,
                    QImage.Format_RGBA8888 if image.mode == "RGBA" else QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(qimage)
            else:
                # 假设已经是QImage对象
                pixmap = QPixmap.fromImage(image)
        else:
            return
        
        # 调整图片大小以适应显示区域
        pixmap = pixmap.scaled(
            self.image_scroll_area.width() - 20,
            self.image_scroll_area.height() - 20,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 显示图片
        self.image_label.setPixmap(pixmap)
    
    def _on_execute(self):
        """执行按钮点击处理函数"""
        if not self.current_image_path:
            QMessageBox.warning(self, "警告", "请先选择图片！")
            return
        
        # 获取当前选择的功能
        current_function = self.function_combo.currentIndex()
        
        try:
            # 根据不同功能执行相应处理
            if current_function == 0:  # 自动去背景
                # 获取参数
                model = self.model_combo.currentText()
                alpha_threshold = self.alpha_slider.value()
                
                # 执行去背景
                self.statusBar().showMessage("正在处理图片，请稍候...")
                self.processed_image = self.background_remover.remove_background(
                    self.current_image_path, model, alpha_threshold
                )
                
            elif current_function == 1:  # 图像剪裁
                # 获取参数
                width = self.width_spinbox.value()
                height = self.height_spinbox.value()
                keep_aspect_ratio = self.keep_aspect_ratio.isChecked()
                
                # 执行剪裁
                self.statusBar().showMessage("正在处理图片，请稍候...")
                self.processed_image = self.image_processor.crop_image(
                    self.current_image_path, width, height, keep_aspect_ratio
                )
                
            elif current_function == 2:  # 图像缩放
                # 获取缩放模式
                resize_mode = self.resize_mode_combo.currentIndex()
                
                if resize_mode == 0:  # 按尺寸缩放
                    # 获取参数
                    width = self.resize_width_spinbox.value()
                    height = self.resize_height_spinbox.value()
                    keep_aspect_ratio = self.resize_keep_aspect_ratio.isChecked()
                    
                    # 执行缩放
                    self.statusBar().showMessage("正在处理图片，请稍候...")
                    self.processed_image = self.image_processor.resize_image(
                        self.current_image_path, width, height, keep_aspect_ratio
                    )
                    
                else:  # 按文件大小缩放
                    # 获取参数
                    target_size = self.filesize_spinbox.value()  # KB
                    quality = self.quality_slider.value()
                    
                    # 执行缩放
                    self.statusBar().showMessage("正在处理图片，请稍候...")
                    self.processed_image = self.image_processor.resize_to_filesize(
                        self.current_image_path, target_size, quality
                    )
            
            # 显示处理结果
            if self.processed_image:
                self._display_image(image=self.processed_image)
                
                # 启用保存按钮
                self.save_btn.setEnabled(True)
                self.save_action.setEnabled(True)
                
                # 更新状态栏
                self.statusBar().showMessage("处理完成")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理图片时出错: {str(e)}")
            self.statusBar().showMessage("处理失败")
    
    def _on_save_result(self):
        """保存结果按钮点击处理函数"""
        if not self.processed_image:
            QMessageBox.warning(self, "警告", "没有可保存的处理结果！")
            return
        
        # 打开保存文件对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存结果", "", "PNG图片 (*.png);;JPEG图片 (*.jpg);;所有文件 (*.*)"
        )
        
        if file_path:
            try:
                # 保存图片
                self.processed_image.save(file_path)
                
                # 更新状态栏
                self.statusBar().showMessage(f"结果已保存至: {os.path.basename(file_path)}")
                
                # 显示成功消息
                QMessageBox.information(self, "成功", "处理结果已成功保存！")
                
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存结果时出错: {str(e)}")
    
    def _show_about_dialog(self):
        """显示关于对话框"""
        about_text = (
            "<h2>刘东升的图片处理工具</h2>"
            "<p>版本: 1.0.0</p>"
            "<p>开发者: 刘东升</p>"
            "<p>这是一个功能强大的图片处理工具，提供了多种图片处理功能，"
            "包括自动去背景、图像剪裁与缩放等。</p>"
            "<p>该工具采用模块化设计，便于扩展和维护。</p>"
        )
        
        QMessageBox.about(self, "关于", about_text)
    
    def resizeEvent(self, event):
        """窗口大小改变事件处理函数"""
        super().resizeEvent(event)
        
        # 如果有图片，则重新调整图片大小以适应新的显示区域
        if self.image_label.pixmap():
            if self.processed_image:
                self._display_image(image=self.processed_image)
            elif self.current_image_path:
                self._display_image(image_path=self.current_image_path)
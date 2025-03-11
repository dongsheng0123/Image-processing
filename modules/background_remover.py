#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
刘东升的图片处理工具 - 自动去背景模块

使用rembg库实现自动去除图片背景的功能。
支持多种模型选择和透明度阈值设置。
"""

import os
import numpy as np
from PIL import Image
from rembg import remove, new_session


class BackgroundRemover:
    """自动去背景类"""
    
    def __init__(self):
        """初始化背景移除器"""
        # 可用的模型列表
        self.available_models = [
            "u2net",            # 通用模型
            "u2netp",           # 轻量级模型
            "u2net_human_seg",  # 人像分割模型
            "silueta",          # 轮廓模型
            "isnet-general-use" # 高精度通用模型
        ]
        
        # 当前会话和模型
        self.current_model = None
        self.session = None
    
    def remove_background(self, image_path, model="u2net", alpha_threshold=0):
        """
        移除图片背景
        
        参数:
            image_path (str): 输入图片路径
            model (str): 使用的模型名称
            alpha_threshold (int): 透明度阈值，0-255之间
            
        返回:
            PIL.Image: 处理后的图片对象
        """
        # 检查模型是否有效
        if model not in self.available_models:
            raise ValueError(f"不支持的模型: {model}，可用模型: {', '.join(self.available_models)}")
        
        # 检查透明度阈值是否有效
        if not 0 <= alpha_threshold <= 255:
            raise ValueError(f"透明度阈值必须在0-255之间，当前值: {alpha_threshold}")
        
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 如果模型发生变化，创建新会话
        if self.current_model != model or self.session is None:
            self.session = new_session(model)
            self.current_model = model
        
        try:
            # 加载图片
            input_image = Image.open(image_path)
            
            # 移除背景
            output_image = remove(
                input_image,
                session=self.session,
                alpha_matting=alpha_threshold > 0,
                alpha_matting_foreground_threshold=alpha_threshold,
                alpha_matting_background_threshold=alpha_threshold,
                alpha_matting_erode_size=10
            )
            
            return output_image
            
        except Exception as e:
            raise RuntimeError(f"处理图片时出错: {str(e)}")
    
    def remove_background_batch(self, input_dir, output_dir, model="u2net", alpha_threshold=0):
        """
        批量移除图片背景
        
        参数:
            input_dir (str): 输入图片目录
            output_dir (str): 输出图片目录
            model (str): 使用的模型名称
            alpha_threshold (int): 透明度阈值，0-255之间
            
        返回:
            int: 成功处理的图片数量
        """
        # 检查输入目录是否存在
        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
            raise FileNotFoundError(f"输入目录不存在: {input_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 支持的图片格式
        supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
        
        # 获取所有图片文件
        image_files = [
            f for f in os.listdir(input_dir) 
            if os.path.isfile(os.path.join(input_dir, f)) and 
            any(f.lower().endswith(ext) for ext in supported_formats)
        ]
        
        # 如果没有图片文件
        if not image_files:
            raise ValueError(f"输入目录中没有支持的图片文件: {input_dir}")
        
        # 处理计数
        processed_count = 0
        
        # 如果模型发生变化，创建新会话
        if self.current_model != model or self.session is None:
            self.session = new_session(model)
            self.current_model = model
        
        # 批量处理图片
        for image_file in image_files:
            try:
                # 构建完整路径
                input_path = os.path.join(input_dir, image_file)
                
                # 构建输出路径（保持原文件名，但扩展名改为png以支持透明度）
                output_filename = os.path.splitext(image_file)[0] + ".png"
                output_path = os.path.join(output_dir, output_filename)
                
                # 加载图片
                input_image = Image.open(input_path)
                
                # 移除背景
                output_image = remove(
                    input_image,
                    session=self.session,
                    alpha_matting=alpha_threshold > 0,
                    alpha_matting_foreground_threshold=alpha_threshold,
                    alpha_matting_background_threshold=alpha_threshold,
                    alpha_matting_erode_size=10
                )
                
                # 保存结果
                output_image.save(output_path)
                
                # 增加计数
                processed_count += 1
                
            except Exception as e:
                print(f"处理图片 {image_file} 时出错: {str(e)}")
        
        return processed_count
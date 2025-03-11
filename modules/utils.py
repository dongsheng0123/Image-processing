#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
刘东升的图片处理工具 - 工具函数模块

提供一些通用的工具函数，如文件操作、图像格式转换等。
"""

import os
import sys
from PIL import Image


def get_supported_formats():
    """
    获取支持的图片格式列表
    
    返回:
        list: 支持的图片格式扩展名列表
    """
    return [".jpg", ".jpeg", ".png", ".bmp", ".gif"]


def is_valid_image(file_path):
    """
    检查文件是否为有效的图片文件
    
    参数:
        file_path (str): 文件路径
        
    返回:
        bool: 如果是有效的图片文件则返回True，否则返回False
    """
    # 检查文件是否存在
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False
    
    # 检查文件扩展名
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in get_supported_formats():
        return False
    
    # 尝试打开图片
    try:
        with Image.open(file_path) as img:
            img.verify()  # 验证图片完整性
        return True
    except Exception:
        return False


def get_image_info(image_path):
    """
    获取图片信息
    
    参数:
        image_path (str): 图片路径
        
    返回:
        dict: 包含图片信息的字典，如果图片无效则返回None
    """
    if not is_valid_image(image_path):
        return None
    
    try:
        with Image.open(image_path) as img:
            # 获取基本信息
            info = {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size": os.path.getsize(image_path),
                "filename": os.path.basename(image_path)
            }
            return info
    except Exception:
        return None


def ensure_dir(directory):
    """
    确保目录存在，如果不存在则创建
    
    参数:
        directory (str): 目录路径
        
    返回:
        bool: 如果目录已存在或创建成功则返回True，否则返回False
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
        return True
    except Exception:
        return False


def convert_image_format(image_path, output_path, format="PNG"):
    """
    转换图片格式
    
    参数:
        image_path (str): 输入图片路径
        output_path (str): 输出图片路径
        format (str): 目标格式，如'PNG'、'JPEG'等
        
    返回:
        bool: 如果转换成功则返回True，否则返回False
    """
    if not is_valid_image(image_path):
        return False
    
    try:
        img = Image.open(image_path)
        
        # 如果目标格式是JPEG且图片有透明通道，需要转换为RGB模式
        if format.upper() == "JPEG" and img.mode == "RGBA":
            img = img.convert("RGB")
        
        # 保存为目标格式
        img.save(output_path, format=format)
        return True
    except Exception:
        return False
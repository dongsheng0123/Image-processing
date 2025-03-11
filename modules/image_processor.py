#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
刘东升的图片处理工具 - 图像处理模块

实现图像剪裁与缩放功能，包括按照指定尺寸剪裁和按照目标文件大小缩放图片。
"""

import os
import io
from PIL import Image


class ImageProcessor:
    """图像处理类"""
    
    def __init__(self):
        """初始化图像处理器"""
        # 支持的图片格式
        self.supported_formats = [".jpg", ".jpeg", ".png", ".bmp", ".gif"]
    
    def crop_image(self, image_path, width, height, keep_aspect_ratio=True):
        """
        剪裁图片
        
        参数:
            image_path (str): 输入图片路径
            width (int): 目标宽度
            height (int): 目标高度
            keep_aspect_ratio (bool): 是否保持宽高比
            
        返回:
            PIL.Image: 处理后的图片对象
        """
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 检查宽高是否有效
        if width <= 0 or height <= 0:
            raise ValueError(f"宽度和高度必须大于0，当前值: 宽度={width}, 高度={height}")
        
        try:
            # 加载图片
            image = Image.open(image_path)
            
            if keep_aspect_ratio:
                # 计算原始宽高比
                original_ratio = image.width / image.height
                target_ratio = width / height
                
                if original_ratio > target_ratio:
                    # 原图更宽，需要裁剪宽度
                    new_width = int(image.height * target_ratio)
                    left = (image.width - new_width) // 2
                    right = left + new_width
                    image = image.crop((left, 0, right, image.height))
                else:
                    # 原图更高，需要裁剪高度
                    new_height = int(image.width / target_ratio)
                    top = (image.height - new_height) // 2
                    bottom = top + new_height
                    image = image.crop((0, top, image.width, bottom))
            
            # 调整到目标尺寸
            resized_image = image.resize((width, height), Image.LANCZOS)
            
            return resized_image
            
        except Exception as e:
            raise RuntimeError(f"处理图片时出错: {str(e)}")
    
    def resize_image(self, image_path, width, height, keep_aspect_ratio=True):
        """
        调整图片大小
        
        参数:
            image_path (str): 输入图片路径
            width (int): 目标宽度
            height (int): 目标高度
            keep_aspect_ratio (bool): 是否保持宽高比
            
        返回:
            PIL.Image: 处理后的图片对象
        """
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 检查宽高是否有效
        if width <= 0 or height <= 0:
            raise ValueError(f"宽度和高度必须大于0，当前值: 宽度={width}, 高度={height}")
        
        try:
            # 加载图片
            image = Image.open(image_path)
            
            if keep_aspect_ratio:
                # 计算原始宽高比
                original_ratio = image.width / image.height
                target_ratio = width / height
                
                if original_ratio > target_ratio:
                    # 原图更宽，以宽度为基准调整高度
                    new_height = int(width / original_ratio)
                    resized_image = image.resize((width, new_height), Image.LANCZOS)
                else:
                    # 原图更高，以高度为基准调整宽度
                    new_width = int(height * original_ratio)
                    resized_image = image.resize((new_width, height), Image.LANCZOS)
            else:
                # 直接调整到目标尺寸
                resized_image = image.resize((width, height), Image.LANCZOS)
            
            return resized_image
            
        except Exception as e:
            raise RuntimeError(f"处理图片时出错: {str(e)}")
    
    def resize_to_filesize(self, image_path, target_size_kb, quality=85):
        """
        将图片缩放到指定文件大小
        
        参数:
            image_path (str): 输入图片路径
            target_size_kb (int): 目标文件大小（KB）
            quality (int): 初始质量设置（1-100）
            
        返回:
            PIL.Image: 处理后的图片对象
        """
        # 检查图片是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 检查目标大小是否有效
        if target_size_kb <= 0:
            raise ValueError(f"目标文件大小必须大于0，当前值: {target_size_kb} KB")
        
        # 检查质量设置是否有效
        if not 1 <= quality <= 100:
            raise ValueError(f"质量设置必须在1-100之间，当前值: {quality}")
        
        try:
            # 加载图片
            image = Image.open(image_path)
            original_format = image.format
            
            # 如果是PNG且有透明通道，保持PNG格式
            if original_format == 'PNG' and image.mode == 'RGBA':
                output_format = 'PNG'
            else:
                # 否则使用JPEG格式（更容易控制文件大小）
                output_format = 'JPEG'
                if image.mode == 'RGBA':
                    # 如果有透明通道，转换为RGB
                    image = image.convert('RGB')
            
            # 目标大小（字节）
            target_size_bytes = target_size_kb * 1024
            
            # 获取原始图片大小
            buffer = io.BytesIO()
            image.save(buffer, format=output_format, quality=quality)
            current_size = buffer.getbuffer().nbytes
            
            # 如果原始图片已经小于目标大小，直接返回
            if current_size <= target_size_bytes:
                return image
            
            # 二分查找合适的尺寸和质量
            min_dimension = 100  # 最小尺寸限制
            max_dimension = max(image.width, image.height)
            current_dimension = max_dimension
            min_quality = 30  # 最低质量限制
            max_quality = quality
            current_quality = quality
            
            # 首先尝试降低质量
            while current_size > target_size_bytes and current_quality > min_quality:
                current_quality -= 5
                buffer = io.BytesIO()
                image.save(buffer, format=output_format, quality=current_quality)
                current_size = buffer.getbuffer().nbytes
            
            # 如果降低质量后仍然超过目标大小，开始降低尺寸
            while current_size > target_size_bytes and current_dimension > min_dimension:
                # 计算新尺寸
                scale_factor = 0.9  # 每次缩小10%
                new_dimension = int(current_dimension * scale_factor)
                
                # 调整图片大小
                if image.width >= image.height:
                    new_width = new_dimension
                    new_height = int(image.height * new_width / image.width)
                else:
                    new_height = new_dimension
                    new_width = int(image.width * new_height / image.height)
                
                resized_image = image.resize((new_width, new_height), Image.LANCZOS)
                
                # 检查新大小
                buffer = io.BytesIO()
                resized_image.save(buffer, format=output_format, quality=current_quality)
                current_size = buffer.getbuffer().nbytes
                
                # 更新当前尺寸和图片
                current_dimension = new_dimension
                image = resized_image
            
            return image
            
        except Exception as e:
            raise RuntimeError(f"处理图片时出错: {str(e)}")
    
    def batch_process(self, input_dir, output_dir, process_func, **kwargs):
        """
        批量处理图片
        
        参数:
            input_dir (str): 输入图片目录
            output_dir (str): 输出图片目录
            process_func (callable): 处理函数
            **kwargs: 传递给处理函数的参数
            
        返回:
            int: 成功处理的图片数量
        """
        # 检查输入目录是否存在
        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
            raise FileNotFoundError(f"输入目录不存在: {input_dir}")
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取所有图片文件
        image_files = [
            f for f in os.listdir(input_dir) 
            if os.path.isfile(os.path.join(input_dir, f)) and 
            any(f.lower().endswith(ext) for ext in self.supported_formats)
        ]
        
        # 如果没有图片文件
        if not image_files:
            raise ValueError(f"输入目录中没有支持的图片文件: {input_dir}")
        
        # 处理计数
        processed_count = 0
        
        # 批量处理图片
        for image_file in image_files:
            try:
                # 构建完整路径
                input_path = os.path.join(input_dir, image_file)
                
                # 构建输出路径
                output_filename = os.path.splitext(image_file)[0] + ".png"
                output_path = os.path.join(output_dir, output_filename)
                
                # 处理图片
                processed_image = process_func(input_path, **kwargs)
                
                # 保存结果
                processed_image.save(output_path)
                
                # 增加计数
                processed_count += 1
                
            except Exception as e:
                print(f"处理图片 {image_file} 时出错: {str(e)}")
        
        return processed_count
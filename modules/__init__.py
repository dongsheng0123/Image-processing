# 刘东升的图片处理工具 - 功能模块
# 此文件使modules目录成为一个Python包

# 导入所有功能模块，方便外部直接使用
from .background_remover import BackgroundRemover
from .image_processor import ImageProcessor
from .utils import (
    get_supported_formats,
    is_valid_image,
    get_image_info,
    ensure_dir,
    convert_image_format
)

# 版本信息
__version__ = '1.0.0'
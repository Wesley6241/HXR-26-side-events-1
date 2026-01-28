#!/usr/bin/env python3
"""
Pixel → Voxel - Data Ingest Script
自动处理 incoming/ 文件夹中的模型和缩略图文件
"""

import os
import json
import random
import string
import shutil
from pathlib import Path
from PIL import Image

# 配置常量
INCOMING_DIR = Path("incoming")
PUBLIC_DIR = Path("public")
MODELS_DIR = PUBLIC_DIR / "assets" / "models"
THUMBS_DIR = PUBLIC_DIR / "assets" / "thumbs"
DATA_DIR = PUBLIC_DIR / "data"
MODELS_JSON = DATA_DIR / "models.json"

# 文件大小限制（字节）
MAX_MODEL_SIZE = 50 * 1024 * 1024  # 50MB
MAX_IMAGE_SIZE = 4 * 1024 * 1024   # 4MB

# 支持的图片格式
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def generate_id(length=5):
    """生成唯一 ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def ensure_directories():
    """确保所有必要的目录存在"""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def parse_filename(filename):
    """
    解析文件名：ProjectName_AuthorName.ext
    返回 (title, author) 或 None（如果格式不正确）
    """
    name_without_ext = Path(filename).stem
    
    # 检查是否包含空格
    if ' ' in name_without_ext:
        return None, None, "contains space"
    
    # 分割文件名
    parts = name_without_ext.split('_')
    
    # 应该只有两部分：ProjectName 和 AuthorName
    if len(parts) != 2:
        return None, None, f"invalid format (expected: ProjectName_AuthorName, got {len(parts)} parts)"
    
    title, author = parts
    
    # 检查是否为空
    if not title or not author:
        return None, None, "empty title or author"
    
    return title, author, None


def find_thumbnail(glb_path):
    """查找对应的缩略图文件"""
    base_name = glb_path.stem
    
    for ext in IMAGE_EXTENSIONS:
        thumb_path = glb_path.parent / f"{base_name}{ext}"
        if thumb_path.exists():
            return thumb_path
    
    return None


def validate_file_size(file_path, max_size, file_type):
    """验证文件大小"""
    size = file_path.stat().st_size
    if size > max_size:
        size_mb = size / (1024 * 1024)
        max_mb = max_size / (1024 * 1024)
        return False, f"{file_type} exceeds size limit ({size_mb:.2f}MB > {max_mb}MB)"
    return True, None


def convert_to_jpg(image_path, output_path):
    """将图片转换为 JPG 格式"""
    try:
        img = Image.open(image_path)
        # 如果是 RGBA 模式，转换为 RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=85)
        return True, None
    except Exception as e:
        return False, f"Failed to convert image: {str(e)}"


def load_existing_models():
    """加载现有的 models.json"""
    if MODELS_JSON.exists():
        try:
            with open(MODELS_JSON, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('models', [])
        except json.JSONDecodeError:
            print(f"Warning: {MODELS_JSON} is corrupted. Starting fresh.")
            return []
    return []


def save_models(models):
    """保存 models.json"""
    data = {"models": models}
    with open(MODELS_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_duplicate(models, title, author):
    """检查是否已存在相同的 title_author 组合"""
    return any(m.get('title') == title and m.get('author') == author for m in models)


def process_files():
    """主处理函数"""
    # 确保目录存在
    ensure_directories()
    
    # 检查 incoming 目录是否存在
    if not INCOMING_DIR.exists():
        print(f"Error: {INCOMING_DIR} directory does not exist.")
        return
    
    # 查找所有 .glb 文件
    glb_files = list(INCOMING_DIR.glob("*.glb"))
    
    if not glb_files:
        print(f"No .glb files found in {INCOMING_DIR}")
        return
    
    print(f"Processing incoming files...")
    print(f"✓ Found {len(glb_files)} model files\n")
    
    # 加载现有模型
    existing_models = load_existing_models()
    
    # 处理结果
    processed = []
    errors = []
    skipped = []
    
    for glb_path in glb_files:
        glb_filename = glb_path.name
        
        # 解析文件名
        title, author, parse_error = parse_filename(glb_filename)
        if parse_error:
            errors.append(f"✗ Error: Invalid naming in {glb_filename} ({parse_error})")
            continue
        
        # 检查重复
        if is_duplicate(existing_models, title, author):
            skipped.append(f"⊘ Skipped: {glb_filename} (already exists in models.json)")
            continue
        
        # 查找缩略图
        thumb_path = find_thumbnail(glb_path)
        if not thumb_path:
            errors.append(f"✗ Error: Missing thumbnail for {glb_filename}")
            continue
        
        # 验证文件大小
        model_valid, model_error = validate_file_size(glb_path, MAX_MODEL_SIZE, "Model")
        if not model_valid:
            errors.append(f"✗ Error: {glb_filename} - {model_error}")
            continue
        
        image_valid, image_error = validate_file_size(thumb_path, MAX_IMAGE_SIZE, "Image")
        if not image_valid:
            errors.append(f"✗ Error: {thumb_path.name} - {image_error}")
            continue
        
        # 生成唯一 ID
        model_id = generate_id()
        
        # 确保 ID 唯一（虽然概率很低，但还是要检查）
        while any(m.get('id') == model_id for m in existing_models + processed):
            model_id = generate_id()
        
        # 目标路径
        target_glb = MODELS_DIR / f"{model_id}.glb"
        target_thumb = THUMBS_DIR / f"{model_id}.jpg"
        
        # 复制模型文件
        try:
            shutil.copy2(glb_path, target_glb)
        except Exception as e:
            errors.append(f"✗ Error: Failed to copy {glb_filename}: {str(e)}")
            continue
        
        # 处理缩略图（转换为 JPG）
        if thumb_path.suffix.lower() == '.jpg' or thumb_path.suffix.lower() == '.jpeg':
            # 已经是 JPG，直接复制
            try:
                shutil.copy2(thumb_path, target_thumb)
            except Exception as e:
                errors.append(f"✗ Error: Failed to copy thumbnail {thumb_path.name}: {str(e)}")
                continue
        else:
            # 需要转换
            success, error_msg = convert_to_jpg(thumb_path, target_thumb)
            if not success:
                errors.append(f"✗ Error: {error_msg}")
                # 清理已复制的模型文件
                if target_glb.exists():
                    target_glb.unlink()
                continue
        
        # 创建模型数据
        model_data = {
            "id": model_id,
            "title": title,
            "author": author,
            "glbPath": f"/assets/models/{model_id}.glb",
            "thumbPath": f"/assets/thumbs/{model_id}.jpg",
            "tags": []
        }
        
        processed.append(model_data)
        print(f"✓ {model_id}: {title}_{author} processed successfully")
    
    # 输出结果
    print()
    
    if skipped:
        for msg in skipped:
            print(msg)
        print()
    
    if errors:
        for error in errors:
            print(error)
        print("\nPlease fix the above issues and try again.")
        return
    
    if not processed:
        print("No new models to process.")
        return
    
    # 更新 JSON
    all_models = existing_models + processed
    save_models(all_models)
    
    print(f"✓ Updated models.json with {len(processed)} new model(s)")
    print(f"✓ Total models in database: {len(all_models)}")


if __name__ == "__main__":
    try:
        process_files()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

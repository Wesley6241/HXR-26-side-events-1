# Pixel → Voxel

将扫描影像转译为沉浸式三维体验的实时展示系统。

## 项目结构

```
hxr_SideEvent/
├── incoming/              # 输入文件夹（拖放文件到这里）
│   ├── ProjectA_Alice.glb
│   ├── ProjectA_Alice.jpg
│   └── ...
├── public/
│   ├── assets/
│   │   ├── models/       # 脚本生成的模型文件（<ID>.glb）
│   │   └── thumbs/       # 脚本生成的缩略图（<ID>.jpg）
│   └── data/
│       └── models.json   # 数据源（脚本自动更新）
├── ingest.py             # 主脚本
├── requirements.txt      # Python 依赖
└── README.md            # 使用说明
```

## 环境设置

### 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv
```

### 激活虚拟环境

**方法 1：使用批处理脚本（推荐，Windows）**
```bash
activate_venv.bat
```

**方法 2：手动激活**
```bash
# Windows (CMD):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

激活成功后，命令行提示符前会显示 `(venv)`。

### 安装依赖

**方法 1：使用批处理脚本（推荐，最简单）**
```bash
install_deps.bat
```

**方法 2：使用 pip（虚拟环境激活后）**
```bash
pip install -r requirements.txt
```

**方法 3：直接使用 Python 模块（无需激活）**
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**注意**：如果遇到 `pip` 命令无法识别的问题，使用方法 1 或方法 3。

## 使用流程

### 1. 准备文件

将模型文件和缩略图放入 `incoming/` 文件夹：

- **模型文件**：`.glb` 格式，≤ 50MB
- **缩略图**：`.jpg` / `.png` / `.jpeg` 格式，≤ 4MB

### 2. 文件命名规范

**必须遵守的命名规则**：

```
ProjectName_AuthorName.glb
ProjectName_AuthorName.jpg
```

**规则说明**：
- 使用单个下划线 `_` 分隔项目名和作者名
- 不要使用空格（用 `-` 代替）
- 不要在名字里再用 `_`（避免解析歧义）

**示例**：
```
FloatingMemory_Wenxin.glb
FloatingMemory_Wenxin.jpg
```

### 3. 运行 ingest 脚本

**方法 1：使用批处理脚本（推荐）**
```bash
run_ingest.bat
```

**方法 2：虚拟环境激活后**
```bash
python ingest.py
```

**方法 3：直接运行（无需激活）**
```bash
venv\Scripts\python.exe ingest.py
```

### 4. 查看结果

脚本会自动：
- 生成唯一 ID（如 `UTF91`）
- 复制并重命名文件到 `public/assets/`
- 将缩略图统一转换为 JPG 格式
- 更新 `public/data/models.json`

刷新前端页面即可看到新模型。

## 输出示例

**成功情况**：
```
Processing incoming files...
✓ Found 3 model files

✓ UTF91: ProjectA_Alice processed successfully
✓ A3F2K: ProjectB_Bob processed successfully
✓ X9M1P: ProjectC_Charlie processed successfully

✓ Updated models.json with 3 new model(s)
✓ Total models in database: 3
```

**错误情况**：
```
Processing incoming files...
✓ Found 3 model files

✗ Error: Missing thumbnail for ProjectA_Alice.glb
✗ Error: ProjectB_Bob.glb - Model exceeds size limit (75.23MB > 50MB)
✗ Error: Invalid naming in Project C_Dave.glb (contains space)

Please fix the above issues and try again.
```

## 数据格式

`models.json` 的数据结构：

```json
{
  "models": [
    {
      "id": "UTF91",
      "title": "FloatingMemory",
      "author": "Wenxin",
      "glbPath": "/assets/models/UTF91.glb",
      "thumbPath": "/assets/thumbs/UTF91.jpg",
      "tags": []
    }
  ]
}
```

## 功能特性

- ✅ 自动文件扫描和配对
- ✅ 文件大小校验（模型 ≤ 50MB，图片 ≤ 4MB）
- ✅ 命名规范校验
- ✅ 自动格式转换（PNG/JPEG → JPG）
- ✅ 重复检测（避免重复处理）
- ✅ 友好的错误提示

## 注意事项

1. **重复处理**：如果同一个 `ProjectName_AuthorName` 组合已存在于 `models.json`，脚本会跳过该文件
2. **文件保留**：处理完成后，`incoming/` 中的原始文件不会被删除，可以手动清理
3. **ID 生成**：每个模型会获得一个 5 位随机字符串作为唯一 ID（如 `UTF91`）

## 故障排除

### 问题：找不到 incoming 文件夹
**解决**：确保在项目根目录运行脚本，或手动创建 `incoming/` 文件夹

### 问题：Pillow 安装失败
**解决**：尝试使用 `pip install --upgrade pip` 更新 pip，然后重新安装

### 问题：虚拟环境激活失败或 pip 命令找不到
**解决**：
1. 使用提供的 `activate_venv.bat` 脚本激活
2. 或直接使用 `venv\Scripts\python.exe -m pip install -r requirements.txt` 安装依赖
3. 或使用 `venv\Scripts\python.exe ingest.py` 直接运行脚本

### 问题：路径编码错误（包含中文字符）
**解决**：如果项目路径包含中文字符导致问题，可以：
- 使用 `activate_venv.bat` 脚本
- 或直接使用完整路径运行：`venv\Scripts\python.exe ingest.py`

### 问题：文件处理失败
**解决**：检查文件命名是否符合规范，文件大小是否超限，以及是否有对应的缩略图文件
"# HXR-26-side-events-1" 

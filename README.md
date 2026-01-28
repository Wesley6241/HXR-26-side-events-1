# Pixel → Voxel

A real-time showcase system that translates scanned imagery into an immersive 3D experience.

## Project structure

```
hxr_SideEvent/
├── incoming/              # Input folder (drag & drop files here)
│   ├── ProjectA_Alice.glb
│   ├── ProjectA_Alice.jpg
│   └── ...
├── public/
│   ├── assets/
│   │   ├── models/       # Script-generated model files (<ID>.glb)
│   │   └── thumbs/       # Script-generated thumbnails (<ID>.jpg)
│   └── data/
│       └── models.json   # Data source (auto-updated by script)
├── ingest.py             # Main script
├── requirements.txt      # Python dependencies
└── README.md             # Documentation
```

## Environment setup

### Create a virtual environment (recommended)

```bash
# Create a virtual environment
python -m venv venv
```

### Activate the virtual environment

**Option 1: Use the batch script (recommended on Windows)**
```bash
activate_venv.bat
```

**Option 2: Activate manually**
```bash
# Windows (CMD):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

After activation, your prompt will show `(venv)`.

### Install dependencies

**Option 1: Use the batch script (recommended, simplest)**
```bash
install_deps.bat
```

**Option 2: Use pip (after activating the venv)**
```bash
pip install -r requirements.txt
```

**Option 3: Use the venv Python directly (no activation required)**
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**Note**: If `pip` is not recognized, use option 1 or option 3.

## Usage workflow

### 1. Prepare files

Put the model file and its thumbnail into the `incoming/` folder:

- **Model file**: `.glb`, ≤ 50MB
- **Thumbnail**: `.jpg` / `.png` / `.jpeg`, ≤ 4MB

### 2. File naming convention

**Required naming rule**:

```
ProjectName_AuthorName.glb
ProjectName_AuthorName.jpg
```

**Rules**:
- Use a single underscore `_` to separate project name and author name
- Do not use spaces (use `-` instead)
- Do not use additional `_` in the name (to avoid parsing ambiguity)

**Example**:
```
FloatingMemory_Wenxin.glb
FloatingMemory_Wenxin.jpg
```

### 3. Run the ingest script

**Option 1: Use the batch script (recommended)**
```bash
run_ingest.bat
```

**Option 2: After activating the venv**
```bash
python ingest.py
```

**Option 3: Run directly (no activation required)**
```bash
venv\Scripts\python.exe ingest.py
```

### 4. View results

The script will automatically:
- Generate a unique ID (e.g., `UTF91`)
- Copy and rename files into `public/assets/`
- Convert thumbnails to JPG format
- Update `public/data/models.json`

Refresh the frontend page to see the new model.

## Output examples

**Success**:
```
Processing incoming files...
✓ Found 3 model files

✓ UTF91: ProjectA_Alice processed successfully
✓ A3F2K: ProjectB_Bob processed successfully
✓ X9M1P: ProjectC_Charlie processed successfully

✓ Updated models.json with 3 new model(s)
✓ Total models in database: 3
```

**Error**:
```
Processing incoming files...
✓ Found 3 model files

✗ Error: Missing thumbnail for ProjectA_Alice.glb
✗ Error: ProjectB_Bob.glb - Model exceeds size limit (75.23MB > 50MB)
✗ Error: Invalid naming in Project C_Dave.glb (contains space)

Please fix the above issues and try again.
```

## Data format

Structure of `models.json`:

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

## Features

- ✅ Automatic file scanning and pairing
- ✅ File size validation (models ≤ 50MB, images ≤ 4MB)
- ✅ Naming convention validation
- ✅ Automatic format conversion (PNG/JPEG → JPG)
- ✅ Duplicate detection (avoid re-processing)
- ✅ Friendly error messages

## Notes

1. **Duplicate handling**: If the same `ProjectName_AuthorName` pair already exists in `models.json`, the script will skip it.
2. **Files are kept**: After processing, the original files in `incoming/` are not deleted. Clean them up manually if needed.
3. **ID generation**: Each model gets a 5-character random string as a unique ID (e.g., `UTF91`).

## Troubleshooting

### Issue: `incoming` folder not found
**Fix**: Run the script from the project root, or create the `incoming/` folder manually.

### Issue: Pillow installation failed
**Fix**: Try `pip install --upgrade pip`, then install again.

### Issue: venv activation failed or `pip` not found
**Fix**:
1. Use `activate_venv.bat` to activate
2. Or install deps via `venv\Scripts\python.exe -m pip install -r requirements.txt`
3. Or run the script via `venv\Scripts\python.exe ingest.py`

### Issue: Path encoding problems (non-ASCII characters)
**Fix**: If non-ASCII characters in the project path cause issues:
- Use `activate_venv.bat`
- Or run directly: `venv\Scripts\python.exe ingest.py`

### Issue: File processing failed
**Fix**: Check naming rules, file size limits, and that a matching thumbnail exists.

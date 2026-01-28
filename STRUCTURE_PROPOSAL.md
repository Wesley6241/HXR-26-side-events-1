# Pixel → Voxel - 项目结构方案评估

## 您提出的结构评估

### ✅ 优点
1. **清晰的页面分离**：Home / Archive / Detail 分离明确
2. **多入口配置**：适合 SEO 和独立页面部署
3. **组件复用**：Header/Footer 可以共享
4. **符合传统 Web 应用模式**：易于理解和维护

### ⚠️ 需要考虑的问题

1. **项目实际需求**：
   - Gallery Mode（球体星云）- 需要 3D 场景
   - Dive Mode（单作品空间）- 需要 3D 查看器
   - 语音召唤功能
   - Mesh ↔ Voxel 切换
   - 这些功能更适合单页应用（SPA）

2. **Three.js 集成**：
   - 需要 React Three Fiber (@react-three/fiber)
   - 3D 场景状态管理复杂
   - 页面切换可能导致 Three.js 资源清理问题

3. **路由需求**：
   - Gallery → Detail 需要平滑过渡
   - 可能需要 URL 参数传递模型 ID

## 推荐方案（结合您的需求和项目特点）

### 方案 A：SPA + React Router（推荐）

```
hxr_SideEvent/
├── public/
│   ├── assets/          # 现有资源
│   ├── data/
│   └── index.html       # 单入口
│
├── src/
│   ├── pages/
│   │   ├── Gallery.jsx      # Gallery Mode（球体星云）
│   │   └── Viewer.jsx       # Dive Mode（单作品空间）
│   │
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── ModelCard.jsx
│   │   ├── SphereGallery.jsx    # 球体星云组件
│   │   ├── ModelViewer.jsx      # 3D 查看器组件
│   │   ├── VoiceSearch.jsx      # 语音搜索
│   │   └── SearchBar.jsx        # 搜索框
│   │
│   ├── hooks/
│   │   ├── useModels.js         # 数据加载
│   │   ├── useVoice.js          # 语音识别
│   │   └── useViewer.js         # 3D 查看器状态
│   │
│   ├── utils/
│   │   ├── api.js               # 数据 API
│   │   └── pathFix.js           # 路径修复
│   │
│   ├── App.jsx                  # 路由配置
│   └── main.jsx                 # 入口文件
│
├── package.json
└── vite.config.js
```

**优点**：
- ✅ 平滑的页面过渡
- ✅ 共享状态管理（模型数据、3D 场景状态）
- ✅ React Three Fiber 集成更自然
- ✅ 适合复杂的交互需求

### 方案 B：多页应用（您提出的方案，适合简化版）

```
hxr_SideEvent/
├── public/
│   ├── index.html           # Gallery Mode
│   ├── viewer.html          # Dive Mode
│   ├── assets/
│   └── data/
│
├── src/
│   ├── pages/
│   │   ├── Gallery.jsx
│   │   └── Viewer.jsx
│   │
│   ├── components/
│   │   ├── SphereGallery.jsx
│   │   ├── ModelViewer.jsx
│   │   └── VoiceSearch.jsx
│   │
│   ├── shared/
│   │   ├── useModels.js     # 共享逻辑
│   │   └── threeUtils.js    # Three.js 工具
│   │
│   ├── main/
│   │   ├── gallery.js        # 挂载 Gallery.jsx
│   │   └── viewer.js         # 挂载 Viewer.jsx
│   │
│   └── lib/
│       └── three-setup.js    # Three.js 初始化
│
├── vite.config.js            # 多入口配置
└── package.json
```

**vite.config.js 示例**：
```js
export default {
  build: {
    rollupOptions: {
      input: {
        gallery: './public/index.html',
        viewer: './public/viewer.html',
      }
    }
  }
}
```

**优点**：
- ✅ 页面完全独立，易于部署
- ✅ 每个页面可以独立优化
- ✅ 适合 GitHub Pages 等静态托管

**缺点**：
- ⚠️ 页面切换会重新加载，丢失状态
- ⚠️ Three.js 资源需要重新初始化
- ⚠️ 状态传递需要 URL 参数

## 我的建议

### 根据项目需求，推荐 **方案 A（SPA）**，原因：

1. **Gallery Mode → Dive Mode 需要平滑过渡**
   - 球体旋转到目标模型
   - 3D 场景状态保持
   - 更好的用户体验

2. **状态管理需求**
   - 模型数据需要共享
   - 语音搜索结果需要传递
   - 3D 场景状态需要管理

3. **React Three Fiber 集成**
   - SPA 中更容易管理 Three.js 生命周期
   - 组件化 3D 场景更自然

### 但如果坚持多页方案，建议改进：

1. **使用 URL 参数传递状态**：
   ```
   /viewer.html?id=A5X07&mode=mesh
   ```

2. **共享工具库**：
   ```js
   // src/shared/modelLoader.js
   export async function loadModel(id) { ... }
   ```

3. **考虑使用 iframe 嵌入**：
   - Gallery 页面嵌入 Viewer iframe
   - 通过 postMessage 通信

## 最终推荐结构（SPA 版本）

```
hxr_SideEvent/
├── public/
│   ├── index.html
│   ├── assets/
│   └── data/
│
├── src/
│   ├── App.jsx                    # 主应用 + 路由
│   ├── main.jsx                   # 入口
│   │
│   ├── pages/
│   │   ├── GalleryPage.jsx       # Gallery Mode 页面
│   │   └── ViewerPage.jsx        # Dive Mode 页面
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   └── Footer.jsx
│   │   │
│   │   ├── gallery/
│   │   │   ├── SphereGallery.jsx    # 球体星云
│   │   │   ├── ModelNode.jsx        # 单个节点
│   │   │   └── VoiceSearch.jsx      # 语音搜索
│   │   │
│   │   └── viewer/
│   │       ├── ModelViewer.jsx      # 3D 查看器
│   │       ├── ModeToggle.jsx       # Mesh/Voxel 切换
│   │       └── ViewerControls.jsx   # 控制按钮
│   │
│   ├── hooks/
│   │   ├── useModels.js            # 模型数据
│   │   ├── useVoiceRecognition.js  # 语音识别
│   │   └── useViewerState.js       # 查看器状态
│   │
│   ├── stores/                     # 状态管理（可选 Zustand）
│   │   └── modelStore.js
│   │
│   └── utils/
│       ├── api.js
│       └── threeHelpers.js
│
├── package.json
└── vite.config.js
```

## 技术栈建议

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.8.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.88.0",
    "three": "^0.155.0",
    "zustand": "^4.4.0"  // 轻量状态管理
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "autoprefixer": "^10.4.0"
  }
}
```

## 总结

- **如果追求最佳用户体验和复杂交互** → 选择 **SPA 方案**
- **如果需要简单部署和独立页面** → 选择 **多页方案**（但需要处理状态传递）

您更倾向于哪种方案？我可以帮您搭建完整的项目结构。

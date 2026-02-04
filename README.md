# GitHub Pages 部署配置
# =========================================

## 🚀 快速部署到 GitHub Pages

### 方法 1：手动部署（推荐）

```bash
# 1. 进入 docs 目录
cd /root/.openclaw/workspace/docs

# 2. 初始化 Git 仓库
git init
git add .
git commit -m "feat: 添加 MuJoCo + LeRobot 训练指南"

# 3. 创建 GitHub 仓库并推送
#    访问 https://github.com/new 创建仓库，名称为: mujoco-lerobot-guide

# 4. 推送
git remote add origin git@github.com:你的用户名/mujoco-lerobot-guide.git
git push -u origin main
```

### 方法 2：使用 GitHub CLI

```bash
# 安装 GitHub CLI
curl -fsSL https://cli.github.com/packages/deb | sudo apt deb -

# 创建仓库并推送
cd /root/.openclaw/workspace/docs
gh repo create mujoco-lerobot-guide --public --source=. --push
```

### 方法 3：使用 Python 脚本

编辑配置并运行：

```bash
# 创建配置文件
cat > /root/.openclaw/workspace/docs/github_config.yaml << 'EOF'
github:
  owner: "你的GitHub用户名"
  repo: "mujoco-lerobot-guide"
  token: "ghp_你的PersonalAccessToken"
EOF

# 运行部署脚本
python /root/.openclaw/workspace/docs/deploy.py
```

---

## 📋 GitHub Pages 启用步骤

### 1. 创建仓库后

访问仓库 → Settings → Pages → Source: "main" branch → /docs folder → Save

### 2. 访问你的网站

```
https://你的用户名.github.io/mujoco-lerobot-guide/
```

### 3. 首次部署提示

- 首次推送后可能需要 1-2 分钟
- 可以在 Actions 标签查看部署状态

---

## 🔧 故障排除

### Q: 页面无法访问

1. 检查 Settings → Pages 是否正确配置
2. 确认 index.html 在 docs/ 文件夹根目录
3. 等待 2-5 分钟让 GitHub 处理

### Q: 样式丢失

确保所有 CSS 都在 index.html 内联（已配置）

### Q: 推送失败

```bash
# 检查远程仓库
git remote -v

# 如果需要更新远程
git remote set-url origin git@github.com:用户名/仓库名.git
```

---

## 📁 文档文件结构

```
docs/
├── index.html          # 主页面（已生成）
├── README.md          # 说明文件
├── deploy.py          # 部署脚本（可选）
└── github_config.yaml # GitHub 配置（模板）
```

---

## ✨ 更新文档

修改 index.html 后：

```bash
cd /root/.openclaw/workspace/docs
git add .
git commit -m "docs: 更新训练指南"
git push
```

GitHub Pages 会自动更新！

---

## 🔒 安全提示

- **不要提交 token** 到公开仓库
- 使用 Personal Access Token (Classic)
- 权限: repo + admin:repo_hook

---

## 📞 获取帮助

- <a href="https://docs.github.com/en/pages" target="_blank">GitHub Pages 文档 →</a>
- <a href="https://cli.github.com/manual/" target="_blank">GitHub CLI 文档 →</a>

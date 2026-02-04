#!/usr/bin/env python3
"""
GitHub Pages 部署脚本
用于将 docs 文件夹推送到 GitHub
"""

import os
import subprocess
import yaml

def run_cmd(cmd, cwd=None):
    """执行命令"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ 命令失败: {cmd}")
        print(f"输出: {result.stdout}")
        print(f"错误: {result.stderr}")
        return False
    return True

def load_config():
    """加载配置"""
    config_path = "github_config.yaml"
    if os.path.exists(config_path):
        with open(config_path) as f:
            return yaml.safe_load(f)
    return None

def main():
    print("=" * 60)
    print("🚀 GitHub Pages 部署")
    print("=" * 60)
    
    # 检查 Git
    if not run_cmd("git --version"):
        print("❌ 未安装 Git")
        return
    
    # 加载配置
    config = load_config()
    
    # 检查是否已初始化
    if not os.path.exists(".git"):
        print("\n📦 初始化 Git 仓库...")
        if not run_cmd("git init"):
            return
        if not run_cmd('git commit -m "feat: 初始化文档仓库"'):
            return
        print("✅ Git 仓库初始化完成")
    else:
        print("✅ Git 仓库已存在")
    
    # 检查远程仓库
    result = subprocess.run(
        "git remote get-url origin 2>/dev/null || echo ''",
        shell=True, capture_output=True, text=True
    )
    
    if not result.stdout.strip():
        if config and config.get('github'):
            remote_url = f"https://{config['github']['token']}@github.com/{config['github']['owner']}/{config['github']['repo']}.git"
            print(f"\n🔗 添加远程仓库...")
            if not run_cmd(f'git remote add origin {remote_url}'):
                return
        else:
            print("\n⚠️  未配置远程仓库")
            print("请先在 GitHub 创建仓库，然后运行:")
            print('  git remote add origin https://github.com/用户名/仓库名.git')
            return
    
    print("\n📤 推送到 GitHub...")
    if not run_cmd("git push -u origin main"):
        print("❌ 推送失败")
        print("\n💡 可能需要先在 GitHub 创建仓库")
        print("   访问: https://github.com/new")
        return
    
    print("\n✅ 推送成功!")
    print("\n📝 下一步:")
    print("   1. 访问 GitHub 仓库 Settings → Pages")
    print("   2. Source: main branch → /docs folder")
    print("   3. 保存后等待 1-2 分钟")
    print("   4. 访问: https://用户名.github.io/仓库名/")

if __name__ == "__main__":
    main()

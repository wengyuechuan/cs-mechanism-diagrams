# Git 仓库使用说明

本目录是独立 Git 仓库，日常命令均在仓库根目录执行。远程 `origin` 已连接到 [wengyuechuan/cs-mechanism-diagrams](https://github.com/wengyuechuan/cs-mechanism-diagrams)。项目入口见 [README.md](README.md)。

## 版本控制范围

跟踪完整可迁移 skill 及 271 张 PNG、223 张论文机制参考的 PNG/SVG 与来源元数据、48 套 drawio/SVG/PNG/JSON 蓝图、离线图库、分类索引、采集/构建脚本和检查记录。论文图片保留原作者和出版商权利，原创材料许可见 `LICENSE_TEMPLATES.txt` 与 skill 的 `LICENSE.txt`；建立 Git 仓库不改变这些许可。

原论文 PDF、整页预览、依赖缓存、HTTP 缓存、重复 ZIP 和解压测试副本在本机保留，但被 `.gitignore` 排除。源 PDF 共约 645 MB；它们的网址、SHA-256、页数和版本备注仍保存在 `metadata/papers.json`。

因此，克隆仓库后可直接离线浏览 `风格图库.html`、编辑模板、使用完整 skill；原 PDF/整页预览入口需要先另行取得对应文件。下载目录中的历史主题名称可能与人工修正后的主题标签不同，当前分类以风格图库与索引为准。

## 日常维护

在本仓库目录执行：

```powershell
git status
git diff
git add <修改的文件或目录>
git commit -m "Describe the library update"
git log --oneline
```

首次提交使用 `Codex <codex@local.invalid>` 的本地工具署名，没有修改全局 Git 配置。自己的后续提交可在本仓库设置真实作者：

```powershell
git config --local user.name "你的姓名"
git config --local user.email "你的提交邮箱"
```

## 构建与检查

Skill 检索脚本只用 Python 标准库：

```powershell
python agent-skill/cs-mechanism-imagegen/scripts/library.py verify
python qa/test_skill_tools.py
```

重建图库/模板预览需要 `requirements.txt` 中的依赖。可以在虚拟环境中安装，或使用本机已保留但不入 Git 的 `tools/vendor/`。

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python tools/build_style_library.py
.venv/Scripts/python tools/build_gallery.py
.venv/Scripts/python tools/package_style_skill.py
```

`tools/validate_library.py` 验证全量本地资料，包含被忽略的 PDF 与整页预览，故只在相应本地源文件齐备时运行。`collect_library.py` 是重采集工具，会生成新的待审候选，不应为了补充几个 PDF 直接对已复核元数据做完整重采集。

## 远程仓库

远程仓库地址为 `https://github.com/wengyuechuan/cs-mechanism-diagrams.git`，分支为 `main`。223 张论文参考的逐图再分发核验尚未完成，记录见 [第三方素材说明](THIRD_PARTY_NOTICES.md) 与 `metadata/rights_review.json`。初始提交已包含参考图，只在新提交中删除不能清除历史中的图片。后续更新可在本仓库提交后推送：

```powershell
git push -u origin main
```

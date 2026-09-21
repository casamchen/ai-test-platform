# GitHub Push Guide · 上传到 GitHub 步骤

> 适用项目：`AI Test Management Platform`（位于 `/Users/casamchen/Desktop/桌面 - Casam的笔记本电脑/aitest`）
> 目标：`https://github.com/<your-username>/ai-test-platform`

---

## ⚠️ Step 0 — 先做这两件安全的事

1. **立刻改 GitHub 密码**——你之前把密码发在了对话里。GitHub 设置 → Password and authentication → Change password。
2. **开启 2FA**（两步验证）——Settings → Password and authentication → Two-factor authentication。

> GitHub 自 2021 年 8 月起**不再支持密码 push / clone**。本次 push 必须用 Personal Access Token（PAT）替代密码。

---

## Step 1 — 在 GitHub 创建空仓库

浏览器 → 右上角 `+` → **New repository**

| 字段 | 填写 |
|---|---|
| Repository name | `ai-test-platform` |
| Description | `AI Test Management Platform — full-stack RAG + LoRA + Zhipu AI for auto-generating test cases from requirement docs.` |
| Visibility | ✅ **Public**（recruiter 能看到） |
| Initialize | ❌ **不要**勾选 Add a README / .gitignore / license（脚本里已经有） |

点 **Create repository**。

---

## Step 2 — 生成 Personal Access Token

浏览器 → 右上角头像 → **Settings** → 左侧最下方 **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token** → 选 **classic**

| 字段 | 填写 |
|---|---|
| Note | `ai-test-platform local push` |
| Expiration | 选 30 days 或更短（更安全） |
| Scopes | 勾选 **`repo`** 即可 |

点 **Generate token** → **立即复制 token**（它只显示一次，格式像 `ghp_xxxxxxxxxxxxxxxxxxxx`）。

---

## Step 3 — 第一次 push（推荐用脚本）

打开终端，进入项目目录：

```bash
cd "/Users/casamchen/Desktop/桌面 - Casam的笔记本电脑/aitest"

# 让 push.sh 可执行
chmod +x push.sh

# 运行 push.sh，把 token 通过环境变量传进去（不会硬编码到脚本）
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxx \
GITHUB_USER=你的GitHub用户名 \
./push.sh
```

> 替换 `ghp_xxxxxxxxxxxxxxxxxxxx` 为 Step 2 拿到的真实 token。
> `GITHUB_USER` 填你的真实 GitHub 用户名（不是邮箱）。

脚本会做这些事：

1. **安全检查** — `.env` 没被列入 push、`node_modules/` 被排除、没漏掉 `vectorsFrame/`、没硬编码 API key
2. **估算大小** — 列出 git 会 push 的文件清单
3. **两次确认** — 第一次问你 push 到哪，第二次显示具体文件再确认一次
4. **初始化** — `git init`、设置 user.name / user.email（如未配置）、添加/更新 remote
5. **提交推送** — `git add` + `git commit` + `git push -u origin main`

---

## Step 4 — 验证 push 成功

1. 浏览器打开 `https://github.com/你的用户名/ai-test-platform`
2. 应该能看到 README 自动渲染在首页
3. 文件数应该在 80-150 个之间（不算 node_modules / vectorsFrame / screenshot / record）
4. **检查 `.env` 没有出现在文件列表里**（如果出现了，立刻删除仓库、轮换 token）

---

## Step 5 — 仓库美化（让仓库看起来更专业）

### 5.1 仓库描述 + Topics
在 GitHub 仓库页右上角 ⚙️ → 设置 Description + Topics：

- Description: `AI Test Management Platform — full-stack RAG + LoRA + Zhipu AI for auto-generating test cases from requirement docs.`
- Topics: `python` `django` `vue` `ai` `rag` `lora` `test-automation` `zhipuai` `element-ui` `faiss`

### 5.2 Pin 到 Profile
GitHub 个人主页 → 选 "Customize your pins" → 勾选 `ai-test-platform`

### 5.3 在简历和求职信里加这个仓库链接

例如：

```
GitHub: github.com/jiasheng-chen/ai-test-platform
```

---

## 高级用法

### 推送到指定分支
```bash
GITHUB_PAT=ghp_xxx BRANCH=release/v1.0 ./push.sh
```

### 只想 dry-run 检查（不实际 push）
```bash
bash -c 'GITHUB_PAT=dry-run-just-for-checks ./push.sh' < /dev/null
# 或者在脚本提示 "Continue? [y/N]" 时直接 Ctrl-C 退出
```

### 推完之后想撤销（强制）
```bash
git push -f origin HEAD~1:main   # 删掉最近一次 commit
```

---

## 常见错误

| 错误 | 原因 | 修复 |
|---|---|---|
| `403 Permission denied` | Token 没勾 `repo` 权限 / 仓库名不对 | 重新生成 token + 检查仓库名 |
| `Repository not found` | 用户名拼错 / 仓库没创建 | 在 GitHub 创建仓库 / 检查大小写 |
| `failed to push some refs` | 远端有本地没有的 commit | `git pull --rebase origin main` 后再 push |
| `.env` 被错误 push 了 | `.gitignore` 没生效 | `git rm --cached .env` + `git commit --amend` + 立刻轮换 token |

---

## 安全 checklist（提交前再过一遍）

- [ ] `.env` 没有出现在 git status 里
- [ ] `.gitignore` 包含 `node_modules/` `vectorsFrame/` `__pycache__/` `*.rdb`
- [ ] `aitestapp/screenshot/` `aitestapp/record/` `aitestapp/interface_file/` 都没出现
- [ ] 没有 .docx / .xlsx / 业务数据被加入仓库
- [ ] 没有 API key 硬编码在代码里（应该用 `os.getenv`）

脚本 `push.sh` 已经把这些检查自动化了。
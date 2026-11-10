# Muse 备份包 — 恢复说明

打包日期：2026-11-11（按 X 文章《复活你的 Muse：Agent 备份保姆级攻略》的五步法执行）
包内共 285+ 个文件，约 19MB（未压缩）。

## 包里有什么（对应文章的档案结构）

- `profile/` —— 个人档案与指令
  - `USER.md`：kuai 的基本信息（姓名郑日坤、称呼 kuai）
  - `MEMORY.md`：长期记忆主文件（事实、偏好、承诺）
  - `SOUL.md` / `AGENTS.md` / `IDENTITY.md`：助手人格与操作守则（含骚扰取证「够用即止」规则）
  - `PROACTIVE_PREFERENCES.md`：主动提醒偏好与禁区
- `memory-files/` —— 记忆库
  - `memory/`：每日日志、人物档案（memory/people）、群组档案（memory/groups）
  - `dreams/`：对齐综述（ALIGNMENT_SYNTHESIS 等）
  - `config/`：技能偏好配置
- `skills/` —— 自定义技能（custom-skills：x_draft_batches、douyin_comment_campaign、cloud_account_action_safety 等）
- `projects/` —— 项目文件
  - `goals/`：全部目标工作区（X 运营、VPN、装修、公众号、求职、哥哥罚金案、土地退款相关等），含隐藏工作文件
  - `your_files/`：已交付文档（含购地协议照片整理、购地退款案件要点）
  - `zheng-chao-song/`：郑超松罚金延期申请书与寄出清单
  - `objectives/`：目标学习状态

## 有意排除的（丢了可重建，不是家当）

- VPN 目标里的 `xray.zip`、`xray_bin/` 二进制与各类 `*.log` 日志（可重新下载/生成）
- `workspace/user/media_library/`（kuai 上传的照片原图，79MB，原图在他手机里）
- 浏览器缓存、临时文件、系统日志

## ⚠️ 安全警告

`projects/goals/vpn/hidden_files/` 里含服务器节点凭据、面板密码，以及 kuai 的服务器 SSH 私钥副本（kuai_server_key.pem）。
**这个包只能存本地/U盘/自己的加密云盘，绝不要发到公开网盘链接、不要转给任何人。**

## 怎么恢复（换号/新环境时）

1. 把本包文件发给新的 Muse；
2. 对它说：「这是我之前备份的 Muse，请读完这份档案（先读 00-RESTORE-README.md、profile/USER.md、profile/MEMORY.md 和 memory-files/dreams 里的对齐综述），告诉我你现在知道关于我的哪些事，看起来和之前的我像吗？」
3. 核对无误后，让它把 profile/ 与 memory-files/ 的内容写回新环境对应位置，skills/ 与 projects/ 放回 workspace。

## 更新节奏

- 已按文章最后一条设置：每天约 23:00 自动重新打包到同一目录（workspace/backups/），覆盖旧包；
- 每月做一次「备份体检」：核对 MEMORY.md、技能与目标进度是否为最新版。

## GitHub 版说明（仅本仓库副本适用）

- 图片、docx、pdf、音频等二进制文件在本仓库中以「原路径 + .b64」的 base64 文本形式保存，清单与校验值见根目录 `BINARIES-INDEX.md`，恢复时按其中命令解码还原。
- 本地原始备份包（muse-backup-2026-11-11.tar.gz）含未编码的原文件，两边内容一致。

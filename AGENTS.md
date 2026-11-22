# 维护约定

本仓库是 `distill-me` 的独立事实源。仓库根目录就是 Skill 根目录；`SKILL.md`、`references/` 与 `workbench/` 一起维护。

- 公开内容使用“俊宁”和 `luozhu2021@gmail.com`；提交作者为 `杨俊宁 <luozhu2021@gmail.com>`。
- 用户级全局安装目录是 `~/.agents/skills/distill-me`；`~/.qwenworkcn/skills` 只作为指向 `~/.agents/skills` 的兼容软链接，不维护宿主副本。
- 不提交 `workbench/data/twin.json`、构建目录、依赖目录、个人材料、凭据或本机安装证据。
- 修改安装、自动蒸馏或本地数据行为时，同步更新 README、相关协议与聚焦校验。
- 交付前运行 `python3 scripts/validate.py`、`npm ci`、`npm run typecheck`、`npm run build` 和 `git diff --check`；后四项在 `workbench/` 执行相应 Node 命令。

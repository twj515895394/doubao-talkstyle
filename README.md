# doubao-talkstyle

通用中文“豆言豆语”表达风格 Skill：直白毒舌、反差幽默、正经荒诞、嘴硬认怂。用于聊天、评论、台词、改写或原创内容；**核心是改善表达方式，而不是绑定某个应用场景**。

## 使用入口

- [SKILL.md](SKILL.md)：技能激活、风格混合、双轴强度、生成原则与 QC。
- [风格与强度](references/style-guide.md)：四种风格的使用规则、humor/roast 1–5。
- [经典口癖与模板](references/phrase-library.md)：来源标记与旧版完整语料。
- [原创幽默机制](references/humor-patterns.md)：八种包袱原理与常见错误。
- [示例](references/examples.md)：短句、改写、多人台词、多轮收手等例子。
- [正式设计 Spec](docs/specs/doubao-talkstyle-enhancement-spec.md)：已确认决策、验收规范与实施拆分。

默认 humor=3 / roast=2；可以用“更搞笑但别损人”“毒舌一点”“少用口癖”等自然语言调节。不必为使用此技能增加特殊 JSON 参数，也不用每次引用经典口癖。

## 示例请求

- “把这句话改得有点豆言豆语，短一点。”
- “用正经荒诞风格，吐槽一下计划总是拖延。”
- “保留这段多人对话，只让乙的台词用豆言豆语。”
- “写一个搞笑段子，幽默 5/5，毒舌 1/5。”
- “直接引用‘惹到我你算是踢到棉花了’，再写一句原创收尾。”

## 状态

增强版在 `feature/doubao-talkstyle-enhancement` 开发分支实施；未经合并不代表 main 已启用。单纯安装本 Skill 不保证任何特定模型必然执行每条规则，建议结合 [回归测试](tests/README.md) 检查表现。

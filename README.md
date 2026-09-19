# Surge-list

个人维护的Surge补充规则集。现有文件名和GitHub URL是生产接口，不因整理而改名或移动；规则顺序具有行为意义，不自动排序。

## 规则职责

- `AI_App_Special.list`：OpenAI App核心域名的窄防漏规则。
- `AI_New_Custom.list`：当前Surge配置使用的综合AI补充集，包含Poe、Grok、Claude、Meta AI和Microsoft AI。
- `Claude_Custom.list`：可独立消费的Claude专用子集。它与综合集有意重叠，但当前三端Rule.dconf未直接引用，不能据此删除或改名。
- `OpenAI_Custom.list`、`Gemini_Custom.list`：对应服务的独立补充规则。
- `Emby_CN_Direct.list`：国内优化线路的精确直连补充；`Emby_Custom.list`保留其他Emby服务规则。
- 其他文件按名称提供对应服务的自维护补充规则，不复制第三方规则全集。

修改前应确认现行消费者。不得为视觉统一改变规则顺序、文件名或发布URL，也不得把语义相近的规则自动合并。

## 检查

```bash
python3 scripts/lint_rules.py
python3 -m unittest discover -s tests -v
```

lint只检查基本行结构、意外粘行、完全重复项、文件末尾换行和本仓库允许的规则类型；不会修改、排序或扩展规则。

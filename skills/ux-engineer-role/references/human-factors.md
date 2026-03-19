# Human Factors Notes

## Purpose

在需要把 UX 建议建立在人类视觉与认知约束之上时，读取本文件。以下内容用于支持判断，不是要求把学术术语原样塞进用户答复。

## Core Notes

### Central Vision And Foveal Priority

- 中央视觉区域承担最高精度识别能力；关键指标、主要动作、关键状态应尽量围绕注视点布置。
- 当用户必须在屏幕两端来回扫视才能比较或决策时，理解成本会上升。
- 设计含义：把主指标与其解释、主动作与其风险提示、输入项与其即时反馈尽量放在邻近位置。

来源：
- NCBI Bookshelf, Webvision: https://www.ncbi.nlm.nih.gov/books/NBK11556/

### Peripheral Vision Crowding

- 周边视觉在拥挤场景下更容易发生 crowding，邻近对象会更难区分。
- 设计含义：不要把高相似度标签、数值、图标、按钮无间距地堆在一起；用留白和分组让对象先形成结构，再让用户扫视。

来源：
- PMC, Crowding in peripheral vision: https://pmc.ncbi.nlm.nih.gov/articles/PMC3045113/

### Working Memory Is Narrow

- 工作记忆中的注意焦点容量有限，经典现代综述常把纯容量限制概括为大约 4 个 chunk。
- 设计含义：避免要求用户同时记住过多字段、步骤、比较对象或状态；优先分块、摘要、默认值、逐步展开。

来源：
- Cowan, 2001: https://memory.psych.missouri.edu/assets/doc/articles/2001/cowan-bbs-2001.pdf

### Transient Visual Persistence Is Brief

- 视觉暂留与图像记忆是短暂且脆弱的，重要信息不应只通过一闪而过的状态传递。
- 设计含义：不要让关键通知、校验错误、异步成功状态只短暂出现后消失；提供稳定可回看的状态位。

来源：
- Nature, Temporal characteristics of iconic memory: https://www.nature.com/articles/267241a0
- Oxford Academic, Visual Sensory Memory: https://academic.oup.com/book/9546/chapter/156544487

### Flash Safety

- Web 内容不应在 1 秒内闪烁超过 3 次，超阈值闪烁会引发明显无障碍风险。
- 设计含义：避免高频闪烁、爆闪警报、快速红闪；异常提示优先使用稳定高对比状态和可控动画。

来源：
- W3C WAI, SC 2.3.1: https://w3c.github.io/wcag/understanding/three-flashes-or-below-threshold.html

## Translation To UX Practice

- 先定主锚点，再排邻近关系，再补充颜色和图标。
- 先压缩决策路径，再压缩像素占用。
- 先让用户看懂结构，再让用户读文案。
- 先让状态稳定可回看，再讨论动效表现。
- 先减记忆负担，再要求用户学习规则。

## Source Priority

- 优先使用官方规范、学术论文、综述、政府或大学资料。
- 竞品案例只能说明“有人这么做”，不能单独作为“这样做是对的”的证据。
- 对生物学或心理学解释保持克制，只引用足以支持设计判断的部分，避免过度外推。

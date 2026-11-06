# 凯尔希示例资料来源

角色履历按《明日方舟》凯尔希的公开角色介绍、干员档案和语音内容改写为简历结构；示例中的栏目划分与履历表达由本项目整理。

- 官网角色介绍：https://ak.hypergryph.com/ （凯尔希：罗德岛管理者、医疗部门负责人、阿米娅的直接辅导者）
- BWIKI干员资料：https://wiki.biligame.com/arknights/凯尔希 （客观履历、医学专精、跨学科学识与行动语音）
- PRTS档案：https://prts.wiki/w/凯尔希 （基础档案、行动记录与任务配合）
- 官网立绘：https://web.hycdn.cn/arknights/official/_next/static/media/kaltsit.05c0f5e1.png

检索日期：2026-11-06。图片保留官网原文件，HTML以证件照框进行显示裁切。角色及立绘来自《明日方舟》/鹰角网络。

## 新增经历的事实对应

- 亚叶档案：https://wiki.biligame.com/arknights/亚叶 与 https://prts.wiki/w/Folinic ：凯尔希过问两年学习各环节、通过医疗许可后安排结业证明；身体评测后同意进入预备训练营，亚叶半年后开始外派。半年训练由预备训练营承担。
- 《遗尘漫步》剧情：https://moegirl.icu/明日方舟/剧情/遗尘漫步 ：高级行动顾问兼术师教练身份、荒漠救援与保护艾利奥特、目标物品及后续旅途。
- 剧情概览：https://moegirl.uk/凯尔希 ：资源短缺、多方追逐、沁礁黑市与当地联系人。职位以剧情对白中的“高级行动顾问兼术师教练”为准。

## 两份示例

- `layout-input.json` → `previews/kaltsit-max-10.5pt.html/.pdf`：精简履历，正文10.5pt、辅助信息9.25pt。
- `layout-input-min.json` → `previews/kaltsit-min-9pt.html/.pdf`：扩展履历，补充医疗培养、前线资格衔接、萨尔贡任务和健康管理细节；正文9pt、辅助信息8.5pt。

两份采用同一照片、默认浅蓝绿、同一标题层级及页边距；两份采用2.2.0默认间距（板块4.5mm、经历3mm、条目0.8mm）。示例固定边界字号；实际用户简历从10.5pt开始，以0.25pt递减至9pt选择可容纳内容的最大字号。

2.2.0更新：技能采用分类标签行，标题下通栏细线。示例不虚构日历日期，实际年月对齐另由模板测试覆盖。

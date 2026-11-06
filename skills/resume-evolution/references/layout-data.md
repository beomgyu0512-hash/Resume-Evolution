# 排版输入 JSON
根字段：name（必填）、target、contact_lines（字符串数组）、contact_links（可选，最多3项{label:短显示文字,url:完整HTTP(S)地址}，合占一个联系信息行）；contact_lines加链接行合计最多3行、theme（teal默认）、photo（本地png/jpeg路径，可省略）、show_photo（默认true）、sections（数组）。
每个section：title（必填）、entries（数组）。每个entry：name、date、meta、bullets、lines、split_across_pages（默认false）。name必填；仅有lines的技能组可省略name。date存在时name必填。
每条bullet：字符串，或{text:字符串, emphasis:[原文中的短语，最多2项]}。每条lines：{label:类别名称,text:已确认的具体内容}，不加圆点；用于“编程与环境：Python、Linux”等技能分类，不生成熟练度图形。
日期在左、名称在右，由模板决定，禁止在字符串中用空格凑列。meta以“技术栈：”等标签开头时模板自动加粗该标签；每个项目最多一行技术栈，必要时自然换行。
单条经历实际高于可用页高时设置split_across_pages=true，允许按条目分页；其他经历默认保持完整。不得用该字段绕过字号下限。
只放已确认且允许交付的简历内容。HTML自动转义所有文字，emphasis匹配原文短语并加粗。照片相对路径以JSON文件目录解析，图片嵌入HTML；不接受远程图片URL。
--draft允许无照片的带标记预览；缺少照片的完成版需补图或用户明确选择--no-photo。不收集用户个人简历、联系方式或照片到Skill或公开examples中。示例使用虚构数据。

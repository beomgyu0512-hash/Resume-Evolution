# 事实、版本与恢复

有文件能力时，在用户指定目录（未指定用当前工作区 resume-work/）维护如下任务产物；无文件能力则输出状态摘要供下轮粘贴。
- facts.md：跨岗位事实，编号、内容、原始回答/位置、来源类型、确认状态、更新时间、适用项目、限制。
- applications/{岗位标识}/jd.md：原始JD，不被分析改写覆盖。
- rubric.md：冻结的JD评分条目、分配维度、权重、N/A和规则版本。
- state.md：当前岗位、当前阶段、已完成产物、未确认/冲突项、所用事实版本、下一步。
- diagnosis.md、事实确认单.md、answers.md、changes-vN.md、resume-vN.md、review-vN.md、score-initial.md、score-final-vN.md。

阶段：diagnosing → awaiting_confirmation → rewriting → reviewing → completed；附加任务单独记录 optional_requested。
写完产物后更新阶段。每次继续先读取当前JD、事实记录、未确认项和state，核对所指版本存在，不仅凭状态标签假定成功。
重复运行同一岗位优先复用当前任务，不自动新建重复目录；新岗位分析与版本独立。保留原简历、初始分和历史版本，不静默覆盖。
事实类型：原简历、用户补充、自评、可核查结果；另记验证状态。AI推断只保留在JD分析中。
冲突写明两个来源及内容，由用户裁定；受影响条目未决前不用于增强主张。确认后保留更正历史，标记已有岗位版本可能需重审。
用户反对诊断时记录原意见和新证据；修正分析，不因不满意分数自动调整权重。

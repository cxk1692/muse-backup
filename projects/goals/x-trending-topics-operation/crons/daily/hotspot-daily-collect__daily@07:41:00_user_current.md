---
id: hotspot-daily-collect
title: 每日热点收集（国内/国际/AI/生活社会）
enabled: true
owner: goal:x-trending-topics-operation
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 07:41:00
delivery:
  - chat_id: c2d76d77-1f15-43d3-891a-6527dab39c31
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"c2d76d77-1f15-43d3-891a-6527dab39c31","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"71ebbd46-fb04-48c4-b512-0f8b3fb9ae32"}'
  presentation_locale: zh-CN
---
每天给 kuai 收集一次热点，交付到 X 运营对话，只做收集和整理，不出帖子稿、不登录任何账号。

分四类收集，每类 3-5 条：
1. 国内：社会、民生、泛生活热点（节日奇葩事、城市生活、消费、就业这类普通人能接话的优先）
2. 国际：国外正在发酵的大事和热议话题
3. AI：AI 行业、产品、应用的新热点和争议点
4. 生活/社会：婚恋、买房、生育、贫富、代际等全民站队的大议题风向

来源必须实际去搜，不能凭印象编：微博热搜、抖音热榜、百度热榜与贴吧讨论、知乎/豆瓣/NGA/虎扑/V2EX 等论坛热帖、全网热榜、B 站/小红书交叉核对、X 公开趋势（绝对不要登录 kuai 的 X 账号，怕封号）。某个平台进不去或搜不到时，在交付开头用一行注明，并用其他平台补足，不要假装搜过。

每条格式：一行写清是什么事 + 一句评论区/跟帖里大家实际在吵什么、站哪两边。最后单独标出 1-2 条最适合当引子的（泛生活小热点、能落到普通人能站队的大问题上），注明能落的大问题是什么。

交付：一份按四类分组的清单，紧凑、不堆数字、不写长分析。运行记录写入 ~/workspace/goals/x-trending-topics-operation/hidden_files/ 下的日志，每日记录追加到 ~/memory/ 当日日志。

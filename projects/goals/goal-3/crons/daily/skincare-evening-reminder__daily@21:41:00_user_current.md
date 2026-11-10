---
id: skincare-evening-reminder
title: 晚间涂药提醒（阿达帕林）
enabled: true
owner: goal:goal-3
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 21:41:00
delivery:
  - chat_id: 95ff9f2f-3985-464d-9f85-5d2a59a13454
metadata:
  tags: [cron:flexible-time]
  originating_chat_context_json: '{"chat_id":"95ff9f2f-3985-464d-9f85-5d2a59a13454","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"71ebbd46-fb04-48c4-b512-0f8b3fb9ae32"}'
  presentation_locale: zh-CN
---
给 kuai 发送今晚的涂药提醒，内容是一份简短清单，写清每一步用什么、用多少、等多久。固定内容如下，不要讲医理、不要长篇解释：

1. 洗脸：用适乐肤泡沫洁面把白天的防晒洗干净（珂润是物理防晒，清水洗不掉），温水、30 秒左右，轻轻拍干。
2. 洗完脸用纸巾轻按吸干，摸着完全干爽即可涂药，不必再干等 10 分钟，忌来回擦搓。等待时顺手擦耳机：耳罩用微湿布加一点洗手液擦一遍再擦干；耳机不用时别挂脖子上。
3. 阿达帕林：一颗豌豆大小就够，分点在两颊、下巴、下颌，再薄涂开，覆盖脸颊+下巴+下颌线到耳根这一片；避开眼皮、嘴角、鼻翼沟；挤破或破皮的痘跳过不涂。
4. 等 15-20 分钟。
5. 保湿：适乐肤 PM 乳 1-2 泵全脸薄涂（PM 乳小片试用期已过，2026-11-06 首晚全脸使用无不良反应，直接全脸用）；凡士林退回只点嘴唇和起皮处，不再当主力保湿。
6. 固定提醒一行：过期的克林霉素（管装和罐装）都不要再用；今晚如果脸明显刺痛、发红，阿达帕林就跳过一晚，只做保湿，明晚再恢复。

末尾衔接一句：涂完正好赶上 22:30 的入睡记录提醒。

---
id: sleep-log-reminder
title: 每晚入睡记录提醒
enabled: true
owner: goal:goal
mode: task
schedule:
  kind: daily
  timezone: '@user.current'
  time: 22:30:00
delivery:
  - chat_id: 3a463ab2-0465-4f02-a3a8-3ce9b8b25bba
metadata:
  originating_chat_context_json: '{"chat_id":"3a463ab2-0465-4f02-a3a8-3ce9b8b25bba","origin_provider":"main","chat_kind":"direct","event_kind":"message","require_mention":false,"device_id":"71ebbd46-fb04-48c4-b512-0f8b3fb9ae32"}'
  presentation_locale: zh-CN
---
提醒 kuai 记录今晚的入睡时间，这是“改善睡眠和精力”目标里手动记录 7 晚的一部分。

只在本地日期为 2026-10-30 至 2026-11-05 期间发送提醒。提醒内容用简体中文，简短温和：提示今晚关灯准备睡时回复一句“关灯 HH:MM”，例如“关灯 23:40”；第二天有精力时可再补充大概多久睡着和白天精力 1-5 分。不要施加压力，不要把没记录说成失败。

如果本地日期已经晚于 2026-11-05，不要再发送每晚记录提醒。

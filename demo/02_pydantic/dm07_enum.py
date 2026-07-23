"""
Enum：把字段限定为「固定的几个取值」
有些字段的取值是固定的一小撮，比如模拟面试的「阶段」只能是「热身 / 技术基础 / 项目 / 收尾 / 结束」之一。这时用 Enum（枚举）来定义合法取值集合，既防止写错，又让代码更清晰：

Author: danke
Date: 2026/7/22 15:43
"""
from enum import Enum

class InterviewStage(str, Enum):       # 继承 str，取值就是字符串
    WARMUP    = "warmup"
    TECH_BASE = "tech_base"
    PROJECT   = "project"
    CLOSING   = "closing"
    FINISHED  = "finished"

print(InterviewStage.WARMUP)           # InterviewStage.WARMUP
print(InterviewStage.WARMUP.value)     # warmup
if InterviewStage.WARMUP == "warmup":
    print("hello")
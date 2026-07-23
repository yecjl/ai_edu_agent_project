"""
Optional: 如果某个字段「可能有、也可能没有（可以是 None）」


Author: danke
Date: 2026/7/22 15:20
"""
from typing import Optional
from pydantic import BaseModel


class Profile(BaseModel):
    nickname: Optional[str] = None  # 可以是字符串，也可以是 None, Python 3.5+	
    nickname2: str | None = None  # Python 3.10+

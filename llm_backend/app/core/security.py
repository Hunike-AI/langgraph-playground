from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.services.user_service import UserService
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

"""
安全相关工具模块
- 生成访问令牌（JWT）
- 解析并验证令牌，从请求中获取当前用户
"""

# OAuth2 令牌获取方案：从请求头的 Authorization: Bearer <token> 中提取令牌
# tokenUrl 指向登录获取令牌的接口路径（相对路径）
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建访问令牌（JWT）

    参数：
    - data: 需要编码到令牌中的载荷（如 {"sub": 用户标识}）
    - expires_delta: 令牌过期时间增量，不传则默认 15 分钟

    返回：
    - 编码后的 JWT 字符串
    """
    to_encode = data.copy()  # 复制载荷，避免修改原始数据
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # 自定义过期时间
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # 默认过期时间 15 分钟
    to_encode.update({"exp": expire})  # 写入过期时间声明
    # 使用项目配置中的密钥与算法生成令牌
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    通过请求中的 Bearer Token 获取当前用户

    流程：
    - 从 Authorization 中提取令牌
    - 使用密钥和算法解码令牌并提取用户标识（sub）
    - 根据邮箱查询用户，返回用户对象

    异常：
    - 验证失败统一返回 401 未授权
    """
    # 统一的未授权异常，用于各种校验失败场景
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码 JWT，验证签名与算法是否匹配
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")  # 从载荷中获取用户标识（这里使用邮箱）
        if email is None:
            # 令牌中无有效用户标识
            raise credentials_exception
    except JWTError:
        # 令牌无效、过期或签名错误
        raise credentials_exception
        
    # 根据邮箱查询数据库用户
    user_service = UserService(db)
    user = await user_service.get_user_by_email(email)
    if user is None:
        # 用户不存在或已删除
        raise credentials_exception
    return user

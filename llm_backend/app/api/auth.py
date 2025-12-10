from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.user import UserCreate, UserResponse, Token, UserLogin
from app.services.user_service import UserService
from datetime import timedelta
from app.core.config import settings
from app.models.user import User

router = APIRouter()

"""
# response_model 指定了响应的数据类型，返回结果需要与 UserResponse 类型一致
# 详细文档参考：https://fastapi.tiangolo.com/tutorial/response-model/
# Depends(get_db) 表示 db 参数是一个依赖项，会自动调用 get_db 函数获取数据库会话
# FastAPI 会在处理请求时自动注入数据库连接
"""

# 用户注册接口
@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    用户注册接口
    - 接收用户注册信息（邮箱、密码等）
    - 创建新用户账户
    - 返回创建的用户信息
    """
    try:
        user_service = UserService(db)
        user = await user_service.create_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 用户登录接口
@router.post("/token", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    用户登录接口
    - 验证用户邮箱和密码
    - 生成访问令牌（JWT）
    - 返回访问令牌和令牌类型
    """
    user_service = UserService(db)
    user = await user_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 设置令牌过期时间
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 创建访问令牌
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 令牌验证接口
@router.get("/validate-token")
async def validate_token(current_user: User = Depends(get_current_user)):
    """
    验证JWT令牌是否有效
    - 检查当前用户的认证状态
    - 返回用户ID和验证结果
    - 用于前端检查用户登录状态
    """
    return {"valid": True, "user_id": current_user.id}

# 获取当前用户信息接口
@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户的详细信息
    - 返回当前认证用户的数据
    - 用于个人中心、用户资料页面
    - 需要有效的JWT令牌才能访问
    """
    return current_user
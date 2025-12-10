from fastapi import APIRouter
from .auth import router as auth_router

# 创建主API路由器实例
api_router = APIRouter()
# 包含认证相关的路由，标签为"authentication"用于API文档分组
api_router.include_router(auth_router, tags=["authentication"])

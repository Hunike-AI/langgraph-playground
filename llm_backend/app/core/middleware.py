from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import get_logger
import time

# 获取HTTP服务的日志记录器
logger = get_logger(service="http")

# HTTP请求日志中间件
# 用于记录所有HTTP请求的详细信息，包括请求方法、路径、状态码和处理时间
class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志记录中间件
    
    该中间件会拦截所有HTTP请求，记录请求的详细信息，包括：
    - 客户端IP地址和端口
    - 请求方法、路径和HTTP版本
    - 响应状态码
    - 请求处理时间
    """
    
    async def dispatch(self, request: Request, call_next):
        """处理请求并记录日志
        Args:
            request: FastAPI请求对象
            call_next: 下一个中间件或路由处理函数
        Returns:
            响应对象
        """
        # 记录请求开始时间
        start_time = time.time()
        
        # 调用下一个处理程序（路由函数或其他中间件）
        response = await call_next(request)
        
        # 计算请求处理总时间
        process_time = time.time() - start_time
        
        # 记录详细的请求日志信息
        # 格式：IP:端口 - "方法 路径 HTTP版本" 状态码 - 处理时间s
        logger.info(
            f"{request.client.host}:{request.client.port} - "
            f"\"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}\" "
            f"{response.status_code} - {process_time:.2f}s"
        )
        
        # 返回响应对象
        return response 
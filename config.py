"""
Config Manager - 配置管理
安全地管理代理凭证和敏感信息

使用方式：
  from config import get_proxy_config, Config
  
  # 从环境变量或 .env 文件读取
  config = Config()
  proxy_url = config.get_proxy_url()
"""

import os
from pathlib import Path
from typing import Optional, Dict


class Config:
    """应用配置管理"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        初始化配置
        
        Args:
            env_file: .env 文件路径（可选）
        """
        self.env_file = env_file or Path(__file__).parent / '.env'
        self._load_env_file()
    
    def _load_env_file(self):
        """从 .env 文件加载配置"""
        if self.env_file and Path(self.env_file).exists():
            try:
                with open(self.env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                os.environ.setdefault(key.strip(), value.strip())
            except Exception as e:
                print(f"⚠ 警告: 无法读取 .env 文件: {e}")
    
    # ==================== Proxy Configuration ====================
    
    def get_proxy_url(self) -> Optional[str]:
        """
        获取代理 URL
        
        优先级：
        1. PROXY_URL 环境变量
        2. 从用户名和密码构建
        3. 返回 None
        
        Returns:
            代理 URL 字符串或 None
        """
        # 检查直接的代理 URL
        if proxy_url := os.getenv('PROXY_URL'):
            return proxy_url
        
        # 从用户名和密码构建
        username = os.getenv('PROXY_USERNAME')
        password = os.getenv('PROXY_PASSWORD')
        host = os.getenv('PROXY_HOST', 'res.proxy-seller.com')
        port = os.getenv('PROXY_PORT', '10000')
        
        if username and password:
            return f"http://{username}:{password}@{host}:{port}"
        
        return None
    
    def get_proxy_config(self) -> Dict[str, str]:
        """
        获取代理配置字典（用于 requests）
        
        Returns:
            {'http': 'http://...', 'https': 'http://...'}
        """
        if proxy_url := self.get_proxy_url():
            return {
                'http': proxy_url,
                'https': proxy_url,
            }
        return {}
    
    def use_proxy(self) -> bool:
        """检查是否启用代理"""
        return self.get_proxy_url() is not None
    
    # ==================== API Configuration ====================
    
    def get_api_timeout(self) -> int:
        """获取 API 超时时间（秒）"""
        return int(os.getenv('API_TIMEOUT', '15'))
    
    def get_max_retries(self) -> int:
        """获取最大重试次数"""
        return int(os.getenv('MAX_RETRIES', '3'))
    
    def get_retry_delay(self) -> int:
        """获取重试延迟（秒）"""
        return int(os.getenv('RETRY_DELAY', '1'))
    
    # ==================== Output Configuration ====================
    
    def get_output_dir(self) -> Path:
        """获取输出目录"""
        output_dir = os.getenv('OUTPUT_DIR', str(Path(__file__).parent / 'data'))
        return Path(output_dir)
    
    def get_output_dir_data(self) -> Path:
        """获取数据输出目录"""
        return self.get_output_dir() / 'data'
    
    def create_output_dirs(self):
        """创建输出目录"""
        self.get_output_dir().mkdir(parents=True, exist_ok=True)
        self.get_output_dir_data().mkdir(parents=True, exist_ok=True)


def get_proxy_config() -> Dict[str, str]:
    """便利函数：获取代理配置"""
    config = Config()
    return config.get_proxy_config()


def get_config() -> Config:
    """便利函数：获取配置实例"""
    return Config()


if __name__ == '__main__':
    # 测试配置
    config = Config()
    
    print("="*60)
    print("📋 配置管理测试")
    print("="*60)
    
    print("\n🌐 代理配置:")
    print(f"  是否启用代理: {config.use_proxy()}")
    if config.use_proxy():
        proxy = config.get_proxy_url()
        # 隐藏敏感信息
        masked = proxy.replace(proxy.split('@')[0].split('//')[1], '***:***')
        print(f"  代理 URL: {masked}")
    
    print("\n⏱️ API 配置:")
    print(f"  超时时间: {config.get_api_timeout()}s")
    print(f"  最大重试: {config.get_max_retries()}")
    print(f"  重试延迟: {config.get_retry_delay()}s")
    
    print("\n📁 输出目录:")
    print(f"  根目录: {config.get_output_dir()}")
    print(f"  数据目录: {config.get_output_dir_data()}")
    
    print("\n✅ 配置加载成功！")

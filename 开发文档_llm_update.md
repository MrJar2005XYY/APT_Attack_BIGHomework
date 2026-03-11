# LLM API 增强模块 - 补充文档

## 2.3.3 分析功能（增强版）

```python
class LLMAnalyzer:
    """大模型分析器 - 支持灵活的配置和多种分析模式"""
    
    def __init__(self, provider: LLMProvider, config: Optional[LLMConfig] = None):
        self.provider = provider
        self.config = config or LLMConfig(provider="openai")
        
    def analyze_threat(self, intelligence: ParsedIntelligence, 
                      custom_prompt: Optional[str] = None) -> ThreatAnalysis:
        """分析威胁情报"""
        prompt = custom_prompt or self._build_analysis_prompt(intelligence)
        messages = [ChatMessage(role="user", content=prompt)]
        result = self.provider.chat(
            messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return self._parse_analysis_result(result)
    
    def attribute_attack(self, malware: str, techniques: List[str], 
                        custom_prompt: Optional[str] = None) -> AttributionResult:
        """归因分析"""
        prompt = custom_prompt or f"""根据以下恶意软件和攻击技术，分析可能的 APT 组织：
恶意软件：{malware}
攻击技术：{', '.join(techniques)}
请列出可能的 APT 组织及其置信度。"""
        messages = [ChatMessage(role="user", content=prompt)]
        result = self.provider.chat(
            messages,
            temperature=0.5,  # 归因分析需要更保守
            max_tokens=self.config.max_tokens
        )
        return self._parse_attribution(result)
    
    def generate_summary(self, entities: List[ThreatEntity], 
                        style: str = "concise") -> str:
        """生成摘要 - 支持多种风格"""
        style_prompts = {
            "concise": "请用简洁的语言总结",
            "detailed": "请提供详细的分析报告",
            "executive": "请生成面向管理层的高层摘要",
            "technical": "请生成技术细节丰富的报告"
        }
        style_prompt = style_prompts.get(style, "concise")
        
        prompt = f"""{style_prompt}以下威胁实体：
{chr(10).join([f"- {e.name} ({e.type}): {e.description}" for e in entities])}"""
        
        messages = [ChatMessage(role="user", content=prompt)]
        result = self.provider.chat(messages)
        return result
    
    def predict_trends(self, historical_data: List[ThreatEntity]) -> TrendPrediction:
        """趋势预测"""
        prompt = f"""基于以下历史威胁数据，预测未来 3-6 个月的攻击趋势：
{chr(10).join([f"- {e.name}: {e.description}" for e in historical_data])}
请分析：
1. 可能活跃的组织
2. 可能被利用的漏洞类型
3. 攻击技术演进方向
4. 目标行业/地区趋势"""
        messages = [ChatMessage(role="user", content=prompt)]
        result = self.provider.chat(messages, temperature=0.8)  # 预测需要更高创造性
        return self._parse_trend_prediction(result)
    
    def chat_with_context(self, messages: List[ChatMessage], 
                         system_prompt: Optional[str] = None) -> str:
        """支持多轮对话的上下文聊天"""
        if system_prompt:
            messages.insert(0, ChatMessage(role="system", content=system_prompt))
        
        result = self.provider.chat(
            messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=self.config.stream
        )
        return result
    
    def extract_iocs(self, text: str) -> IOCResult:
        """从文本中提取威胁指标（IOCs）"""
        prompt = f"""从以下文本中提取所有威胁指标（IOCs），包括：
- IP 地址
- 域名
- 文件哈希（MD5, SHA1, SHA256）
- 邮箱地址
- URL

文本内容：
{text}

请以 JSON 格式返回结果。"""
        messages = [ChatMessage(role="user", content=prompt)]
        result = self.provider.chat(messages, temperature=0.1)  # 低温度保证准确性
        return self._parse_iocs(result)
    
    def _build_analysis_prompt(self, intelligence: ParsedIntelligence) -> str:
        """构建分析提示词"""
        return f"""分析以下威胁情报：
标题：{intelligence.title}
来源：{intelligence.source}
发布时间：{intelligence.published_at}

已识别的实体：
{chr(10).join([f"- {e.name} ({e.type})" for e in intelligence.entities])}

请提供：
1. 威胁等级评估（高/中/低）
2. 影响范围分析
3. 建议的应对措施"""
    
    def _parse_analysis_result(self, result: ChatCompletion) -> ThreatAnalysis:
        """解析分析结果"""
        content = result.choices[0].message.content
        # 解析逻辑...
        return ThreatAnalysis(content=content)
    
    def _parse_attribution(self, result: ChatCompletion) -> AttributionResult:
        """解析归因结果"""
        content = result.choices[0].message.content
        # 解析逻辑...
        return AttributionResult(content=content)
    
    def _parse_trend_prediction(self, result: ChatCompletion) -> TrendPrediction:
        """解析趋势预测"""
        content = result.choices[0].message.content
        # 解析逻辑...
        return TrendPrediction(content=content)
    
    def _parse_iocs(self, result: ChatCompletion) -> IOCResult:
        """解析 IOC 结果"""
        content = result.choices[0].message.content
        # 解析 JSON 结果...
        return IOCResult.parse_raw(content)


class ChatMessage(BaseModel):
    """聊天消息"""
    role: str  # "system", "user", "assistant"
    content: str
    name: Optional[str] = None  # 可选的名称
    function_call: Optional[dict] = None  # 函数调用（如果支持）


class ThreatAnalysis(BaseModel):
    """威胁分析结果"""
    content: str
    threat_level: Optional[str] = None  # "high", "medium", "low"
    confidence: float = 0.0
    recommendations: List[str] = []


class AttributionResult(BaseModel):
    """归因分析结果"""
    content: str
    suspected_groups: List[dict] = []  # [{name, confidence, evidence}]


class TrendPrediction(BaseModel):
    """趋势预测结果"""
    content: str
    time_range: str
    key_trends: List[str] = []


class IOCResult(BaseModel):
    """威胁指标提取结果"""
    ip_addresses: List[str] = []
    domains: List[str] = []
    file_hashes: List[dict] = []  # [{type, value}]
    emails: List[str] = []
    urls: List[str] = []
```

## 2.3.4 使用示例

```python
# 示例 1: 使用 OpenAI 官方 API
openai_config = LLMConfig(
    provider="openai",
    api_key="sk-...",
    base_url="https://api.openai.com/v1",
    model="gpt-4-turbo-preview",
    temperature=0.7,
    max_tokens=2000
)
openai_provider = OpenAIProvider(openai_config)
analyzer = LLMAnalyzer(openai_provider, openai_config)

# 示例 2: 使用 Azure OpenAI
azure_config = LLMConfig(
    provider="azure",
    api_key="...",
    base_url="https://your-resource.openai.azure.com/",
    api_version="2024-02-15-preview",
    model="gpt-4",
    temperature=0.7
)
azure_provider = AzureOpenAIProvider(azure_config)
analyzer = LLMAnalyzer(azure_provider, azure_config)

# 示例 3: 使用本地 Ollama（无需 API Key）
ollama_config = LLMConfig(
    provider="custom",
    provider_name="Ollama",
    api_key="",  # 本地部署无需 key
    base_url="http://localhost:11434/v1",
    model="llama2:70b",
    temperature=0.7,
    max_tokens=2000
)
ollama_provider = CustomOpenAIProvider(ollama_config)
analyzer = LLMAnalyzer(ollama_provider, ollama_config)

# 示例 4: 使用第三方服务（如 DeepSeek）
deepseek_config = LLMConfig(
    provider="custom",
    provider_name="DeepSeek",
    api_key="sk-...",
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    temperature=0.7
)
deepseek_provider = CustomOpenAIProvider(deepseek_config)
analyzer = LLMAnalyzer(deepseek_provider, deepseek_config)

# 测试连接
if provider.test_connection():
    print(f"成功连接到 {provider.get_model_name()}")
else:
    print("连接失败，请检查配置")
```

## 2.5.4 大模型配置 API 接口

```python
# ========== 大模型配置管理接口 ==========

class LLMConfigCreate(BaseModel):
    """创建大模型配置"""
    provider: str
    provider_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    stream: bool = False

class LLMConfigUpdate(BaseModel):
    """更新大模型配置"""
    provider_name: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None
    stream: Optional[bool] = None

class LLMConfigResponse(BaseModel):
    """大模型配置响应（不返回敏感信息）"""
    id: str
    provider: str
    provider_name: Optional[str]
    base_url: str
    model: str
    temperature: float
    max_tokens: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

class LLMTestRequest(BaseModel):
    """测试 LLM 连接请求"""
    provider: str
    api_key: Optional[str] = None
    base_url: str
    model: str

class LLMTestResponse(BaseModel):
    """测试 LLM 连接响应"""
    success: bool
    message: str
    model_info: Optional[dict] = None
    response_time: float  # 毫秒

@app.get("/api/v1/config/llm", response_model=List[LLMConfigResponse])
async def list_llm_configs():
    """获取所有大模型配置列表"""
    configs = await config_service.list_llm_configs()
    return configs

@app.get("/api/v1/config/llm/{config_id}", response_model=LLMConfigResponse)
async def get_llm_config(config_id: str):
    """获取指定大模型配置"""
    config = await config_service.get_llm_config(config_id)
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return config

@app.post("/api/v1/config/llm", response_model=LLMConfigResponse)
async def create_llm_config(config: LLMConfigCreate):
    """创建新的大模型配置"""
    # 验证配置
    try:
        llm_config = LLMConfig(**config.dict())
        provider = LLMProviderFactory.create(llm_config)
        # 测试连接
        if not provider.test_connection():
            raise HTTPException(status_code=400, detail="无法连接到 LLM 服务")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # 保存到数据库
    new_config = await config_service.create_llm_config(config)
    return new_config

@app.put("/api/v1/config/llm/{config_id}", response_model=LLMConfigResponse)
async def update_llm_config(config_id: str, config: LLMConfigUpdate):
    """更新大模型配置"""
    updated_config = await config_service.update_llm_config(config_id, config)
    if not updated_config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return updated_config

@app.delete("/api/v1/config/llm/{config_id}")
async def delete_llm_config(config_id: str):
    """删除大模型配置"""
    success = await config_service.delete_llm_config(config_id)
    if not success:
        raise HTTPException(status_code=404, detail="配置不存在")
    return {"message": "配置已删除"}

@app.post("/api/v1/config/llm/test", response_model=LLMTestResponse)
async def test_llm_connection(request: LLMTestRequest):
    """测试大模型连接是否可用"""
    import time
    
    try:
        config = LLMConfig(
            provider=request.provider,
            api_key=request.api_key,
            base_url=request.base_url,
            model=request.model
        )
        provider = LLMProviderFactory.create(config)
        
        # 测试连接并计算响应时间
        start_time = time.time()
        is_connected = provider.test_connection()
        response_time = (time.time() - start_time) * 1000
        
        if is_connected:
            model_info = {
                "name": provider.get_model_name(),
                "base_url": request.base_url
            }
            return LLMTestResponse(
                success=True,
                message="连接成功",
                model_info=model_info,
                response_time=response_time
            )
        else:
            return LLMTestResponse(
                success=False,
                message="连接失败，请检查配置",
                response_time=response_time
            )
    except Exception as e:
        return LLMTestResponse(
            success=False,
            message=f"连接出错：{str(e)}",
            response_time=0
        )

@app.post("/api/v1/analyze/chat")
async def chat_with_llm(
    messages: List[ChatMessage],
    config_id: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
):
    """与大模型进行对话（使用保存的配置或临时配置）"""
    # 获取配置
    if config_id:
        config = await config_service.get_llm_config(config_id)
        if not config:
            raise HTTPException(status_code=404, detail="配置不存在")
        llm_config = LLMConfig(**config.dict())
    else:
        # 使用默认配置
        llm_config = LLMConfig(provider="openai")
    
    # 创建 provider
    provider = LLMProviderFactory.create(llm_config)
    analyzer = LLMAnalyzer(provider, llm_config)
    
    # 执行对话
    result = analyzer.chat_with_context(
        messages,
        system_prompt="你是一个网络安全威胁情报分析助手。"
    )
    
    return {
        "response": result,
        "model": provider.get_model_name(),
        "usage": {
            "prompt_tokens": 0,  # 实际使用时从 API 响应中获取
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }
```

## 2.3.5 配置管理界面设计

### 前端配置表单

```typescript
interface LLMConfigForm {
  provider: 'openai' | 'azure' | 'anthropic' | 'custom';
  providerName?: string;  // custom 模式必填
  apiKey?: string;  // 可选，本地部署可为空
  baseUrl: string;
  model: string;
  temperature: number;  // 0-2
  maxTokens: number;
  timeout: number;
  stream: boolean;
  apiVersion?: string;  // Azure 专用
}

// 预设配置模板
const PRESET_CONFIGS = {
  openai: {
    baseUrl: 'https://api.openai.com/v1',
    model: 'gpt-4-turbo-preview',
    providerName: 'OpenAI'
  },
  azure: {
    baseUrl: 'https://your-resource.openai.azure.com/',
    apiVersion: '2024-02-15-preview',
    model: 'gpt-4',
    providerName: 'Azure'
  },
  ollama: {
    baseUrl: 'http://localhost:11434/v1',
    model: 'llama2:70b',
    providerName: 'Ollama',
    apiKey: ''
  },
  deepseek: {
    baseUrl: 'https://api.deepseek.com/v1',
    model: 'deepseek-chat',
    providerName: 'DeepSeek'
  },
  moonshot: {
    baseUrl: 'https://api.moonshot.cn/v1',
    model: 'moonshot-v1-8k',
    providerName: 'Moonshot'
  }
};
```

### 配置管理页面功能

1. **配置列表**
   - 显示所有已保存的配置
   - 显示配置名称、提供商、模型、状态
   - 支持快速切换活跃配置

2. **添加/编辑配置**
   - 选择提供商类型
   - 自动填充预设 URL（可修改）
   - 自定义模型名称
   - 可选填写 API Key
   - 调整参数（temperature、max_tokens 等）

3. **连接测试**
   - 一键测试连接
   - 显示响应时间
   - 显示模型信息

4. **安全存储**
   - API Key 加密存储
   - 前端不显示完整 Key
   - 支持从环境变量读取

## 2.3.6 环境变量配置

```bash
# .env 示例

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1

# Azure OpenAI
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Anthropic
ANTHROPIC_API_KEY=...

# Google Gemini
GOOGLE_API_KEY=...

# DeepSeek
DEEPSEEK_API_KEY=...

# Moonshot
MOONSHOT_API_KEY=...

# 默认配置
DEFAULT_LLM_PROVIDER=openai
DEFAULT_LLM_MODEL=gpt-4-turbo-preview
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000
```

## 2.3.7 快速切换方案

```python
# 方案 1: 通过配置文件切换
# config/llm.yaml
active_provider: openai  # 切换此处

providers:
  openai:
    # ... 配置
  azure:
    # ... 配置
  ollama:
    # ... 配置

# 方案 2: 通过环境变量切换
# .env
ACTIVE_LLM_PROVIDER=ollama

# 方案 3: 通过 API 动态切换
# POST /api/v1/config/llm/switch
{
  "config_id": "ollama-local"
}

# 方案 4: 代码中动态创建
config = LLMConfig(
    provider="custom",
    base_url="http://localhost:11434/v1",
    model="llama2:70b"
)
provider = LLMProviderFactory.create(config)
```

## 总结

通过以上增强设计，系统实现了：

1. ✅ **灵活的 URL 配置** - 支持任意兼容 OpenAI 格式的 API 端点
2. ✅ **可选的 API Key** - 支持本地部署无需认证
3. ✅ **自定义模型名称** - 可填写任意模型名称
4. ✅ **多提供商支持** - OpenAI、Azure、Anthropic、Ollama、vLLM、DeepSeek、Moonshot 等
5. ✅ **工厂模式** - 统一接口，轻松扩展新提供商
6. ✅ **连接测试** - 一键验证配置是否可用
7. ✅ **配置管理 API** - 完整的 CRUD 接口
8. ✅ **安全存储** - API Key 加密处理
9. ✅ **多种切换方式** - 配置文件、环境变量、API 动态切换


# EXP15.md - API参数优化的工程实践经验

## 经验主题
**API参数扩展的最佳实践** - 如何安全地为现有API添加新参数

## 核心经验

### 1. 第一性原理在API设计中的应用

#### 问题分解策略
- **基础事实识别**: 确认API文档、现有代码结构、调用关系
- **假设质疑**: 不假设参数位置、不假设API支持情况
- **逻辑重构**: 从API规范出发，重新构建参数传递逻辑

#### 实践要点
```python
# 错误做法：直接添加参数而不考虑兼容性
def generate_image(self, prompt: str, watermark: bool):  # 破坏向后兼容性

# 正确做法：使用默认值保证兼容性
def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1, watermark: bool = False):
```

### 2. 代码影响范围分析技巧

#### 工具使用策略
- **codebase-retrieval**: 查找所有调用点，避免遗漏
- **搜索模式**: 使用精确的方法名和类名搜索
- **依赖分析**: 分析直接调用和间接调用关系

#### 实际案例
```python
# 发现的调用点
src/utils/image.py:182 - await model.generate_image(prompt, size)
# 需要更新为
src/utils/image.py:182 - await model.generate_image(prompt, size, watermark=False)
```

### 3. API文档验证的多重策略

#### 验证方法
1. **官方文档查阅**: 直接访问API文档页面
2. **搜索引擎验证**: 使用关键词搜索确认参数存在
3. **实际测试验证**: 通过API调用确认参数效果

#### 经验教训
- 文档页面可能需要JavaScript，要使用web-search作为备选
- 搜索时使用具体的参数名和API名称组合
- 实际测试是最终的验证手段

### 4. 向后兼容性设计原则

#### 设计原则
- **默认值策略**: 新参数必须有合理的默认值
- **可选参数**: 新参数应该是可选的，不影响现有调用
- **行为保持**: 默认行为应该与修改前完全一致

#### 实现技巧
```python
# 好的设计：明确的默认值
async def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1, watermark: bool = False):

# 调用时的灵活性
await model.generate_image(prompt)  # 使用所有默认值
await model.generate_image(prompt, watermark=False)  # 明确指定
```

### 5. 测试驱动的参数验证

#### 测试策略
- **对比测试**: 测试新参数的不同值产生的不同效果
- **边界测试**: 测试默认值和非默认值的情况
- **集成测试**: 在实际使用场景中测试新参数

#### 测试脚本设计
```python
# 测试watermark=False（默认行为）
image_urls = await model.generate_image(prompt, watermark=False)

# 测试watermark=True（新功能）
image_urls = await model.generate_image(prompt, watermark=True)

# 验证URL差异
assert "watermark" not in urls_false[0]  # 无水印处理参数
assert "watermark" in urls_true[0]       # 有水印处理参数
```

### 6. 文档同步的重要性

#### 同步策略
- **即时更新**: 代码修改后立即更新相关文档
- **多层次文档**: 更新API文档、架构文档、使用说明
- **变更记录**: 在文档中明确记录新增功能

#### 文档内容
```markdown
### 图像生成
- 支持豆包API图像生成
- 使用模型：doubao-seedream-3-0-t2i-250415
- 自动优化提示词
- 图像下载和存储
- 支持watermark参数控制（默认为false，无水印）  # 新增
```

## 技术深度分析

### API参数传递的最佳实践

#### 参数顺序设计
1. **必需参数**: 放在前面，如prompt
2. **常用可选参数**: 中间位置，如size, n
3. **新增可选参数**: 放在最后，如watermark

#### 参数命名规范
- 使用清晰的布尔值命名：`watermark: bool`
- 避免否定式命名：不用`no_watermark`
- 保持与API文档一致的命名

### 错误处理和日志记录

#### 参数验证
```python
# 可以添加的参数验证
if not isinstance(watermark, bool):
    raise ValueError("watermark参数必须是布尔值")
```

#### 日志记录
```python
self.logger.debug(f"生成图像参数: prompt={prompt}, size={size}, watermark={watermark}")
```

### 性能考虑

#### API调用优化
- 新参数不应该增加API调用的复杂度
- 保持请求数据结构的简洁性
- 避免不必要的参数传递

## 通用经验总结

### 成功要素
1. **系统性思考**: 从需求到实现到测试的完整流程
2. **工具善用**: 充分利用代码分析工具
3. **验证驱动**: 每个步骤都要有验证手段
4. **文档意识**: 代码和文档同步更新

### 常见陷阱
1. **兼容性忽视**: 添加参数时破坏现有调用
2. **测试不足**: 只测试新功能，不测试默认行为
3. **文档滞后**: 代码更新了但文档没有同步
4. **影响范围遗漏**: 没有找到所有的调用点

### 质量保证
1. **代码审查**: 检查参数设计的合理性
2. **测试覆盖**: 确保新旧行为都有测试覆盖
3. **文档检查**: 确保文档准确反映新功能
4. **回归测试**: 确保现有功能不受影响

## 可复用的模式

### API扩展模板
```python
# 原始方法
async def api_method(self, required_param: str, optional_param: str = "default"):
    pass

# 扩展方法
async def api_method(self, required_param: str, optional_param: str = "default", new_param: bool = False):
    # 保持原有逻辑
    # 添加新参数处理
    pass
```

### 测试模板
```python
async def test_new_parameter():
    # 测试默认行为（向后兼容性）
    result_default = await api_method("test")
    
    # 测试新参数功能
    result_new = await api_method("test", new_param=True)
    
    # 验证差异
    assert result_default != result_new
```

### 文档更新模板
```markdown
### 功能名称
- 现有功能描述
- 新增：新参数说明（默认值，作用）
```

## 结论
这次API参数优化实践展示了完整的软件工程流程：需求分析、设计实现、测试验证、文档更新。关键在于保持向后兼容性的同时，通过系统性的方法确保新功能的正确性和可靠性。这种方法论可以应用到任何API扩展场景中。

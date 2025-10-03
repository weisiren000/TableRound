# 关键词格式参考

本文档提供了关键词提取和展示的格式参考，包括KJ法分类结果和最终关键词展示格式。

## 关键词图格式

根据 `docs\项目要求\fix_program_ideas.md` 文件中提到的关键词图格式，我们需要实现类似的关键词展示方式。

### KJ法分类结果示例

```
一级类别1：[传统文化元素]
- 二级类别1.1：[吉祥符号]
  - 蝙蝠
  - 如意
  - 福字
  - 寿字
- 二级类别1.2：[传统工艺]
  - 剪纸
  - 刺绣
  - 雕刻
  - 印染

一级类别2：[设计元素]
- 二级类别2.1：[色彩]
  - 中国红
  - 金色
  - 黑色
  - 白色
- 二级类别2.2：[构图]
  - 对称
  - 重复
  - 环形
  - 放射状

一级类别3：[产品形式]
- 二级类别3.1：[装饰品]
  - 挂饰
  - 窗花
  - 壁画
  - 摆件
- 二级类别3.2：[实用品]
  - 灯具
  - 餐具
  - 文具
  - 包装

核心概念：中国传统剪纸艺术的现代文创应用
```

### 最终关键词展示格式

最终的关键词应该以清晰、层次化的方式展示，例如：

```
【核心概念】
中国传统剪纸艺术的现代文创应用

【一级关键词】
1. 传统文化元素
2. 设计元素
3. 产品形式

【二级关键词】
1.1 吉祥符号：蝙蝠、如意、福字、寿字
1.2 传统工艺：剪纸、刺绣、雕刻、印染
2.1 色彩：中国红、金色、黑色、白色
2.2 构图：对称、重复、环形、放射状
3.1 装饰品：挂饰、窗花、壁画、摆件
3.2 实用品：灯具、餐具、文具、包装

【用户输入关键词】
创新、实用、美观、文化传承、市场需求

【合并关键词】
1. 文化传承
2. 创新设计
3. 实用功能
4. 美学价值
5. 市场适应性
6. 传统工艺
7. 现代审美
8. 对称构图
9. 吉祥寓意
10. 多元应用
```

## 设计卡牌格式

设计卡牌应该包含以下内容，并以结构化的方式呈现：

```
【设计卡牌】- 手工艺人视角

【产品形式】
多功能剪纸灯饰，可作为台灯、挂灯或壁灯使用。

【设计元素】
- 色彩：传统中国红为主，辅以金色点缀
- 图案：对称蝙蝠纹样，融合云纹和如意纹
- 材质：优质红纸剪纸部分，竹木支架，LED灯源

【功能特点】
- 实用性：提供柔和照明，可调节亮度
- 装饰性：传统剪纸艺术与现代灯具结合
- 收藏价值：手工制作，限量发行

【目标用户】
25-45岁的文化爱好者，注重家居装饰，有一定消费能力的都市人群。

【文化内涵】
蝙蝠象征"福气"，灯光象征"光明"，二者结合寓意"幸福光明"。传统剪纸工艺与现代照明技术的融合，体现传统文化在现代生活中的应用。
```

## 实现注意事项

1. **格式一致性**：确保所有关键词和设计卡牌的格式保持一致，便于用户理解和系统处理。

2. **层次清晰**：使用标题、缩进和分隔符等方式，确保层次结构清晰可见。

3. **内容完整**：确保包含所有必要的信息，如关键词分类、设计元素、产品特点等。

4. **视觉呈现**：在命令行界面中，可以使用不同的颜色、分隔线或框架来增强视觉效果。

5. **数据存储**：将关键词和设计卡牌保存为结构化数据（如JSON），便于后续处理和展示。

## 示例实现

在命令行界面中展示关键词的示例代码：

```python
def display_keywords(keywords_structure: Dict[str, Any]):
    """
    在命令行中展示关键词结构
    
    Args:
        keywords_structure: 关键词结构数据
    """
    print("\n" + "=" * 50)
    print("【关键词分类结果】")
    print("=" * 50 + "\n")
    
    # 显示核心概念
    print(f"【核心概念】\n{keywords_structure['core_concept']}\n")
    
    # 显示一级关键词
    print("【一级关键词】")
    for i, category in enumerate(keywords_structure['categories'], 1):
        print(f"{i}. {category['name']}")
    print()
    
    # 显示二级关键词
    print("【二级关键词】")
    for i, category in enumerate(keywords_structure['categories'], 1):
        for j, subcategory in enumerate(category['subcategories'], 1):
            keywords_str = ", ".join(subcategory['keywords'])
            print(f"{i}.{j} {subcategory['name']}：{keywords_str}")
    print()
    
    # 显示用户输入关键词
    if 'user_keywords' in keywords_structure:
        print("【用户输入关键词】")
        print(", ".join(keywords_structure['user_keywords']))
        print()
    
    # 显示合并关键词
    if 'merged_keywords' in keywords_structure:
        print("【合并关键词】")
        for i, keyword in enumerate(keywords_structure['merged_keywords'], 1):
            print(f"{i}. {keyword}")
        print()
    
    print("=" * 50)
```

在命令行界面中展示设计卡牌的示例代码：

```python
def display_design_card(design_card: Dict[str, Any]):
    """
    在命令行中展示设计卡牌
    
    Args:
        design_card: 设计卡牌数据
    """
    print("\n" + "=" * 50)
    print(f"【设计卡牌】- {design_card['agent_type']}视角")
    print("=" * 50 + "\n")
    
    # 显示产品形式
    print(f"【产品形式】\n{design_card['product_form']}\n")
    
    # 显示设计元素
    print("【设计元素】")
    for element in design_card['design_elements']:
        print(f"- {element}")
    print()
    
    # 显示功能特点
    print("【功能特点】")
    for feature in design_card['features']:
        print(f"- {feature}")
    print()
    
    # 显示目标用户
    print(f"【目标用户】\n{design_card['target_users']}\n")
    
    # 显示文化内涵
    print(f"【文化内涵】\n{design_card['cultural_meaning']}\n")
    
    print("=" * 50)
```

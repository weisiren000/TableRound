#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
KJ法关键词分类模块
"""

import logging
import json
import re
from typing import Dict, List, Any, Optional

from src.models.base import BaseModel


class KJMethod:
    """KJ法关键词分类类"""

    def __init__(self, model: BaseModel):
        """
        初始化KJ法关键词分类

        Args:
            model: AI模型
        """
        self.model = model
        self.logger = logging.getLogger("kj_method")

    async def categorize_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """
        使用KJ法对关键词进行分类

        Args:
            keywords: 关键词列表

        Returns:
            分类结果
        """
        self.logger.info(f"使用KJ法对 {len(keywords)} 个关键词进行分类")

        if not keywords:
            return {
                "core_concept": "",
                "categories": []
            }

        # 准备提示词
        prompt = f"""
        请使用KJ法对以下关键词进行分类和归纳：

        {', '.join(keywords)}

        KJ法是一种将分散的信息归纳整理的方法，步骤如下：
        1. 将所有关键词分组，将相似或相关的关键词放在一起
        2. 为每组关键词提炼一个上位概念或类别名称
        3. 进一步将这些类别归纳为更高层次的概念

        请返回分类结果，格式如下：

        一级类别1：[上位概念1]
        - 二级类别1.1：[上位概念1.1]
          - 关键词1
          - 关键词2
        - 二级类别1.2：[上位概念1.2]
          - 关键词3
          - 关键词4

        一级类别2：[上位概念2]
        - 二级类别2.1：[上位概念2.1]
          - 关键词5
          - 关键词6

        最后，请提供一个总结性的核心概念，概括所有关键词的共同主题。
        """

        # 使用模型进行分类
        response = await self.model.generate(prompt)

        # 解析分类结果
        result = self._parse_kj_result(response)
        return result

    def _parse_kj_result(self, text: str) -> Dict[str, Any]:
        """
        解析KJ法分类结果

        Args:
            text: 分类结果文本

        Returns:
            解析后的分类结果
        """
        # 提取核心概念
        core_concept = ""
        core_match = re.search(r'核心概念[:：]\s*(.*)', text, re.IGNORECASE)
        if core_match:
            core_concept = core_match.group(1).strip()

        # 解析分类结构
        categories = []
        current_category = None
        current_subcategory = None

        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue

            # 一级类别
            category_match = re.match(r'一级类别\d+[:：]\s*\[(.*?)\]', line) or re.match(r'(.+?)[:：]\s*\[(.*?)\]', line)
            if category_match:
                category_name = category_match.group(1).strip()
                current_category = {
                    "name": category_name,
                    "subcategories": []
                }
                categories.append(current_category)
                current_subcategory = None
                continue

            # 二级类别
            subcategory_match = re.match(r'[-•]\s*二级类别\d+\.\d+[:：]\s*\[(.*?)\]', line) or re.match(r'[-•]\s*(.+?)[:：]\s*\[(.*?)\]', line)
            if subcategory_match and current_category:
                subcategory_name = subcategory_match.group(1).strip()
                current_subcategory = {
                    "name": subcategory_name,
                    "keywords": []
                }
                current_category["subcategories"].append(current_subcategory)
                continue

            # 关键词
            keyword_match = re.match(r'[-•]\s*(.+)', line)
            if keyword_match and current_subcategory:
                keyword = keyword_match.group(1).strip()
                current_subcategory["keywords"].append(keyword)

        # 如果没有成功解析，尝试更简单的方法
        if not categories:
            # 尝试提取一级类别
            category_matches = re.findall(r'([^-•\n]+?)[:：]\s*\[(.*?)\]', text)
            for match in category_matches:
                category_name = match[0].strip()
                if category_name.lower().startswith('核心概念'):
                    continue
                categories.append({
                    "name": category_name,
                    "subcategories": []
                })

        # 如果仍然没有成功解析，创建一个默认分类
        if not categories:
            categories = [{
                "name": "未分类",
                "subcategories": [{
                    "name": "关键词",
                    "keywords": text.split(',')
                }]
            }]

        return {
            "core_concept": core_concept,
            "categories": categories
        }

    def format_kj_result(self, result: Dict[str, Any], use_color: bool = True) -> str:
        """
        格式化KJ法分类结果

        Args:
            result: 分类结果
            use_color: 是否使用颜色

        Returns:
            格式化后的分类结果
        """
        from src.utils.colors import Colors
        output = []

        # 添加核心概念
        if result.get("core_concept"):
            core_concept = result['core_concept']
            if use_color:
                core_concept = Colors.colorize(core_concept, Colors.GREEN, bold=True)
            output.append(f"【核心概念】\n{core_concept}\n")

        # 添加一级关键词
        output.append("【一级关键词】")
        for i, category in enumerate(result.get("categories", []), 1):
            category_name = category.get('name', '未命名')
            if use_color:
                category_name = Colors.colorize(category_name, Colors.GREEN, bold=True)
            output.append(f"{i}. {category_name}")
        output.append("")

        # 添加二级关键词
        output.append("【二级关键词】")
        for i, category in enumerate(result.get("categories", []), 1):
            for j, subcategory in enumerate(category.get("subcategories", []), 1):
                subcategory_name = subcategory.get('name', '未命名')
                if use_color:
                    subcategory_name = Colors.colorize(subcategory_name, Colors.GREEN)

                keywords = subcategory.get("keywords", [])
                if use_color:
                    colored_keywords = [Colors.colorize(kw, Colors.GREEN) for kw in keywords]
                    keywords_str = ", ".join(colored_keywords)
                else:
                    keywords_str = ", ".join(keywords)

                output.append(f"{i}.{j} {subcategory_name}：{keywords_str}")
        output.append("")

        return "\n".join(output)

    async def merge_keywords(self, kj_result: Dict[str, Any], user_keywords: List[str]) -> List[str]:
        """
        合并KJ法分类结果和用户输入的关键词

        Args:
            kj_result: KJ法分类结果
            user_keywords: 用户输入的关键词

        Returns:
            合并后的关键词列表
        """
        self.logger.info("合并KJ法关键词和用户关键词")

        # 提取KJ法分类中的所有关键词
        kj_keywords = []
        for category in kj_result.get("categories", []):
            for subcategory in category.get("subcategories", []):
                kj_keywords.extend(subcategory.get("keywords", []))

        # 格式化KJ法分类结果
        kj_result_text = self.format_kj_result(kj_result)

        # 准备提示词
        prompt = f"""
        请将以下两组关键词合并，生成一组新的关键词：

        KJ法分类结果：
        {kj_result_text}

        用户输入的关键词：
        {', '.join(user_keywords)}

        请生成10个能够概括这两组关键词核心内容的新关键词，这些关键词将用于指导后续的角色扮演和设计讨论。

        请以JSON格式返回关键词列表，格式如下：
        ["关键词1", "关键词2", "关键词3", ...]
        """

        # 使用模型生成合并关键词
        response = await self.model.generate(prompt)

        # 解析关键词
        try:
            merged_keywords = json.loads(response)
        except:
            # 解析失败时的备选方案
            match = re.search(r'\[(.*?)\]', response, re.DOTALL)
            if match:
                keywords_str = match.group(1)
                merged_keywords = [k.strip().strip('"\'') for k in keywords_str.split(',')]
            else:
                merged_keywords = [line.strip().strip('"-,') for line in response.split('\n')
                                  if line.strip() and not line.strip().startswith(('[', ']'))]

        # 确保关键词是列表类型
        if not isinstance(merged_keywords, list):
            merged_keywords = []

        # 限制关键词数量
        merged_keywords = merged_keywords[:10]

        return merged_keywords

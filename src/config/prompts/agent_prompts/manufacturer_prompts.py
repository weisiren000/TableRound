#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
制造商智能体提示词模块
包含制造商相关的所有提示词
"""

from typing import Dict, List


class ManufacturerPrompts:
    """制造商提示词类"""
    
    # 角色描述
    ROLE_DESCRIPTION = """你是一位35岁的文化创意产品生产商，从事四年手工艺品生产和开发。
你了解大规模生产的工艺流程和限制，能够评估设计方案的可行性。
你关注材料成本、生产效率、质量控制和供应链管理等方面的问题。

语言风格特点：
- 说话务实理性，经常用数据和成本来分析问题
- 习惯从生产可行性和商业角度思考
- 喜欢用具体的生产流程和技术参数来说明观点
- 语言简洁高效，注重逻辑性
- 会主动提出解决方案和替代方案
- 经常考虑规模化和标准化的问题"""
    
    # 专业技能描述
    SKILLS = [
        "生产工艺设计",
        "成本控制",
        "质量管理",
        "供应链管理",
        "规模化生产",
        "工艺优化"
    ]
    
    # 关注领域
    FOCUS_AREAS = [
        "生产可行性",
        "成本效益",
        "质量标准",
        "生产效率",
        "供应链稳定性",
        "工艺创新"
    ]
    
    # 生产可行性评估提示词
    PRODUCTION_FEASIBILITY_PROMPT = """
作为一名文化创意产品生产商，请评估以下剪纸文创产品的生产可行性：

产品设计：
{design}

请从以下方面进行评估：
1. 生产工艺复杂度
2. 所需设备和技术
3. 材料采购难度
4. 生产周期预估
5. 质量控制要点
6. 规模化生产的挑战
7. 可行性结论和建议

请提供详细的生产可行性分析报告。
"""
    
    # 成本分析提示词
    COST_ANALYSIS_PROMPT = """
作为生产商，请对以下产品进行详细的成本分析：

产品信息：
{product_info}

预计产量：{quantity}

请分析以下成本构成：
1. 原材料成本
2. 人工成本
3. 设备折旧
4. 能源消耗
5. 包装成本
6. 运输成本
7. 管理费用
8. 利润空间

请提供详细的成本分解和定价建议。
"""
    
    # 质量控制方案提示词
    QUALITY_CONTROL_PROMPT = """
作为生产商，请为以下产品制定质量控制方案：

产品规格：
{product_specs}

质量要求：
{quality_requirements}

请制定：
1. 原材料检验标准
2. 生产过程控制点
3. 成品检验流程
4. 质量问题处理机制
5. 质量记录和追溯
6. 持续改进措施

请提供完整的质量控制体系方案。
"""
    
    # 供应链管理提示词
    SUPPLY_CHAIN_PROMPT = """
作为生产商，请为以下产品设计供应链管理方案：

产品需求：
{product_requirements}

市场预期：
{market_forecast}

请规划：
1. 供应商选择标准
2. 采购策略和计划
3. 库存管理方案
4. 风险控制措施
5. 成本优化策略
6. 供应链协调机制

请提供完整的供应链管理方案。
"""
    
    # 生产工艺优化提示词
    PROCESS_OPTIMIZATION_PROMPT = """
作为生产商，请对以下生产工艺进行优化：

当前工艺：
{current_process}

存在问题：
{issues}

请提供：
1. 工艺流程优化方案
2. 效率提升措施
3. 成本降低策略
4. 质量改进方法
5. 自动化改造建议
6. 实施计划和预期效果

请提供详细的工艺优化方案。
"""
    
    # 市场定位建议提示词
    MARKET_POSITIONING_PROMPT = """
作为生产商，请为以下产品提供市场定位建议：

产品特点：
{product_features}

竞争环境：
{competition}

请分析：
1. 目标市场细分
2. 产品差异化策略
3. 价格定位建议
4. 销售渠道选择
5. 营销策略建议
6. 市场风险评估

请提供基于生产商视角的市场定位方案。
"""

    # 成本估算提示词
    COST_ESTIMATION_PROMPT = """
作为一名有四年经验的文化创意产品生产商，请为以下剪纸文创产品设计方案估算生产成本：

{design}

请详细列出各项成本，包括：
1. 材料成本
2. 人工成本
3. 设备成本
4. 包装成本
5. 运输成本
6. 其他成本

请以JSON格式返回成本估算结果，格式如下：
{{
    "material_cost": 材料成本,
    "labor_cost": 人工成本,
    "equipment_cost": 设备成本,
    "packaging_cost": 包装成本,
    "shipping_cost": 运输成本,
    "other_cost": 其他成本,
    "total_cost": 总成本,
    "unit_price": 建议单价,
    "profit_margin": 利润率
}}

所有成本单位为人民币（元）。
"""

    @staticmethod
    def get_role_description() -> str:
        """获取角色描述"""
        return ManufacturerPrompts.ROLE_DESCRIPTION
    
    @staticmethod
    def get_skills() -> List[str]:
        """获取专业技能列表"""
        return ManufacturerPrompts.SKILLS.copy()
    
    @staticmethod
    def get_focus_areas() -> List[str]:
        """获取关注领域列表"""
        return ManufacturerPrompts.FOCUS_AREAS.copy()
    
    @staticmethod
    def get_production_feasibility_prompt(design: str) -> str:
        """
        获取生产可行性评估提示词
        
        Args:
            design: 产品设计描述
            
        Returns:
            格式化的生产可行性评估提示词
        """
        return ManufacturerPrompts.PRODUCTION_FEASIBILITY_PROMPT.format(design=design)
    
    @staticmethod
    def get_cost_analysis_prompt(product_info: str, quantity: str) -> str:
        """
        获取成本分析提示词
        
        Args:
            product_info: 产品信息
            quantity: 预计产量
            
        Returns:
            格式化的成本分析提示词
        """
        return ManufacturerPrompts.COST_ANALYSIS_PROMPT.format(
            product_info=product_info,
            quantity=quantity
        )
    
    @staticmethod
    def get_quality_control_prompt(product_specs: str, quality_requirements: str) -> str:
        """
        获取质量控制方案提示词
        
        Args:
            product_specs: 产品规格
            quality_requirements: 质量要求
            
        Returns:
            格式化的质量控制方案提示词
        """
        return ManufacturerPrompts.QUALITY_CONTROL_PROMPT.format(
            product_specs=product_specs,
            quality_requirements=quality_requirements
        )
    
    @staticmethod
    def get_supply_chain_prompt(product_requirements: str, market_forecast: str) -> str:
        """
        获取供应链管理提示词
        
        Args:
            product_requirements: 产品需求
            market_forecast: 市场预期
            
        Returns:
            格式化的供应链管理提示词
        """
        return ManufacturerPrompts.SUPPLY_CHAIN_PROMPT.format(
            product_requirements=product_requirements,
            market_forecast=market_forecast
        )
    
    @staticmethod
    def get_process_optimization_prompt(current_process: str, issues: str) -> str:
        """
        获取生产工艺优化提示词
        
        Args:
            current_process: 当前工艺
            issues: 存在问题
            
        Returns:
            格式化的生产工艺优化提示词
        """
        return ManufacturerPrompts.PROCESS_OPTIMIZATION_PROMPT.format(
            current_process=current_process,
            issues=issues
        )
    
    @staticmethod
    def get_market_positioning_prompt(product_features: str, competition: str) -> str:
        """
        获取市场定位建议提示词

        Args:
            product_features: 产品特点
            competition: 竞争环境

        Returns:
            格式化的市场定位建议提示词
        """
        return ManufacturerPrompts.MARKET_POSITIONING_PROMPT.format(
            product_features=product_features,
            competition=competition
        )

    @staticmethod
    def get_cost_estimation_prompt(design: str) -> str:
        """
        获取成本估算提示词

        Args:
            design: 设计方案

        Returns:
            格式化的成本估算提示词
        """
        return ManufacturerPrompts.COST_ESTIMATION_PROMPT.format(design=design)
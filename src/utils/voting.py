#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
投票机制模块
"""

import logging
import random
from typing import Dict, List, Any, Tuple, Optional


class VotingSystem:
    """投票系统类"""

    def __init__(self, threshold: float = 0.6):
        """
        初始化投票系统

        Args:
            threshold: 投票阈值，默认0.6
        """
        self.threshold = threshold
        self.logger = logging.getLogger("voting_system")

    def black_box_voting(
        self, 
        keywords: List[str], 
        agent_count: int, 
        max_keywords: int = 10
    ) -> List[Tuple[str, int]]:
        """
        黑箱投票

        Args:
            keywords: 关键词列表
            agent_count: 智能体数量
            max_keywords: 最大关键词数量

        Returns:
            投票结果，格式为 [(关键词, 票数), ...]
        """
        self.logger.info(f"开始黑箱投票，关键词数量: {len(keywords)}, 智能体数量: {agent_count}")
        
        # 如果关键词数量小于等于最大关键词数量，直接返回
        if len(keywords) <= max_keywords:
            return [(kw, agent_count) for kw in keywords]
        
        # 初始化投票结果
        votes: Dict[str, int] = {}
        for keyword in keywords:
            votes[keyword] = 0
        
        # 每个智能体投票
        for _ in range(agent_count):
            # 随机选择关键词进行投票
            vote_count = min(len(keywords), max_keywords)
            voted_keywords = random.sample(keywords, vote_count)
            
            for keyword in voted_keywords:
                votes[keyword] += 1
        
        # 排序并返回结果
        sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        
        # 如果设置了阈值，只返回票数超过阈值的关键词
        if self.threshold > 0:
            threshold_count = int(agent_count * self.threshold)
            sorted_votes = [(kw, votes) for kw, votes in sorted_votes if votes >= threshold_count]
        
        # 限制返回数量
        return sorted_votes[:max_keywords]

    def weighted_voting(
        self, 
        keywords: List[Tuple[str, float]], 
        agent_count: int, 
        max_keywords: int = 10
    ) -> List[Tuple[str, float]]:
        """
        加权投票

        Args:
            keywords: 关键词列表，格式为 [(关键词, 权重), ...]
            agent_count: 智能体数量
            max_keywords: 最大关键词数量

        Returns:
            投票结果，格式为 [(关键词, 得分), ...]
        """
        self.logger.info(f"开始加权投票，关键词数量: {len(keywords)}, 智能体数量: {agent_count}")
        
        # 如果关键词数量小于等于最大关键词数量，直接返回
        if len(keywords) <= max_keywords:
            return keywords
        
        # 初始化投票结果
        votes: Dict[str, float] = {}
        for keyword, weight in keywords:
            votes[keyword] = weight
        
        # 排序并返回结果
        sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        
        # 限制返回数量
        return sorted_votes[:max_keywords]

    def consensus_voting(
        self, 
        agent_keywords: Dict[str, List[str]], 
        max_keywords: int = 10
    ) -> List[Tuple[str, int]]:
        """
        共识投票

        Args:
            agent_keywords: 智能体关键词，格式为 {智能体ID: [关键词1, 关键词2, ...], ...}
            max_keywords: 最大关键词数量

        Returns:
            投票结果，格式为 [(关键词, 票数), ...]
        """
        self.logger.info(f"开始共识投票，智能体数量: {len(agent_keywords)}")
        
        # 统计每个关键词的出现次数
        keyword_counts: Dict[str, int] = {}
        for agent_id, keywords in agent_keywords.items():
            for keyword in keywords:
                if keyword in keyword_counts:
                    keyword_counts[keyword] += 1
                else:
                    keyword_counts[keyword] = 1
        
        # 排序并返回结果
        sorted_counts = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        # 如果设置了阈值，只返回票数超过阈值的关键词
        if self.threshold > 0:
            agent_count = len(agent_keywords)
            threshold_count = int(agent_count * self.threshold)
            sorted_counts = [(kw, count) for kw, count in sorted_counts if count >= threshold_count]
        
        # 限制返回数量
        return sorted_counts[:max_keywords]

    def get_final_keywords(
        self, 
        voting_results: List[Tuple[str, Any]], 
        max_keywords: int = 10
    ) -> List[str]:
        """
        获取最终关键词

        Args:
            voting_results: 投票结果，格式为 [(关键词, 票数/得分), ...]
            max_keywords: 最大关键词数量

        Returns:
            最终关键词列表
        """
        # 提取关键词
        keywords = [kw for kw, _ in voting_results]
        
        # 限制数量
        return keywords[:max_keywords]

"""
数据序列化器
将 Python 数据模型转换为 JSON 可序列化的字典格式
"""

from typing import Dict, List, Any
from urllib.parse import unquote
from src.models.checklist import TreeChecklistItem, Issue


def issue_to_summary_dict(issue: Issue) -> Dict[str, Any]:
    """
    将 Issue 转换为摘要字典（用于问题列表展示）

    Args:
        issue: 问题对象

    Returns:
        可 JSON 序列化的字典
    """
    return {
        "title": issue.status,
        "describe": issue.describe,
        "priority": issue.priority,
        "version": issue.version,
        "sourceFile": issue.file_name,
        "howToCheck": {
            "description": issue.describe,
            "knowledgeLinks": [],
            "gifGuides": [],
            "scriptLinks": []
        }
    }


def tree_node_to_dict(node: TreeChecklistItem) -> Dict[str, Any]:
    """
    将 TreeChecklistItem 转换为字典（供 JSON 序列化）

    Args:
        node: 树形检查项节点

    Returns:
        可 JSON 序列化的字典
    """
    # 生成唯一 ID（使用路径连接）
    node_id = "_".join(node.original_path)

    return {
        # 基本信息
        "id": node_id,
        "title": node.status,  # React 使用 title 字段
        "status": node.status,  # 原始 status 字段
        "describe": node.describe,
        "version": node.version,
        "priority": node.priority,  # 数字 1-10

        # HowToCheck 信息
        "howToCheck": {
            "description": node.describe if node.describe else "",
            "knowledgeLinks": [
                {
                    "id": f"wiki_{i}",
                    "title": _extract_link_title(url),
                    "url": url
                }
                for i, url in enumerate(node.wiki_links)
            ],
            "gifGuides": [
                {
                    "id": f"gif_{i}",
                    "title": f"演示 {i+1}",
                    "url": url
                }
                for i, url in enumerate(node.gif_links)
            ],
            "scriptLinks": [
                {
                    "id": f"script_{i}",
                    "title": _extract_script_name(url),
                    "url": url
                }
                for i, url in enumerate(node.script_links)
            ]
        },

        # FixSteps（如果有解决方案）
        "fixSteps": {
            "description": node.todo if node.todo else "",
            "knowledgeLinks": [
                {
                    "id": f"wiki_{i}",
                    "title": _extract_link_title(url),
                    "url": url
                }
                for i, url in enumerate(node.wiki_links)
            ],
            "gifGuides": [
                {
                    "id": f"gif_{i}",
                    "title": f"演示 {i+1}",
                    "url": url
                }
                for i, url in enumerate(node.gif_links)
            ],
            "scriptLinks": [
                {
                    "id": f"script_{i}",
                    "title": _extract_script_name(url),
                    "url": url
                }
                for i, url in enumerate(node.script_links)
            ]
        } if node.todo else None,

        # 来源和路径信息
        "sourceFile": node.source_file,
        "originalPath": node.original_path,
        "isRefer": node.is_refer,
        "parentRef": node.parent_ref,

        # 递归处理子项
        "subCheckItems": [
            tree_node_to_dict(child)
            for child in node.children
        ]
    }


def _extract_link_title(url: str) -> str:
    """
    从 URL 中提取链接标题

    Args:
        url: 链接 URL

    Returns:
        链接标题
    """
    try:
        decoded = unquote(url)
        if "/" in decoded:
            # 取 URL 的最后一部分作为标题
            title = decoded.split("/")[-1]
            # 移除查询参数
            if "?" in title:
                title = title.split("?")[0]
            return title if title else "文档链接"
        return decoded if decoded else "文档链接"
    except Exception:
        return "文档链接"


def _extract_script_name(script_url: str) -> str:
    """
    从脚本 URL 中提取文件名

    Args:
        script_url: 脚本文件 URL

    Returns:
        脚本文件名
    """
    try:
        if "/" in script_url:
            script_name = script_url.split("/")[-1]
        else:
            script_name = script_url

        decoded = unquote(script_name)

        # 移除查询参数
        if "?" in decoded:
            decoded = decoded.split("?")[0]

        return decoded if decoded else "脚本"
    except Exception:
        return "脚本"

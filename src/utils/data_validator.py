"""
数据验证器
负责验证YAML数据的完整性和正确性
"""

import yaml
from pathlib import Path
from typing import List, Dict, Optional


class DataValidator:
    """数据完整性验证器"""

    @staticmethod
    def check_file_integrity(yml_file: Path, data_dir: Path) -> List[str]:
        """检查单个文件的完整性"""
        rel_path = str(yml_file.relative_to(data_dir))
        issues = []

        try:
            with open(yml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # 检查文件是否为空
            if not data:
                issues.append("文件为空")
                return issues

            # 检查必需字段
            if 'status' not in data:
                issues.append("缺少status字段（必需）")
            elif not data['status'] or not str(data['status']).strip():
                issues.append("status字段为空")

            # 检查可选但建议的字段
            if 'describe' not in data:
                issues.append("缺少describe字段（建议添加）")
            elif data['describe'] is None:
                issues.append("describe字段为None（建议添加描述）")
            elif not str(data['describe']).strip():
                issues.append("describe字段为空字符串（建议添加描述）")

            if 'priority' not in data:
                issues.append("缺少priority字段（默认使用5）")
            elif data['priority'] is None:
                issues.append("priority字段为None（默认使用5）")
            elif not isinstance(data['priority'], int) or data['priority'] < 1 or data['priority'] > 10:
                issues.append(f"priority字段值无效: {data['priority']}（应为1-10的整数）")

            if 'version' not in data:
                issues.append("缺少version字段（默认使用'-'）")
            elif data['version'] is None:
                issues.append("version字段为None（建议设置版本范围）")
            elif not str(data['version']).strip():
                issues.append("version字段为空字符串（建议设置版本范围）")

            if 'display' not in data:
                issues.append("缺少display字段（默认为false，不会显示在问题列表中）")
            elif data['display'] is None:
                issues.append("display字段为None（默认为false）")

            if 'checklist' not in data:
                issues.append("缺少checklist字段（没有检查项）")
            elif not data['checklist'] or not isinstance(data['checklist'], list):
                issues.append("checklist字段为空或格式错误")
            else:
                # 检查checklist中的每一项
                for i, item in enumerate(data['checklist']):
                    item_issues = DataValidator._validate_checklist_item(item, i)
                    issues.extend(item_issues)

        except yaml.YAMLError as e:
            issues.append(f"YAML解析错误: {str(e)}")
        except Exception as e:
            issues.append(f"读取文件错误: {str(e)}")

        return issues

    @staticmethod
    def _validate_checklist_item(item: dict, index: int) -> List[str]:
        """验证checklist单项"""
        issues = []

        if not isinstance(item, dict):
            issues.append(f"checklist第{index+1}项格式错误（应为字典）")
            return issues

        # 检查refer或status必须有一个
        has_refer = 'refer' in item
        has_status = 'status' in item

        if not has_refer and not has_status:
            issues.append(f"checklist第{index+1}项缺少refer或status字段")
        elif has_refer:
            if not item['refer'] or not str(item['refer']).strip():
                issues.append(f"checklist第{index+1}项的refer字段为空")
        elif has_status:
            if not item['status'] or not str(item['status']).strip():
                issues.append(f"checklist第{index+1}项的status字段为空")

            if 'describe' not in item or not item['describe']:
                issues.append(f"checklist第{index+1}项缺少describe字段")

            if 'priority' not in item:
                issues.append(f"checklist第{index+1}项缺少priority字段（默认使用5）")
            elif not isinstance(item['priority'], int) or item['priority'] < 1 or item['priority'] > 10:
                issues.append(f"checklist第{index+1}项的priority值无效: {item['priority']}")

            has_sub_checklist = 'checklist' in item and item['checklist']
            if not has_sub_checklist:
                if 'todo' not in item or not item['todo']:
                    issues.append(f"checklist第{index+1}项缺少todo字段（没有解决方案或子检查项）")

        return issues

    @staticmethod
    def validate_issues(issues: Dict[str, 'Issue']) -> List[str]:
        """验证所有问题的数据完整性"""
        errors = []

        for issue_name, issue in issues.items():
            # 验证checklist中的refer引用是否存在
            if hasattr(issue, 'checklist'):
                for item in issue.checklist:
                    if hasattr(item, 'refer') and item.refer and item.refer not in issues:
                        errors.append(f"问题 '{issue_name}' 中的引用 '{item.refer}' 不存在")

        return errors

"""
YAML数据加载和解析器
负责加载和解析运维知识库的YAML文件
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Optional

from ..models.checklist import ChecklistItem, Issue


class DataLoader:
    """YAML数据加载和解析器"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.issues: Dict[str, Issue] = {}
        self.issue_list: List[str] = []

        # 确保数据目录存在
        if not self.data_dir.exists():
            raise FileNotFoundError(f"数据目录不存在: {self.data_dir}")

    def load_all_issues(self) -> Dict[str, Issue]:
        """加载所有yml文件中的问题数据"""
        self.issues.clear()
        self.issue_list.clear()

        # 获取所有yml文件
        yml_files = list(self.data_dir.glob("*.yml")) + list(self.data_dir.glob("*.yaml"))

        if not yml_files:
            print(f"警告: 在 {self.data_dir} 目录下未找到任何yml文件")

        for yml_file in yml_files:
            try:
                issue = self._parse_yml_file(yml_file)
                if issue:
                    self.issues[issue.status] = issue
                    self.issue_list.append(issue.status)
                    print(f"成功加载: {yml_file.name}")
            except Exception as e:
                print(f"解析文件 {yml_file} 失败: {e}")

        print(f"共加载 {len(self.issues)} 个问题")
        return self.issues

    def get_issue_by_name(self, name: str) -> Optional[Issue]:
        """根据名称获取问题"""
        return self.issues.get(name)

    def get_issue_names(self) -> List[str]:
        """获取所有问题名称列表"""
        return self.issue_list.copy()

    def get_all_issues(self) -> Dict[str, Issue]:
        """获取所有问题"""
        return self.issues.copy()

    def reload_data(self) -> bool:
        """重新加载数据"""
        try:
            self.load_all_issues()
            return True
        except Exception as e:
            print(f"重新加载数据失败: {e}")
            return False

    def _parse_yml_file(self, file_path: Path) -> Optional[Issue]:
        """解析单个yml文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if not data:
                print(f"文件 {file_path} 为空")
                return None

            if 'status' not in data:
                print(f"文件 {file_path} 缺少必需的status字段")
                return None

            # 解析checklist项目
            checklist_items = []
            for item_data in data.get('checklist', []):
                checklist_item = self._parse_checklist_item(item_data, file_path.stem)
                if checklist_item:
                    checklist_items.append(checklist_item)

            # 创建Issue对象 - 允许空的describe字段
            issue = Issue(
                file_name=file_path.stem,
                status=data['status'],
                describe=data.get('describe', ''),  # 允许空字符串
                priority=data.get('priority', 5),
                version=data.get('version', '-'),
                checklist=checklist_items
            )

            return issue

        except yaml.YAMLError as e:
            print(f"YAML解析错误 {file_path}: {e}")
        except Exception as e:
            print(f"解析文件 {file_path} 时发生未知错误: {e}")

        return None

    def _parse_checklist_item(self, item_data: dict, source_file: str) -> Optional[ChecklistItem]:
        """解析checklist项目"""
        if not isinstance(item_data, dict):
            print(f"checklist项目格式错误: {item_data}")
            return None

        # 处理refer类型
        if 'refer' in item_data:
            return ChecklistItem(
                status=f"引用: {item_data['refer']}",
                describe=f"关联到问题: {item_data['refer']}",
                priority=item_data.get('priority', 1),
                version=item_data.get('version', '-'),
                todo=f"跳转到问题: {item_data['refer']}",
                refer=item_data['refer']
            )

        # 检查必需字段
        if 'status' not in item_data:
            print(f"checklist项目缺少status字段: {item_data}")
            return None

        # 处理普通checklist项
        checklist_subitems = []
        for subitem_data in item_data.get('checklist', []):
            subitem = self._parse_checklist_item(subitem_data, source_file)
            if subitem:
                checklist_subitems.append(subitem)

        return ChecklistItem(
            status=item_data['status'],
            describe=item_data.get('describe', ''),
            priority=item_data.get('priority', 5),
            version=item_data.get('version', '-'),
            todo=item_data.get('todo', ''),
            checklist=checklist_subitems if checklist_subitems else None,
            refer=item_data.get('refer')
        )

    def validate_data_integrity(self) -> List[str]:
        """验证数据完整性"""
        errors = []

        for issue_name, issue in self.issues.items():
            # 验证checklist中的refer引用是否存在
            for item in issue.checklist:
                if item.refer and item.refer not in self.issues:
                    errors.append(f"问题 '{issue_name}' 中的引用 '{item.refer}' 不存在")

        return errors

    def get_statistics(self) -> Dict[str, int]:
        """获取数据统计信息"""
        total_checklists = sum(len(issue.checklist) for issue in self.issues.values())

        return {
            'total_issues': len(self.issues),
            'total_checklists': total_checklists,
            'avg_checklists_per_issue': total_checklists / len(self.issues) if self.issues else 0
        }
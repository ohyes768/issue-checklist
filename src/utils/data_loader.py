"""
YAML数据加载器
负责加载和解析运维知识库的YAML文件
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional

from ..models.checklist import ChecklistItem, Issue
from .data_validator import DataValidator
from .reference_checker import ReferenceChecker
from .data_quality_reporter import DataQualityReporter


class DataLoader:
    """YAML数据加载和解析器（简化版）"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.issues: Dict[str, Issue] = {}
        self.issue_list: List[str] = []
        self.loaded_files: set = set()  # 记录成功加载的文件
        self.all_yml_files: set = set()  # 记录所有yml文件
        self.file_issues: Dict[str, List[str]] = {}  # 记录每个文件的问题

        # 确保数据目录存在
        if not self.data_dir.exists():
            raise FileNotFoundError(f"数据目录不存在: {self.data_dir}")

    def load_all_issues(self) -> Dict[str, Issue]:
        """加载所有yml文件中的问题数据"""
        self._clear_internal_state()

        # 获取所有yml文件
        yml_files = list(self.data_dir.rglob("*.yml")) + list(self.data_dir.rglob("*.yaml"))

        if not yml_files:
            print(f"警告: 在 {self.data_dir} 目录下未找到任何yml文件")

        self.all_yml_files = set(yml_files)

        # 检查文件完整性并加载数据
        self._check_all_files_integrity(yml_files)
        self._load_yml_files(yml_files)
        self._print_quality_report()

        return self.issues

    def _clear_internal_state(self):
        """清空内部状态"""
        self.issues.clear()
        self.issue_list.clear()
        self.loaded_files.clear()
        self.all_yml_files.clear()
        self.file_issues.clear()

    def _load_yml_files(self, yml_files: List[Path]):
        """加载所有yml文件"""
        for yml_file in yml_files:
            try:
                issue = self._parse_yml_file(yml_file)
                if issue:
                    self.issues[issue.status] = issue
                    self.issue_list.append(issue.status)
                    self.loaded_files.add(yml_file)
                    print(f"成功加载: {yml_file.relative_to(self.data_dir)}")
            except Exception as e:
                print(f"解析文件 {yml_file.relative_to(self.data_dir)} 失败: {e}")

        print(f"共加载 {len(self.issues)} 个问题")

    def get_issue_by_name(self, name: str) -> Optional[Issue]:
        """根据名称获取问题"""
        return self.issues.get(name)

    def get_issue_names(self) -> List[str]:
        """获取所有问题名称列表（仅返回display=True的问题，按优先级降序排列）"""
        visible_issues = [issue for issue in self.issues.values() if issue.display]
        sorted_issues = sorted(visible_issues, key=lambda x: x.priority, reverse=True)
        return [issue.status for issue in sorted_issues]

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

    def validate_data_integrity(self) -> List[str]:
        """验证数据完整性（委托给 DataValidator）"""
        return DataValidator.validate_issues(self.issues)

    def get_statistics(self) -> Dict[str, int]:
        """获取数据统计信息"""
        total_checklists = sum(len(issue.checklist) for issue in self.issues.values())
        return {
            'total_issues': len(self.issues),
            'total_checklists': total_checklists,
            'avg_checklists_per_issue': total_checklists / len(self.issues) if self.issues else 0
        }

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

            # 创建Issue对象
            issue = Issue(
                file_name=file_path.stem,
                status=data['status'],
                describe=data.get('describe', ''),
                priority=data.get('priority', 5),
                version=data.get('version', '-'),
                checklist=checklist_items,
                display=data.get('display', False)
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
                status=item_data['refer'],
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
            wiki_links=item_data.get('wiki_links') or [],
            gif_links=item_data.get('gif_links') or [],
            script_links=item_data.get('script_links') or [],
            checklist=checklist_subitems if checklist_subitems else None,
            refer=item_data.get('refer')
        )

    def _check_all_files_integrity(self, yml_files: List[Path]):
        """检查所有文件的完整性（委托给 DataValidator）"""
        for yml_file in yml_files:
            rel_path = str(yml_file.relative_to(self.data_dir))
            issues = DataValidator.check_file_integrity(yml_file, self.data_dir)
            if issues:
                self.file_issues[rel_path] = issues

    def _check_references(self) -> tuple:
        """检查引用关系并返回结果"""
        checker = ReferenceChecker(self.data_dir, self.all_yml_files, self.issues)
        invalid_refs = checker.check_invalid_references()
        orphan_issues = checker.find_orphan_issues()
        return invalid_refs, orphan_issues

    def _print_quality_report(self):
        """打印数据质量检查报告（委托给 DataQualityReporter）"""
        invalid_refs, orphan_issues = self._check_references()
        DataQualityReporter.print_report(
            self.file_issues,
            invalid_refs,
            orphan_issues
        )

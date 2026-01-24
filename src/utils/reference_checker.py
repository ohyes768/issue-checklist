"""
引用检查器
负责检查YAML文件中的refer引用关系
"""

import yaml
from pathlib import Path
from typing import List, Dict, Set, Optional


class ReferenceChecker:
    """引用关系检查器"""

    def __init__(self, data_dir: Path, all_yml_files: Set[Path], issues: Dict):
        self.data_dir = data_dir
        self.all_yml_files = all_yml_files
        self.issues = issues

    def check_invalid_references(self) -> Dict[str, List[Dict]]:
        """检查所有无效的refer引用"""
        invalid_refs_not_exist = []  # 引用的文件不存在
        invalid_refs_not_loaded = []  # 文件存在但未加载

        for issue_name, issue in self.issues.items():
            if hasattr(issue, 'checklist'):
                self._collect_invalid_references_detailed(
                    issue_name,
                    issue.checklist,
                    invalid_refs_not_exist,
                    invalid_refs_not_loaded
                )

        return {
            'not_exist': invalid_refs_not_exist,
            'not_loaded': invalid_refs_not_loaded
        }

    def collect_referenced_issues(self) -> Set[str]:
        """收集所有被refer引用的问题"""
        referenced = set()

        for issue in self.issues.values():
            if hasattr(issue, 'checklist'):
                self._collect_references(issue.checklist, referenced)

        return referenced

    def find_orphan_issues(self) -> List[str]:
        """找出没被引用但display不为true的问题"""
        referenced = self.collect_referenced_issues()
        orphan_issues = []

        for issue_name, issue in self.issues.items():
            if issue_name not in referenced and not issue.display:
                orphan_issues.append(issue_name)

        return orphan_issues

    def _find_yml_file_by_status(self, status: str) -> Optional[Path]:
        """根据问题状态查找对应的yml文件"""
        for yml_file in self.all_yml_files:
            try:
                with open(yml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and data.get('status') == status:
                        return yml_file
            except Exception:
                continue
        return None

    def _collect_references(self, checklist_items, referenced: Set[str]):
        """递归收集所有被refer引用的问题"""
        for item in checklist_items:
            if hasattr(item, 'refer') and item.refer:
                referenced.add(item.refer)
                if item.refer in self.issues:
                    ref_issue = self.issues[item.refer]
                    if hasattr(ref_issue, 'checklist'):
                        self._collect_references(ref_issue.checklist, referenced)
            elif hasattr(item, 'checklist') and item.checklist:
                self._collect_references(item.checklist, referenced)

    def _collect_invalid_references_detailed(
        self,
        source_issue: str,
        checklist_items,
        invalid_refs_not_exist: List[Dict],
        invalid_refs_not_loaded: List[Dict]
    ):
        """递归收集无效的refer引用"""
        for item in checklist_items:
            if hasattr(item, 'refer') and item.refer and item.refer not in self.issues:
                yml_file = self._find_yml_file_by_status(item.refer)

                if yml_file:
                    rel_path = str(yml_file.relative_to(self.data_dir))
                    reason = self._get_failure_reason(yml_file, item.refer)

                    invalid_refs_not_loaded.append({
                        'source': source_issue,
                        'target': item.refer,
                        'file_path': rel_path,
                        'reason': reason
                    })
                else:
                    invalid_refs_not_exist.append({
                        'source': source_issue,
                        'target': item.refer
                    })

            if hasattr(item, 'checklist') and item.checklist:
                self._collect_invalid_references_detailed(
                    source_issue,
                    item.checklist,
                    invalid_refs_not_exist,
                    invalid_refs_not_loaded
                )

    def _get_failure_reason(self, yml_file: Path, refer_name: str) -> str:
        """获取文件加载失败的具体原因"""
        try:
            with open(yml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if not data:
                    return "文件为空"
                elif 'status' not in data:
                    return "缺少status字段"
                elif data.get('status') != refer_name:
                    return f"文件中的status字段为'{data.get('status')}'，与引用名称'{refer_name}'不匹配"
                else:
                    return "未知原因（可能是解析失败）"
        except Exception as e:
            return f"文件解析错误: {str(e)}"

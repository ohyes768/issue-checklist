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
        self.loaded_files: set = set()  # 记录成功加载的文件
        self.all_yml_files: set = set()  # 记录所有yml文件
        self.file_issues: Dict[str, List[str]] = {}  # 记录每个文件的问题

        # 确保数据目录存在
        if not self.data_dir.exists():
            raise FileNotFoundError(f"数据目录不存在: {self.data_dir}")

    def load_all_issues(self) -> Dict[str, Issue]:
        """加载所有yml文件中的问题数据"""
        self.issues.clear()
        self.issue_list.clear()
        self.loaded_files.clear()
        self.all_yml_files.clear()
        self.file_issues.clear()

        # 获取所有yml文件（包括所有子目录）
        yml_files = list(self.data_dir.rglob("*.yml")) + list(self.data_dir.rglob("*.yaml"))

        if not yml_files:
            print(f"警告: 在 {self.data_dir} 目录下未找到任何yml文件")

        # 记录所有yml文件
        self.all_yml_files = set(yml_files)

        # 先检查所有文件的完整性
        self._check_all_files_integrity(yml_files)

        for yml_file in yml_files:
            try:
                issue = self._parse_yml_file(yml_file)
                if issue:
                    self.issues[issue.status] = issue
                    self.issue_list.append(issue.status)
                    self.loaded_files.add(yml_file)
                    # 显示相对于data目录的路径，便于了解文件来源
                    rel_path = str(yml_file.relative_to(self.data_dir))
                    print(f"成功加载: {rel_path}")
            except Exception as e:
                rel_path = str(yml_file.relative_to(self.data_dir))
                print(f"解析文件 {rel_path} 失败: {e}")

        print(f"共加载 {len(self.issues)} 个问题")

        # 打印数据质量检查报告
        self._print_data_quality_report()

        return self.issues

    def get_issue_by_name(self, name: str) -> Optional[Issue]:
        """根据名称获取问题"""
        return self.issues.get(name)

    def get_issue_names(self) -> List[str]:
        """获取所有问题名称列表（仅返回display=True的问题，按优先级降序排列）"""
        # 过滤display=True的问题，并按优先级降序排列
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
                checklist=checklist_items,
                display=data.get('display', False)  # 默认不显示，除非明确设置为true
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
                status=item_data['refer'],  # 直接使用引用的问题名称
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
            wiki_links=item_data.get('wiki_links'),
            gif_links=item_data.get('gif_links'),
            script_links=item_data.get('script_links'),
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

    def _print_data_quality_report(self):
        """打印数据质量检查报告"""
        print("\n" + "="*60)
        print("📊 数据质量检查报告")
        print("="*60)

        # 1. 显示信息不完整的文件
        if self.file_issues:
            print(f"\n⚠️  以下 {len(self.file_issues)} 个文件信息不完整:")
            for file_path, issues in sorted(self.file_issues.items()):
                print(f"\n   📄 {file_path}:")
                for issue in issues:
                    print(f"      - {issue}")
            print(f"\n   💡 建议: 请补充缺失的字段信息")
        else:
            print("\n✅ 所有文件信息完整")

        # 2. 检查无效的refer引用，并分类
        invalid_refs_not_exist = []  # 引用的文件不存在
        invalid_refs_not_loaded = []  # 文件存在但未加载

        for issue_name, issue in self.issues.items():
            self._collect_invalid_references_detailed(
                issue_name,
                issue.checklist,
                invalid_refs_not_exist,
                invalid_refs_not_loaded
            )

        # 打印文件不存在的引用
        if invalid_refs_not_exist:
            print(f"\n❌ 以下 {len(invalid_refs_not_exist)} 个refer引用的文件不存在:")
            for ref_info in invalid_refs_not_exist:
                print(f"   - 问题 '{ref_info['source']}' 引用了 '{ref_info['target']}'，但文件不存在")
            print("   💡 建议: 请创建对应的yml文件")

        # 打印文件存在但未加载的引用
        if invalid_refs_not_loaded:
            print(f"\n⚠️  以下 {len(invalid_refs_not_loaded)} 个refer引用指向的文件存在但未成功加载:")
            for ref_info in invalid_refs_not_loaded:
                print(f"   - 问题 '{ref_info['source']}' 引用了 '{ref_info['target']}'")
                print(f"     文件: {ref_info['file_path']}")
                print(f"     原因: {ref_info['reason']}")
            print("   💡 建议: 请检查这些yml文件的格式和内容完整性")

        if not invalid_refs_not_exist and not invalid_refs_not_loaded:
            print("\n✅ 所有refer引用都有效")

        # 3. 收集所有被refer引用的问题
        referenced_issues = set()
        for issue in self.issues.values():
            self._collect_referenced_issues(issue.checklist, referenced_issues)

        # 4. 找出没被引用但display不为true的问题
        orphan_issues_not_visible = []
        for issue_name, issue in self.issues.items():
            if issue_name not in referenced_issues and not issue.display:
                orphan_issues_not_visible.append(issue_name)

        if orphan_issues_not_visible:
            print(f"\n⚠️  以下 {len(orphan_issues_not_visible)} 个问题未被任何父问题引用，且display不为true:")
            for issue_name in orphan_issues_not_visible:
                issue = self.issues[issue_name]
                rel_path = f"{issue.file_name}.yml"
                print(f"   - {issue_name} ({rel_path})")
            print("   💡 建议: 这些问题可能需要设置 display: true，或者应该被其他问题引用")
        else:
            print("\n✅ 所有不可见的问题都已被其他问题引用")

        print("="*60 + "\n")

    def _check_all_files_integrity(self, yml_files: List[Path]):
        """检查所有文件的完整性"""
        for yml_file in yml_files:
            rel_path = str(yml_file.relative_to(self.data_dir))
            issues = []

            try:
                with open(yml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                # 检查文件是否为空
                if not data:
                    issues.append("文件为空")
                    self.file_issues[rel_path] = issues
                    continue

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
                        if not isinstance(item, dict):
                            issues.append(f"checklist第{i+1}项格式错误（应为字典）")
                            continue

                        # 检查refer或status必须有一个
                        has_refer = 'refer' in item
                        has_status = 'status' in item

                        if not has_refer and not has_status:
                            issues.append(f"checklist第{i+1}项缺少refer或status字段")
                        elif has_refer:
                            # 如果是refer引用，检查引用是否有效
                            if not item['refer'] or not str(item['refer']).strip():
                                issues.append(f"checklist第{i+1}项的refer字段为空")
                        elif has_status:
                            # 检查status是否为空
                            if not item['status'] or not str(item['status']).strip():
                                issues.append(f"checklist第{i+1}项的status字段为空")

                            # 检查describe
                            if 'describe' not in item or not item['describe']:
                                issues.append(f"checklist第{i+1}项缺少describe字段")

                            # 检查priority
                            if 'priority' not in item:
                                issues.append(f"checklist第{i+1}项缺少priority字段（默认使用5）")
                            elif not isinstance(item['priority'], int) or item['priority'] < 1 or item['priority'] > 10:
                                issues.append(f"checklist第{i+1}项的priority值无效: {item['priority']}")

                            # 检查todo（如果有解决方案）
                            has_sub_checklist = 'checklist' in item and item['checklist']
                            if not has_sub_checklist:
                                if 'todo' not in item or not item['todo']:
                                    issues.append(f"checklist第{i+1}项缺少todo字段（没有解决方案或子检查项）")

                # 如果有问题，记录下来
                if issues:
                    self.file_issues[rel_path] = issues

            except yaml.YAMLError as e:
                self.file_issues[rel_path] = [f"YAML解析错误: {str(e)}"]
            except Exception as e:
                self.file_issues[rel_path] = [f"读取文件错误: {str(e)}"]

    def _collect_referenced_issues(self, checklist_items: List[ChecklistItem], referenced: set):
        """递归收集所有被refer引用的问题"""
        for item in checklist_items:
            if item.refer:
                referenced.add(item.refer)
            # 递归处理子checklist
            if item.checklist:
                self._collect_referenced_issues(item.checklist, referenced)

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

    def _collect_invalid_references_detailed(
        self,
        source_issue: str,
        checklist_items: List[ChecklistItem],
        invalid_refs_not_exist: list,
        invalid_refs_not_loaded: list
    ):
        """递归收集无效的refer引用，并区分文件不存在和文件未加载"""
        for item in checklist_items:
            if item.refer and item.refer not in self.issues:
                # 查找对应的yml文件
                yml_file = self._find_yml_file_by_status(item.refer)

                if yml_file:
                    # 文件存在，但未成功加载
                    rel_path = str(yml_file.relative_to(self.data_dir))
                    reason = "文件存在但未成功加载"

                    # 尝试读取文件判断具体原因
                    try:
                        with open(yml_file, 'r', encoding='utf-8') as f:
                            data = yaml.safe_load(f)
                            if not data:
                                reason = "文件为空"
                            elif 'status' not in data:
                                reason = "缺少status字段"
                            elif data.get('status') != item.refer:
                                reason = f"文件中的status字段为'{data.get('status')}'，与引用名称'{item.refer}'不匹配"
                            else:
                                reason = "未知原因（可能是解析失败）"
                    except Exception as e:
                        reason = f"文件解析错误: {str(e)}"

                    invalid_refs_not_loaded.append({
                        'source': source_issue,
                        'target': item.refer,
                        'file_path': rel_path,
                        'reason': reason
                    })
                else:
                    # 文件不存在
                    invalid_refs_not_exist.append({
                        'source': source_issue,
                        'target': item.refer
                    })

            # 递归处理子checklist
            if item.checklist:
                self._collect_invalid_references_detailed(
                    source_issue,
                    item.checklist,
                    invalid_refs_not_exist,
                    invalid_refs_not_loaded
                )
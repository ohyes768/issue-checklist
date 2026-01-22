"""
树形结构构建器
处理refer引用和树形结构拼接
"""

from typing import Dict, Optional, List, Set

from ..models.checklist import Issue, ChecklistItem, TreeChecklistItem
from .data_loader import DataLoader


class TreeBuilder:
    """树形结构构建器 - 处理refer引用和树形结构拼接"""

    def __init__(self, data_loader: DataLoader):
        self.data_loader = data_loader
        self.built_trees: Dict[str, TreeChecklistItem] = {}
        self.building_stack: Set[str] = set()  # 用于检测循环引用

    def build_complete_tree(self, root_issue_name: str) -> Optional[TreeChecklistItem]:
        """构建完整的树形结构"""
        # 检查缓存
        if root_issue_name in self.built_trees:
            return self.built_trees[root_issue_name]

        # 检查循环引用
        if root_issue_name in self.building_stack:
            print(f"警告: 检测到循环引用: {' → '.join(list(self.building_stack) + [root_issue_name])}")
            return None

        # 获取根问题
        root_issue = self.data_loader.get_issue_by_name(root_issue_name)
        if not root_issue:
            print(f"错误: 未找到问题 '{root_issue_name}'")
            return None

        # 开始构建
        self.building_stack.add(root_issue_name)
        try:
            # 构建根节点
            root_tree = TreeChecklistItem(
                status=root_issue.status,
                describe=root_issue.describe,
                priority=root_issue.priority,
                version=root_issue.version,
                todo="",  # 根问题没有todo
                source_file=root_issue.file_name,
                original_path=[root_issue.status],
                is_refer=False
            )

            # 递归构建子树
            for item in root_issue.checklist:
                child_tree = self._build_child_tree(item, root_issue.file_name, [root_issue.status])
                if child_tree:
                    root_tree.children.append(child_tree)

            # 缓存构建结果
            self.built_trees[root_issue_name] = root_tree
            return root_tree

        finally:
            self.building_stack.remove(root_issue_name)

    def find_node_by_path(self, root_tree: TreeChecklistItem, path: List[str]) -> Optional[TreeChecklistItem]:
        """根据路径查找树节点"""
        if not path or not root_tree:
            return None

        current = root_tree
        # 跳过根节点（path[0] 就是根节点的status）
        for path_part in path[1:]:
            found = False
            for child in current.children:
                # 检查是否匹配
                if child.status == path_part:
                    current = child
                    found = True
                    break

            if not found:
                return None

        return current

    def get_all_referenced_issues(self, root_issue_name: str) -> List[str]:
        """获取所有被引用的问题"""
        root_issue = self.data_loader.get_issue_by_name(root_issue_name)
        if not root_issue:
            return []

        referenced = set()

        def collect_references(items: List[ChecklistItem]):
            for item in items:
                if item.refer:
                    referenced.add(item.refer)
                    # 递归收集被引用问题的引用
                    ref_issue = self.data_loader.get_issue_by_name(item.refer)
                    if ref_issue:
                        collect_references(ref_issue.checklist)
                elif item.checklist:
                    collect_references(item.checklist)

        collect_references(root_issue.checklist)
        return list(referenced)

    def clear_cache(self):
        """清空构建缓存"""
        self.built_trees.clear()
        self.building_stack.clear()

    def _build_child_tree(self, item: ChecklistItem, parent_file: str, path: List[str]) -> Optional[TreeChecklistItem]:
        """构建子树"""
        if hasattr(item, 'refer') and item.refer:
            # 处理refer引用
            return self._build_refer_tree(item.refer, parent_file, path)
        else:
            # 处理普通项
            tree_item = TreeChecklistItem(
                status=item.status,
                describe=item.describe,
                priority=item.priority,
                version=item.version,
                todo=item.todo or "",
                wiki_links=item.wiki_links or [],
                gif_links=item.gif_links or [],
                script_links=item.script_links or [],
                source_file=parent_file,
                original_path=path + [item.status],
                is_refer=False
            )

            # 递归处理子项
            if hasattr(item, 'checklist') and item.checklist:
                for child_item in item.checklist:
                    child_tree = self._build_child_tree(child_item, parent_file, path + [item.status])
                    if child_tree:
                        tree_item.children.append(child_tree)

            return tree_item

    def _build_refer_tree(self, refer_name: str, parent_file: str, path: List[str]) -> Optional[TreeChecklistItem]:
        """构建引用树"""
        # 检查循环引用
        if refer_name in self.building_stack:
            print(f"警告: 在引用中检测到循环: {' → '.join(list(self.building_stack) + [refer_name])}")
            return None

        refer_issue = self.data_loader.get_issue_by_name(refer_name)
        if not refer_issue:
            print(f"警告: 未找到引用的问题 '{refer_name}'")
            return None

        # 添加到构建栈
        self.building_stack.add(refer_name)
        try:
            # 创建引用节点
            refer_tree = TreeChecklistItem(
                status=refer_issue.status,
                describe=refer_issue.describe,
                priority=refer_issue.priority,
                version=refer_issue.version,
                todo="",  # 引用的问题本身没有todo
                wiki_links=[],  # 引用的问题本身不包含wiki链接
                gif_links=[],  # 引用的问题本身不包含gif链接
                script_links=[],  # 引用的问题本身不包含脚本链接
                source_file=refer_issue.file_name,
                original_path=path + [refer_name],  # 移除[引用]前缀
                is_refer=True,
                parent_ref=parent_file
            )

            # 递归构建引用问题的子项
            for item in refer_issue.checklist:
                child_tree = self._build_child_tree(item, refer_issue.file_name, path + [refer_name])  # 移除[引用]前缀
                if child_tree:
                    refer_tree.children.append(child_tree)

            return refer_tree

        finally:
            self.building_stack.remove(refer_name)

    def validate_tree_structure(self, root_issue_name: str) -> List[str]:
        """验证树形结构的完整性"""
        errors = []
        root_tree = self.build_complete_tree(root_issue_name)

        if not root_tree:
            return [f"无法构建问题 '{root_issue_name}' 的树形结构"]

        def validate_node(node: TreeChecklistItem, depth: int = 0):
            # 检查深度限制（防止无限递归）
            if depth > 20:
                errors.append(f"树形结构过深，可能存在循环引用: {' → '.join(node.original_path)}")
                return

            # 检查必需字段
            if not node.status.strip():
                errors.append(f"节点状态为空: {' → '.join(node.original_path)}")
            if node.priority < 1 or node.priority > 10:
                errors.append(f"节点优先级无效 {node.priority}: {' → '.join(node.original_path)}")

            # 递归验证子节点
            for child in node.children:
                validate_node(child, depth + 1)

        validate_node(root_tree)
        return errors
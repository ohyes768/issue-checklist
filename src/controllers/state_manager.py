"""
应用状态管理器
管理排查过程中的状态变化和导航逻辑
"""

from typing import Optional, List, Tuple

from ..models.checklist import AppState, TreeChecklistItem
from ..utils.tree_builder import TreeBuilder


class StateManager:
    """应用状态管理器"""

    def __init__(self, tree_builder: TreeBuilder):
        self.tree_builder = tree_builder
        self.state = AppState()

    def set_current_issue(self, issue_name: str) -> bool:
        """设置当前问题"""
        try:
            # 构建完整的树形结构
            tree = self.tree_builder.build_complete_tree(issue_name)
            if not tree:
                return False

            # 获取Issue对象
            issue = self.tree_builder.data_loader.get_issue_by_name(issue_name)
            if not issue:
                return False

            self.state.current_issue = issue
            self.state.current_issue_name = issue_name
            self.state.current_tree = tree
            self.state.current_checklist = None  # 重置到根节点
            self.state.navigation_path = [issue_name]  # 简化的路径，只包含问题名
            self.state.solution_text = None
            self.state.excluded_items.clear()
            self.state.confirmed_item = None  # 重置已确认项目

            return True
        except Exception as e:
            print(f"设置当前问题失败: {e}")
            return False

    def navigate_to_child(self, child_item: TreeChecklistItem) -> Tuple[bool, Optional[str]]:
        """导航到子节点"""
        try:
            # 无论是否有子节点，都更新当前节点为该检查项
            self.state.current_checklist = child_item

            # 构建简单的导航路径（只保存status名称）
            current_path = []
            current_issue_name = self.state.current_issue_name

            # 添加根节点（问题名）
            if current_issue_name:
                current_path.append(current_issue_name)

            # 添加从根到当前节点的所有检查项名称
            if child_item.original_path:
                current_path.extend(child_item.original_path[1:])  # 跳过根节点，只添加检查项

            self.state.navigation_path = current_path

            if not child_item.has_children():
                # 没有子节点，显示解决方案
                self.state.solution_text = child_item.todo
                return True, child_item.todo
            else:
                # 有子节点，清除解决方案，继续排查
                self.state.solution_text = None
                return True, None

        except Exception as e:
            print(f"导航到子节点失败: {e}")
            return False, None

    def navigate_to_parent(self) -> bool:
        """导航到父节点"""
        if len(self.state.navigation_path) <= 1:
            return False  # 已经在根节点

        try:
            # 移除当前节点
            self.state.navigation_path.pop()

            # 查找父节点
            if self.state.current_tree:
                parent_item = self.tree_builder.find_node_by_path(
                    self.state.current_tree,
                    self.state.navigation_path
                )

                if parent_item:
                    self.state.current_checklist = parent_item
                    self.state.solution_text = None
                    # 清除已确认项目，确保右侧区域同步返回到checklist列表
                    self.state.confirmed_item = None
                    print(f"导航到父节点，清除已确认项目，当前路径: {self.state.navigation_path}")
                    return True

            return False
        except Exception as e:
            print(f"导航到父节点失败: {e}")
            return False

    def navigate_to_path(self, path: List[str]) -> bool:
        """导航到指定路径"""
        if not self.state.current_tree or not path:
            return False

        try:
            target_node = self.tree_builder.find_node_by_path(self.state.current_tree, path)
            if target_node:
                self.state.navigation_path = path.copy()
                self.state.current_checklist = target_node
                self.state.solution_text = None
                # 清除已确认项目，确保右侧区域同步更新
                self.state.confirmed_item = None
                print(f"导航到指定路径，清除已确认项目，新路径: {self.state.navigation_path}")
                return True

            return False
        except Exception as e:
            print(f"导航到指定路径失败: {e}")
            return False

    def navigate_to_root(self) -> bool:
        """导航到根节点"""
        if not self.state.current_tree:
            return False

        self.state.current_checklist = None
        self.state.navigation_path = [self.state.current_issue_name] if self.state.current_issue_name else []
        self.state.solution_text = None
        # 清除已确认项目，确保右侧区域同步返回到根状态
        self.state.confirmed_item = None
        print(f"导航到根节点，清除已确认项目")
        return True

    def exclude_item(self, item: TreeChecklistItem) -> bool:
        """排除检查项"""
        try:
            item_path = item.get_path_display()
            if item_path not in self.state.excluded_items:
                self.state.excluded_items.append(item_path)
                item.excluded = True
            return True
        except Exception as e:
            print(f"排除项目失败: {e}")
            return False

    def confirm_item(self, item: TreeChecklistItem) -> Tuple[bool, Optional[str]]:
        """确认检查项"""
        try:
            item.confirmed = True
            self.state.confirmed_item = item  # 记录已确认的项目

            # 更新导航路径，使其包含当前确认的项目
            if item.original_path:
                # 使用项目的original_path更新导航路径
                self.state.navigation_path = item.original_path.copy()
                print(f"更新导航路径为: {self.state.navigation_path}")  # 调试信息

            # 如果是引用项目，导航到被引用项目的子项
            if item.is_refer:
                if item.has_children():
                    return self.navigate_to_child(item)
                else:
                    return True, None
            else:
                # 普通项目的处理逻辑
                # 如果项目有解决方案且没有子节点，返回解决方案
                if item.todo and not item.has_children():
                    return True, item.todo
                elif item.has_children():
                    # 有子节点，导航到第一层子节点
                    return self.navigate_to_child(item)
                else:
                    # 没有解决方案也没有子节点
                    return True, None
        except Exception as e:
            print(f"确认项目失败: {e}")
            return False, None

    def get_current_checklist_items(self) -> List[TreeChecklistItem]:
        """获取当前层级的checklist项"""
        return self.state.get_current_checklist_items()

    def get_navigation_breadcrumbs(self) -> List[Tuple[str, List[str]]]:
        """获取导航面包屑（标题, 路径）"""
        if not self.state.navigation_path:
            return []

        breadcrumbs = []
        current_path = []

        for i, path_item in enumerate(self.state.navigation_path):
            current_path.append(path_item)

            # 处理显示标题
            display_title = path_item
            if i > 0:  # 不是根节点
                # 查找对应的节点获取完整标题
                if self.state.current_tree:
                    node = self.tree_builder.find_node_by_path(self.state.current_tree, current_path)
                    if node:
                        display_title = node.status

            breadcrumbs.append((display_title, current_path.copy()))

        return breadcrumbs

    def is_item_excluded(self, item: TreeChecklistItem) -> bool:
        """检查项目是否已排除"""
        item_path = item.get_path_display()
        return item_path in self.state.excluded_items

    def get_parent_path(self) -> Optional[List[str]]:
        """获取父级路径"""
        if len(self.state.navigation_path) <= 1:
            return None

        return self.state.navigation_path[:-1].copy()

    def get_current_node(self) -> Optional[TreeChecklistItem]:
        """获取当前节点"""
        if not self.state.current_tree or not self.state.navigation_path:
            return None

        return self.tree_builder.find_node_by_path(
            self.state.current_tree,
            self.state.navigation_path
        )

    def get_display_node(self) -> Optional[TreeChecklistItem]:
        """获取应该在详情面板显示的节点"""
        # 如果有已确认的项目，显示已确认的项目
        if self.state.confirmed_item:
            return self.state.confirmed_item

        # 如果有当前问题，将问题转换为TreeChecklistItem显示
        if self.state.current_issue and self.state.current_tree:
            # 如果导航路径只有根节点，显示问题本身
            if len(self.state.navigation_path) <= 1:
                return self.state.current_tree

            # 如果导航路径有多个节点，显示最后一个导航节点（即当前所在的检查项）
            return self.tree_builder.find_node_by_path(
                self.state.current_tree,
                self.state.navigation_path
            )

        return None

    def has_solution(self) -> bool:
        """当前是否有解决方案"""
        return self.state.solution_text is not None

    def get_solution(self) -> Optional[str]:
        """获取当前解决方案"""
        return self.state.solution_text

    def reset_state(self):
        """重置状态"""
        self.state.reset_state()

    def get_confirmed_item(self) -> Optional[TreeChecklistItem]:
        """获取当前已确认的项目"""
        return self.state.confirmed_item

    def has_confirmed_item(self) -> bool:
        """是否有已确认的项目"""
        return self.state.confirmed_item is not None

    def get_state_summary(self) -> dict:
        """获取状态摘要"""
        current_node = self.get_current_node()
        current_items = self.get_current_checklist_items()

        return {
            'current_issue': self.state.current_issue_name,
            'navigation_path': self.state.navigation_path.copy(),
            'path_display': self.state.get_current_path_display(),
            'current_node_status': current_node.status if current_node else None,
            'current_items_count': len(current_items),
            'excluded_items_count': len(self.state.excluded_items),
            'has_solution': self.has_solution(),
            'is_at_root': self.state.is_at_root(),
            'has_confirmed_item': self.has_confirmed_item()
        }
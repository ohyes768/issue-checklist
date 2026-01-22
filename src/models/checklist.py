"""
Checklist数据模型
定义运维排查助手的核心数据结构
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ChecklistItem:
    """检查项目数据模型"""
    status: str  # 直接原因现象描述
    describe: str  # 详细说明和确认方法
    priority: int  # 优先级(1-10，数字越大越重要)
    version: str  # 影响版本范围
    todo: str  # 解决方案描述
    wiki_links: Optional[List[str]] = None  # Wiki文档链接列表
    gif_links: Optional[List[str]] = None  # GIF演示图链接列表
    script_links: Optional[List[str]] = None  # 脚本文件链接列表
    checklist: Optional[List['ChecklistItem']] = None  # 子checklist
    refer: Optional[str] = None  # 相关问题引用
    excluded: bool = False  # 是否已排除该原因
    confirmed: bool = False  # 是否已确认该原因存在

    def __post_init__(self):
        """数据验证"""
        if self.priority < 1 or self.priority > 10:
            raise ValueError(f"优先级必须在1-10之间，当前值: {self.priority}")
        if not self.status.strip():
            raise ValueError("status不能为空")
        if not self.describe.strip():
            raise ValueError("describe不能为空")


@dataclass
class Issue:
    """问题现象数据模型（支持顶层priority和version）"""
    file_name: str        # yml文件名
    status: str           # 问题现象标题
    describe: str         # 问题描述
    priority: int         # 问题整体优先级
    version: str          # 问题影响版本
    checklist: List[ChecklistItem]  # 直接原因checklist列表
    display: bool = False  # 是否在问题列表中显示，默认为False

    def get_checklist_by_priority(self) -> List[ChecklistItem]:
        """按优先级降序返回checklist"""
        return sorted(self.checklist, key=lambda x: x.priority, reverse=True)

    def __post_init__(self):
        """数据验证"""
        if self.priority < 1 or self.priority > 10:
            raise ValueError(f"优先级必须在1-10之间，当前值: {self.priority}")
        if not self.status.strip():
            raise ValueError("status不能为空")
        # describe可以为空，只检查是否为None
        if self.describe is None:
            raise ValueError("describe不能为None")


@dataclass
class TreeChecklistItem:
    """树形检查项数据模型（支持refer引用和树形结构）"""
    status: str  # 显示标题
    describe: str  # 描述
    priority: int  # 优先级
    version: str  # 版本
    todo: str  # 解决方案
    source_file: str  # 来源yml文件
    original_path: List[str]  # 原始路径（用于导航）
    wiki_links: List[str] = field(default_factory=list)  # Wiki文档链接列表
    gif_links: List[str] = field(default_factory=list)  # GIF演示图链接列表
    script_links: List[str] = field(default_factory=list)  # 脚本文件链接列表
    children: List['TreeChecklistItem'] = field(default_factory=list)  # 子项
    is_refer: bool = False  # 是否为refer引用的项
    parent_ref: Optional[str] = None  # 父级引用来源
    excluded: bool = False  # 是否已排除
    confirmed: bool = False  # 是否已确认

    def get_children_by_priority(self) -> List['TreeChecklistItem']:
        """按优先级降序返回子项"""
        return sorted(self.children, key=lambda x: x.priority, reverse=True)

    def has_children(self) -> bool:
        """是否有子项"""
        return len(self.children) > 0

    def get_path_display(self) -> str:
        """获取路径显示文本"""
        return " → ".join(self.original_path)

    def __post_init__(self):
        """数据验证"""
        if self.priority < 1 or self.priority > 10:
            raise ValueError(f"优先级必须在1-10之间，当前值: {self.priority}")
        if not self.status.strip():
            raise ValueError("status不能为空")


@dataclass
class AppState:
    """应用状态管理（支持树形结构）"""
    current_issue: Optional[Issue] = None  # 当前问题对象
    current_issue_name: Optional[str] = None  # 选择的问题名称
    current_tree: Optional[TreeChecklistItem] = None  # 当前树形结构
    current_checklist: Optional[TreeChecklistItem] = None  # 当前检查项
    excluded_items: List[str] = field(default_factory=list)  # 已排除项目路径
    navigation_path: List[str] = field(default_factory=list)  # 当前导航路径
    solution_text: Optional[str] = None  # 当前显示的解决方案
    confirmed_item: Optional[TreeChecklistItem] = None  # 当前已确认的检查项

    def get_current_path_display(self) -> str:
        """获取当前路径的显示文本"""
        return " → ".join(self.navigation_path) if self.navigation_path else "未开始排查"

    def get_current_checklist_items(self) -> List[TreeChecklistItem]:
        """获取当前层级的checklist项"""
        if not self.current_checklist:
            if self.current_tree:
                return self.current_tree.get_children_by_priority()
            return []

        return self.current_checklist.get_children_by_priority()

    def is_at_root(self) -> bool:
        """是否在根节点"""
        return len(self.navigation_path) <= 1

    def reset_state(self):
        """重置状态"""
        self.current_issue = None
        self.current_issue_name = None
        self.current_tree = None
        self.current_checklist = None
        self.excluded_items.clear()
        self.navigation_path.clear()
        self.solution_text = None
        self.confirmed_item = None
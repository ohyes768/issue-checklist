"""
Streamlit Web应用控制器
负责处理Web界面的渲染和用户交互
"""

import streamlit as st
from typing import Optional, List, Dict

from ..models.checklist import TreeChecklistItem
from ..utils.data_loader import DataLoader
from ..utils.tree_builder import TreeBuilder
from .state_manager import StateManager


class WebController:
    """Streamlit Web应用控制器"""

    def __init__(self):
        self.data_loader = DataLoader()
        self.tree_builder = TreeBuilder(self.data_loader)
        self.state_manager = StateManager(self.tree_builder)

        # 加载数据
        self._load_data()

    def _load_data(self) -> bool:
        """加载初始数据"""
        try:
            self.data_loader.load_all_issues()

            # 验证数据完整性
            errors = self.data_loader.validate_data_integrity()
            if errors:
                for error in errors:
                    st.error(f"数据完整性错误: {error}")

            return True
        except Exception as e:
            st.error(f"加载数据失败: {e}")
            return False

    def render_top_toolbar(self) -> Optional[str]:
        """渲染顶部工具栏并返回选择的问题"""
        # 问题选择和重置按钮放在一行
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            issue_names = self.data_loader.get_issue_names()
            if issue_names:
                selected_issue = st.selectbox(
                    "📋 选择问题现象",
                    options=issue_names,
                    key="issue_selector",
                    index=0 if not st.session_state.get('current_issue') else
                           issue_names.index(st.session_state.get('current_issue', issue_names[0]))
                )
                return selected_issue
            else:
                st.error("未找到任何问题数据")
                return None

        with col2:
            if st.button("🔄 重置", key="reset_button", use_container_width=True):
                self._reset_session_state()
                st.rerun()

        with col3:
            if st.button("🏠 首页", key="home_button", use_container_width=True):
                # 回到根节点
                if self.state_manager.state.current_issue_name:
                    self.state_manager.navigate_to_root()
                st.rerun()

        return None

    def render_main_content(self):
        """渲染主内容区"""
        if not st.session_state.get('current_issue'):
            self._show_welcome_screen()
            return

        # 获取当前状态
        summary = self.state_manager.get_state_summary()

        # 创建三栏布局
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            self._render_navigation_panel()

        with col2:
            self._render_detail_panel()

        with col3:
            if summary['has_solution']:
                self._render_solution_panel()
            else:
                self._render_checklist_panel()

    def handle_issue_selection(self, issue_name: str):
        """处理问题选择"""
        if issue_name != st.session_state.get('current_issue'):
            success = self.state_manager.set_current_issue(issue_name)
            if success:
                st.session_state.current_issue = issue_name
                st.success(f"已加载问题: {issue_name}")
            else:
                st.error(f"加载问题失败: {issue_name}")

    def _render_navigation_panel(self):
        """渲染导航面板"""
        st.subheader("📍 当前排查路径")

        summary = self.state_manager.get_state_summary()
        current_path = summary['navigation_path']

        if not current_path:
            st.info("未开始排查")
            return

        # 树状层级显示，但不区分类型emoji
        for i, path_item in enumerate(current_path):
            if i == len(current_path) - 1:
                # 当前位置高亮显示
                if i == 0:
                    st.markdown(f"◉ **{path_item}**")
                else:
                    indent = "└─ " * (i - 1)
                    st.markdown(f"{indent}◉ **{path_item}**")
            else:
                # 上级路径，可以点击导航
                if i == 0:
                    if st.button(f"{path_item}", key=f"nav_{i}", help="点击跳转到此位置"):
                        # 构建到该位置的路径
                        target_path = current_path[:i+1]
                        self.state_manager.navigate_to_path(target_path)
                        st.rerun()
                else:
                    indent = "└─ " * i
                    if st.button(f"{indent}{path_item}", key=f"nav_{i}", help="点击跳转到此位置"):
                        # 构建到该位置的路径
                        target_path = current_path[:i+1]
                        self.state_manager.navigate_to_path(target_path)
                        st.rerun()

        # 返回上级按钮
        if not summary['is_at_root']:
            if st.button("⬆️ 返回上级", key="nav_parent", use_container_width=True):
                self.state_manager.navigate_to_parent()
                st.rerun()

    def _render_detail_panel(self):
        """渲染详情面板"""
        st.subheader("📋 当前检查项详情")

        current_node = self.state_manager.get_current_node()
        if not current_node:
            st.info("未选择检查项")
            return

        # 获取状态摘要
        summary = self.state_manager.get_state_summary()
        current_path = summary['navigation_path']

        # 根据当前位置决定显示内容
        if summary['is_at_root']:
            # 在根节点时，显示根问题的信息
            if self.state_manager.state.current_issue:
                issue = self.state_manager.state.current_issue
                st.markdown(f"**📁 问题现象**: {issue.status}")
                st.markdown(f"**问题描述**: {issue.describe}")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("问题优先级", issue.priority)
                with col2:
                    st.metric("影响版本", issue.version if issue.version else "-")

                st.info(f"📄 来源文件: {issue.file_name}.yml")
        else:
            # 在子节点时，显示当前检查项的详细信息
            st.markdown(f"**🔍 检查项**: {current_node.status}")
            st.markdown(f"**描述**: {current_node.describe}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("优先级", current_node.priority)
            with col2:
                st.metric("版本", current_node.version if current_node.version else "-")

            # 显示来源信息
            if current_node.is_refer:
                st.info(f"📎 引用自: {current_node.source_file}")
                if current_node.parent_ref:
                    st.info(f"📎 父级引用: {current_node.parent_ref}")
            else:
                st.info(f"📄 来源文件: {current_node.source_file}")

            # 显示路径信息
            if current_path:
                st.info(f"📍 完整路径: {' → '.join(current_path)}")

            # 显示解决方案预览（如果有）
            if current_node.todo:
                with st.expander("🔧 解决方案预览"):
                    st.write(current_node.todo)

            # 显示子项信息（如果有）
            if current_node.has_children():
                child_count = len(current_node.children)
                st.info(f"📋 包含 {child_count} 个子检查项")

    def _render_checklist_panel(self):
        """渲染检查清单面板"""
        st.subheader("✅ Checklist确认")

        current_items = self.state_manager.get_current_checklist_items()

        if not current_items:
            st.info("没有检查项")
            return

        # 按优先级排序并显示（不使用expander，直接显示）
        for i, item in enumerate(current_items):
            # 检查是否已被排除
            is_excluded = self.state_manager.is_item_excluded(item)

            # 根据排除状态应用不同的样式
            if is_excluded:
                # 已排除的项目使用删除线样式和灰色背景
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f0f0f0;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 5px 0;
                        border-left: 4px solid #999;
                    ">
                        <h4 style="color: #999; text-decoration: line-through; margin: 0 0 5px 0;">
                            {item.status} (优先级: {item.priority})
                        </h4>
                        <p style="color: #666; margin: 0;">{item.describe}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                # 未排除的项目正常显示
                st.markdown(
                    f"""
                    <div style="
                        background-color: #ffffff;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 5px 0;
                        border-left: 4px solid #FF6B6B;
                        border: 1px solid #e1e1e1;
                    ">
                        <h4 style="color: #262730; margin: 0 0 5px 0;">
                            {item.status} (优先级: {item.priority})
                        </h4>
                        <p style="color: #666; margin: 0 0 10px 0;">{item.describe}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # 固定的操作按钮
            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button(f"排除", key=f"exclude_{i}", use_container_width=True,
                           disabled=is_excluded, help="标记此原因已被排除"):
                    self.state_manager.exclude_item(item)
                    st.success(f"已排除: {item.status}")
                    st.rerun()

            with col2:
                if st.button(f"确认", key=f"confirm_{i}", use_container_width=True,
                           disabled=is_excluded, help="确认此原因存在"):
                    success, solution = self.state_manager.confirm_item(item)
                    if success:
                        if solution:
                            st.success(f"找到解决方案: {item.status}")
                        else:
                            st.success(f"进入下一层级: {item.status}")
                        st.rerun()
                    else:
                        st.error(f"确认失败: {item.status}")

            # 添加分隔线
            if i < len(current_items) - 1:
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

    def _render_solution_panel(self):
        """渲染解决方案面板"""
        st.subheader("🛠️ 解决方案")

        solution = self.state_manager.get_solution()
        if solution:
            with st.success("已找到解决方案"):
                st.markdown("**操作步骤:**")

                # 解析步骤（简单实现，假设换行分隔）
                lines = solution.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                            st.markdown(f"- {line}")
                        elif line.startswith(('-', '•', '*')):
                            st.markdown(f"- {line}")
                        else:
                            st.markdown(line)

        # 继续排查按钮
        if st.button("🔄 重新排查", key="restart_check", use_container_width=True):
            self.state_manager.set_current_issue(st.session_state.current_issue)
            st.rerun()

    def _show_welcome_screen(self):
        """显示欢迎界面"""
        st.markdown("""
        # 🔧 运维知识库智能排查助手

        请从左侧选择要排查的问题现象，开始智能排查流程。

        ## 使用说明
        1. 从左侧选择问题现象
        2. 查看问题详情
        3. 逐项确认checklist
        4. 获取解决方案

        选择问题后，系统将引导您完成排查流程。
        """)

        # 显示可用的问题
        issue_names = self.data_loader.get_issue_names()
        if issue_names:
            st.markdown("### 📋 可用问题")
            for issue_name in issue_names:
                st.markdown(f"- {issue_name}")

    def _reset_session_state(self):
        """重置会话状态"""
        # 重置状态管理器
        self.state_manager.reset_state()

        # 清除session_state中的业务数据
        keys_to_remove = ['current_issue']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
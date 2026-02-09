"""
Streamlit Web应用控制器
负责协调数据加载、状态管理和界面渲染
"""

import streamlit as st
from typing import Optional, Dict

from ..models.checklist import TreeChecklistItem
from ..utils.data_loader import DataLoader
from ..utils.tree_builder import TreeBuilder
from ..controllers.state_manager import StateManager
from ..controllers.style_manager import StyleManager
from ..controllers.renderer import Renderer
from ..controllers.interaction_handler import InteractionHandler


class WebController:
    """Streamlit Web应用控制器（重构版）"""

    def __init__(self):
        self.data_loader = DataLoader()
        self.tree_builder = TreeBuilder(self.data_loader)
        self.state_manager = StateManager(self.tree_builder)

        # 创建辅助组件
        self.style_manager = StyleManager()
        self.renderer = Renderer(self.style_manager)
        self.interaction_handler = InteractionHandler(self.state_manager, self.renderer)

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

    def render_main_content(self):
        """渲染主内容区"""
        summary = self.state_manager.get_state_summary()

        # 创建两栏布局：左侧导航 + 右侧内容区
        col_left, col_right = st.columns([1.2, 2.8])

        with col_left:
            self._render_left_panel()

        with col_right:
            if not st.session_state.get('current_issue'):
                st.info("👈 请从左侧选择要排查的问题")
            elif summary['has_solution']:
                self.renderer.render_solution_panel(self.state_manager)
            else:
                # 右侧左右分布：中间始终显示当前检查项详情，右侧根据状态显示不同内容
                col_detail, col_action = st.columns([1, 1])

                with col_detail:
                    self.renderer.render_detail_panel(self.state_manager)

                with col_action:
                    confirmed_item = self.state_manager.get_confirmed_item()
                    if confirmed_item:
                        if confirmed_item.is_refer:
                            self.renderer.render_checklist_panel(
                                self.state_manager,
                                self.interaction_handler.handle_confirm_item,
                                self.interaction_handler.handle_exclude_item
                            )
                        else:
                            self._render_solution_with_return(confirmed_item)
                    else:
                        self.renderer.render_checklist_panel(
                            self.state_manager,
                            self.interaction_handler.handle_confirm_item,
                            self.interaction_handler.handle_exclude_item
                        )

    def _render_left_panel(self):
        """渲染左侧面板"""
        selected_issue = self.renderer.render_left_panel(
            self.data_loader,
            self.state_manager,
            'current_issue'
        )

        # 当前排查路径区域
        need_reset = self.renderer.render_navigation_path(self.state_manager)

        if need_reset:
            self.interaction_handler.handle_reset()
            st.rerun()

        # 处理问题选择
        if selected_issue and selected_issue != st.session_state.get('current_issue'):
            if self.interaction_handler.handle_issue_selection(selected_issue, 'current_issue'):
                st.rerun()

    def _render_solution_with_return(self, confirmed_item: TreeChecklistItem):
        """渲染解决方案和返回按钮"""
        self.renderer.render_confirmed_item_solution(confirmed_item)

        # 添加返回按钮
        st.markdown("---")
        if st.button("返回", key="return_checklist", use_container_width=True,
                   help="返回到检查列表"):
            self.interaction_handler.handle_return_to_checklist()
            st.rerun()

    def handle_issue_selection(self, issue_name: str):
        """处理问题选择（公共接口）"""
        self.interaction_handler.handle_issue_selection(issue_name, 'current_issue')

    def reset_session_state(self):
        """重置会话状态（公共接口）"""
        self.interaction_handler.handle_reset()

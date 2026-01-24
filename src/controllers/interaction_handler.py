"""
交互处理器
负责处理用户交互逻辑
"""

import streamlit as st


class InteractionHandler:
    """用户交互处理器"""

    def __init__(self, state_manager, renderer):
        self.state_manager = state_manager
        self.renderer = renderer

    def handle_exclude_item(self, item):
        """处理排除项目"""
        return self.state_manager.exclude_item(item)

    def handle_confirm_item(self, item):
        """处理确认项目"""
        success, solution = self.state_manager.confirm_item(item)
        if success:
            if solution:
                st.success(f"找到解决方案: {item.status}")
            else:
                st.success(f"进入下一层级: {item.status}")
            return True
        else:
            st.error(f"确认失败: {item.status}")
            return False

    def handle_return_to_checklist(self):
        """处理返回检查列表"""
        self.state_manager.state.confirmed_item = None
        current_node = self.state_manager.get_current_node()
        if current_node:
            current_node.confirmed = False

    def handle_reset(self):
        """处理重置会话状态"""
        self.state_manager.reset_state()
        keys_to_remove = ['current_issue']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]

    def handle_issue_selection(self, issue_name: str, current_issue_key: str):
        """处理问题选择"""
        if issue_name != st.session_state.get(current_issue_key):
            success = self.state_manager.set_current_issue(issue_name)
            if success:
                st.session_state[current_issue_key] = issue_name
                return True
            else:
                st.error(f"加载问题失败: {issue_name}")
                return False
        return False

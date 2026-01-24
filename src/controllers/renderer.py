"""
渲染器
负责Streamlit界面的渲染逻辑
"""

import streamlit as st
from urllib.parse import unquote

from ..models.checklist import TreeChecklistItem
from .style_manager import StyleManager


class Renderer:
    """Streamlit界面渲染器"""

    def __init__(self, style_manager: StyleManager):
        self.style_manager = style_manager

    def render_left_panel(self, data_loader, state_manager, current_issue_key: str):
        """渲染左侧面板（包含问题选择和导航路径）"""
        self.style_manager.apply_left_panel_styles()
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)

        # 问题选择区域
        st.markdown("### 📋 选择问题")
        issue_names = data_loader.get_issue_names()
        if issue_names:
            current_issue = st.session_state.get(current_issue_key)
            selected_issue = st.selectbox(
                "问题现象",
                options=issue_names,
                index=0 if not current_issue else issue_names.index(current_issue),
                key="left_panel_issue_selector",
                help="选择要排查的问题"
            )
            return selected_issue

        st.error("未找到任何问题数据")
        return None

    def render_navigation_path(self, state_manager):
        """渲染当前排查路径"""
        st.markdown('<div class="navigation-section">', unsafe_allow_html=True)
        st.markdown("### 📍 当前排查路径")

        summary = state_manager.get_state_summary()
        current_path = summary['navigation_path']

        if not current_path:
            st.info("未开始排查")
            st.markdown('</div></div>', unsafe_allow_html=True)
            return False

        # 渲染路径项
        for i, path_item in enumerate(current_path):
            is_last = i == len(current_path) - 1
            indent = "" if i == 0 else "└─ " * (i if not is_last else i - 1)

            if is_last:
                st.markdown(f'{indent}◉ **{path_item}**')
            else:
                if st.button(f'{indent}◉ **{path_item}**', key=f"nav_{i}", help=f"跳转到 {path_item}"):
                    state_manager.navigate_to_path(current_path[:i+1])
                    st.rerun()

        # 返回上级和重置按钮
        if not summary['is_at_root']:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("返回上级", key="nav_parent", use_container_width=True):
                    state_manager.navigate_to_parent()
                    st.rerun()
            with col2:
                if st.button("重置", key="reset_panel", use_container_width=True):
                    st.markdown('</div></div>', unsafe_allow_html=True)
                    return True

        st.markdown('</div></div>', unsafe_allow_html=True)
        return False

    def render_detail_panel(self, state_manager):
        """渲染详情面板"""
        confirmed_item = state_manager.get_confirmed_item()
        if confirmed_item:
            st.markdown("### ✅ 已确认检查项")
        else:
            st.markdown("### 📋 当前排查进展")

        display_node = state_manager.get_display_node()
        if not display_node:
            st.info("未选择检查项")
            return

        summary = state_manager.get_state_summary()
        current_path = summary['navigation_path']

        # 基本信息
        st.markdown(f"**📋 现象**: {display_node.status}")
        if display_node.describe:
            st.markdown(f"**HowToCheck**: {display_node.describe}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("优先级/出现概率", display_node.priority)
        with col2:
            st.metric("适配版本", display_node.version if display_node.version else "-")
        with col3:
            child_count = len(display_node.children) if display_node.has_children() else 0
            st.metric("检查项数目", child_count)

        # 来源信息
        st.info(f"📄 来源文件: {display_node.source_file}")

        # 根因分析
        path_to_show = confirmed_item.original_path if confirmed_item else display_node.original_path
        if not path_to_show:
            path_to_show = current_path

        if path_to_show and len(path_to_show) > 1:
            reversed_path = list(reversed(path_to_show))
            st.info(f"🔍 根因分析: {' → '.join(reversed_path)}")
        elif path_to_show and len(path_to_show) == 1:
            st.info(f"🔍 根因分析: {path_to_show[0]}")

    def render_checklist_panel(self, state_manager, on_confirm, on_exclude):
        """渲染检查清单面板"""
        st.markdown("### ✅ Checklist确认单")
        current_items = state_manager.get_current_checklist_items()

        if not current_items:
            st.info("没有检查项")
            return

        self.style_manager.apply_compact_card_styles()

        for i, item in enumerate(current_items):
            is_excluded = state_manager.is_item_excluded(item)
            col1, col2 = st.columns([0.8, 4.2])

            with col1:
                if is_excluded:
                    self.style_manager.render_disabled_icon()
                else:
                    col_ex, col_conf = st.columns([1, 1])
                    with col_ex:
                        if st.button("🚫", key=f"exclude_{i}", help="标记此原因已被排除"):
                            on_exclude(item)
                            st.success(f"已排除: {item.status}")
                            st.rerun()
                    with col_conf:
                        if st.button("✅", key=f"confirm_{i}", help="确认此原因存在"):
                            on_confirm(item)
                            st.rerun()

            with col2:
                if is_excluded:
                    st.markdown(self.style_manager.render_excluded_item_card(item), unsafe_allow_html=True)
                else:
                    st.markdown(self.style_manager.render_normal_item_card(item), unsafe_allow_html=True)

            self.style_manager.render_compact_separator(i, len(current_items))

    def render_confirmed_item_solution(self, confirmed_item):
        """渲染已确认项目的解决方案"""
        st.markdown("### 🛠️ 解决方案")
        st.info(f"已确认: {confirmed_item.status}")

        if confirmed_item.todo:
            with st.success("解决方案"):
                st.markdown("**操作步骤:**")
                self._render_solution_text(confirmed_item.todo)

            st.markdown("---")
            self._render_links(confirmed_item)
            st.markdown("---")

            return True
        else:
            if confirmed_item.is_refer:
                st.info("引用项目本身无解决方案，请从右侧排查被引用项目的具体原因")
            else:
                st.warning("该检查项暂无解决方案，请返回排查其他项目")

            return False

    def _render_solution_text(self, todo_text: str):
        """渲染解决方案文本"""
        lines = todo_text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 判断是否为列表项
            if line[0].isdigit() and '.' in line and len(line) > 2 and line[1] == '.':
                st.markdown(f"- {line}")
            elif line.startswith(('-', '•', '*')):
                st.markdown(f"- {line}")
            else:
                st.markdown(line)

    def _render_links(self, item: TreeChecklistItem):
        """渲染相关链接"""
        links_to_render = [
            ("📚 相关文档", item.wiki_links, lambda url: unquote(url)),
            ("🎬 演示视频", item.gif_links, lambda url: unquote(url)),
            ("📜 相关脚本", item.script_links, self._extract_script_name),
        ]

        for title, links, name_func in links_to_render:
            if links:
                st.markdown(f"### {title}")
                for url in links:
                    st.markdown(f'- [{name_func(url)}]({url})', unsafe_allow_html=True)

    @staticmethod
    def _extract_script_name(script_url: str) -> str:
        """从脚本URL中提取文件名"""
        if "/" in script_url:
            script_name = script_url.split("/")[-1]
        else:
            script_name = script_url
        return unquote(script_name)

    def render_solution_panel(self, state_manager):
        """渲染解决方案面板"""
        st.markdown("### 🛠️ 解决方案")
        solution = state_manager.get_solution()
        if solution:
            with st.success("已找到解决方案"):
                st.markdown("**操作步骤:**")
                self._render_solution_text(solution)

        if st.button("🔄 重新排查", key="restart_check", use_container_width=True):
            state_manager.set_current_issue(st.session_state.current_issue)
            st.rerun()

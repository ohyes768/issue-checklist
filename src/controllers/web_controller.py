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

    
    def render_main_content(self):
        """渲染主内容区"""
        # 获取当前状态
        summary = self.state_manager.get_state_summary()

        # 创建两栏布局：左侧导航 + 右侧内容区
        col_left, col_right = st.columns([1.2, 2.8])

        with col_left:
            self._render_left_panel()

        with col_right:
            if not st.session_state.get('current_issue'):
                # 如果还没有选择问题，显示提示
                st.info("👈 请从左侧选择要排查的问题")
            elif summary['has_solution']:
                self._render_solution_panel()
            else:
                # 右侧左右分布：中间始终显示当前检查项详情，右侧根据状态显示不同内容
                col_detail, col_action = st.columns([1, 1])

                # 中间始终显示当前检查项详情
                with col_detail:
                    self._render_detail_panel()

                # 右侧根据状态显示不同内容
                with col_action:
                    confirmed_item = self.state_manager.get_confirmed_item()
                    if confirmed_item:
                        # 如果确认的是引用项目，显示被引用项目的checklist
                        if confirmed_item.is_refer:
                            self._render_checklist_panel()
                        else:
                            # 普通项目显示解决方案
                            self._render_confirmed_item_solution(confirmed_item)
                    else:
                        # 没有已确认项目时，显示当前层级的checklist列表
                        self._render_checklist_panel()

    def handle_issue_selection(self, issue_name: str):
        """处理问题选择"""
        if issue_name != st.session_state.get('current_issue'):
            success = self.state_manager.set_current_issue(issue_name)
            if success:
                st.session_state.current_issue = issue_name
                # 移除成功提示，让界面更简洁
            else:
                st.error(f"加载问题失败: {issue_name}")

    def _render_left_panel(self):
        """渲染左侧面板（包含问题选择和导航路径）"""
        # 添加紧凑的左侧面板样式
        st.markdown("""
        <style>
        .left-panel .stSelectbox > div > div {
            font-size: 0.9em !important;
            padding: 0.25rem 0.5rem !important;
        }
        .navigation-section {
            margin-top: 20px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 6px;
        }
        .navigation-path {
            font-size: 0.9em;
            line-height: 1.3;
        }
        .navigation-path button {
            font-size: 0.85em;
            padding: 0.2rem 0.4rem;
            margin: 0.1rem 0;
            height: auto;
        }
                </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="left-panel">', unsafe_allow_html=True)

        # 问题选择区域
        st.markdown("### 📋 选择问题")

        issue_names = self.data_loader.get_issue_names()
        if issue_names:
            current_issue = st.session_state.get('current_issue')
            selected_issue = st.selectbox(
                "问题现象",
                options=issue_names,
                index=0 if not current_issue else issue_names.index(current_issue),
                key="left_panel_issue_selector",
                help="选择要排查的问题"
            )

            # 处理问题选择
            if selected_issue != current_issue:
                self.handle_issue_selection(selected_issue)
                st.rerun()
        else:
            st.error("未找到任何问题数据")

        # 当前排查路径区域
        st.markdown('<div class="navigation-section">', unsafe_allow_html=True)
        st.markdown("### 📍 当前排查路径")

        summary = self.state_manager.get_state_summary()
        current_path = summary['navigation_path']

        if not current_path:
            st.info("未开始排查")
        else:
            # 树状层级显示 - 使用下划线链接
            for i, path_item in enumerate(current_path):
                if i == len(current_path) - 1:
                    # 当前位置高亮显示
                    if i == 0:
                        st.markdown(f'◉ **{path_item}**')
                    else:
                        indent = "└─ " * (i - 1)
                        st.markdown(f'{indent}◉ **{path_item}**')
                else:
                    # 上级路径，使用普通文字按钮
                    if i == 0:
                        if st.button(f'◉ **{path_item}**', key=f"nav_{i}", help=f"跳转到 {path_item}"):
                            # 构建到该位置的路径
                            target_path = current_path[:i+1]
                            self.state_manager.navigate_to_path(target_path)
                            st.rerun()
                    else:
                        indent = "└─ " * i
                        if st.button(f'{indent}◉ **{path_item}**', key=f"nav_{i}", help=f"跳转到 {path_item}"):
                            # 构建到该位置的路径
                            target_path = current_path[:i+1]
                            self.state_manager.navigate_to_path(target_path)
                            st.rerun()

            # 返回上级按钮和重置按钮
            if not summary['is_at_root']:
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("⬆️ 返回上级", key="nav_parent", use_container_width=True):
                        self.state_manager.navigate_to_parent()
                        st.rerun()
                with col2:
                    if st.button("🔄 重置", key="reset_panel", use_container_width=True):
                        self._reset_session_state()
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    def _render_detail_panel(self):
        """渲染详情面板"""
        # 使用更紧凑的标题
        confirmed_item = self.state_manager.get_confirmed_item()
        if confirmed_item:
            st.markdown("### ✅ 已确认检查项")
        else:
            st.markdown("### 📋 当前排查进展")

        # 使用新的get_display_node方法获取要显示的节点
        display_node = self.state_manager.get_display_node()

        if not display_node:
            st.info("未选择检查项")
            return

        # 获取状态摘要
        summary = self.state_manager.get_state_summary()
        current_path = summary['navigation_path']

        # 统一显示检查项的详细信息（包括问题本身）
        st.markdown(f"**📋 现象**: {display_node.status}")

        if display_node.describe:
            st.markdown(f"**HowToCheck**: {display_node.describe}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("优先级/出现概率", display_node.priority)
        with col2:
            st.metric("适配版本", display_node.version if display_node.version else "-")
        with col3:
            # 计算检查项数目
            if display_node.has_children():
                child_count = len(display_node.children)
                st.metric("检查项数目", child_count)
            else:
                st.metric("检查项数目", 0)

        # 显示来源信息（统一格式）
        st.info(f"📄 来源文件: {display_node.source_file}")

        # 显示根因分析（反序显示因果关系）
        if confirmed_item:
            path_to_show = confirmed_item.original_path
        elif display_node.original_path:
            path_to_show = display_node.original_path
        else:
            path_to_show = current_path

        if path_to_show and len(path_to_show) > 1:
            # 反序显示：当前现象 -> 父级现象 -> 最终问题
            # 例如：yarn节点所在磁盘占用>90% -> yarn节点异常 -> 日志引擎启动异常
            # 表示：因为当前现象，导致父级现象，最终导致日志引擎启动异常
            reversed_path = list(reversed(path_to_show))
            st.info(f"🔍 根因分析: {' → '.join(reversed_path)}")
        elif path_to_show and len(path_to_show) == 1:
            # 只有一个项目时，显示为当前问题的根因分析
            st.info(f"🔍 根因分析: {path_to_show[0]}")

        # 子项信息已在上方metric中显示，不再重复显示

    def _render_checklist_panel(self):
        """渲染检查清单面板"""
        # 使用更紧凑的标题
        st.markdown("### ✅ Checklist确认单")

        current_items = self.state_manager.get_current_checklist_items()

        if not current_items:
            st.info("没有检查项")
            return

        # 按优先级排序并显示（不使用expander，直接显示）
        for i, item in enumerate(current_items):
            # 检查是否已被排除
            is_excluded = self.state_manager.is_item_excluded(item)

            # 添加紧凑样式CSS
            st.markdown("""
            <style>
            .compact-card {
                padding: 8px !important;
                margin: 3px 0 !important;
                border-radius: 4px !important;
                font-size: 0.9em !important;
            }
            .compact-card h4 {
                font-size: 0.95em !important;
                margin: 0 0 3px 0 !important;
                line-height: 1.2 !important;
            }
            .compact-card p {
                font-size: 0.85em !important;
                margin: 0 !important;
                line-height: 1.3 !important;
            }
            </style>
            """, unsafe_allow_html=True)

            # 在每项前面放置小图标按钮
            col1, col2 = st.columns([0.8, 4.2])

            with col1:
                # 放置按钮，垂直居中对齐
                if is_excluded:
                    # 已排除的项显示禁用状态的图标
                    st.markdown("""
                    <div style="display: flex; align-items: center; justify-content: center; gap: 5px; height: 100%; margin-top: 5px;">
                        <span style="opacity: 0.4; font-size: 1.5em;">🚫</span>
                        <span style="opacity: 0.4; font-size: 1.5em;">✅</span>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # 可点击的图标按钮
                    col_ex, col_conf = st.columns([1, 1])
                    with col_ex:
                        if st.button("🚫", key=f"exclude_{i}", help="标记此原因已被排除"):
                            self.state_manager.exclude_item(item)
                            st.success(f"已排除: {item.status}")
                            st.rerun()
                    with col_conf:
                        if st.button("✅", key=f"confirm_{i}", help="确认此原因存在"):
                            success, solution = self.state_manager.confirm_item(item)
                            if success:
                                if solution:
                                    st.success(f"找到解决方案: {item.status}")
                                else:
                                    st.success(f"进入下一层级: {item.status}")
                                st.rerun()
                            else:
                                st.error(f"确认失败: {item.status}")

            with col2:
                # 根据排除状态应用不同的样式
                if is_excluded:
                    # 已排除的项目使用删除线样式和灰色背景
                    st.markdown(
                        f"""
                        <div class="compact-card" style="
                            background-color: #f0f0f0;
                            border-left: 4px solid #999;
                            margin-left: 0;
                        ">
                            <h4 style="color: #999; text-decoration: line-through;">
                                {item.status} ({item.version if item.version else '全版本'})
                            </h4>
                            <p style="color: #666;">{item.describe}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    # 未排除的项目正常显示，并添加hover效果
                    st.markdown(
                        f"""
                        <div class="compact-card" style="
                            background-color: #ffffff;
                            border-left: 4px solid #FF6B6B;
                            border: 1px solid #e1e1e1;
                            margin-left: 0;
                            cursor: pointer;
                        " onmouseover="this.style.backgroundColor='#f8f9fa'"
                           onmouseout="this.style.backgroundColor='#ffffff'">
                            <h4 style="color: #262730;">
                                {item.status} ({item.version if item.version else '全版本'})
                            </h4>
                            <p style="color: #666;">{item.describe}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            # 添加紧凑的分隔线
            if i < len(current_items) - 1:
                st.markdown("<hr style='margin: 5px 0; border-color: #e1e1e1;'>", unsafe_allow_html=True)

    def _render_confirmed_item_solution(self, confirmed_item):
        """渲染已确认项目的解决方案"""
        st.markdown("### 🛠️ 解决方案")

        # 显示已确认的项目名称（统一格式）
        st.info(f"已确认: {confirmed_item.status}")

        if confirmed_item.todo:
            with st.success("解决方案"):
                st.markdown("**操作步骤:**")
                # 解析步骤（简单实现，假设换行分隔）
                lines = confirmed_item.todo.split('\n')
                for line in lines:
                    line = line.strip()
                    if line:
                        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                            st.markdown(f"- {line}")
                        elif line.startswith(('-', '•', '*')):
                            st.markdown(f"- {line}")
                        else:
                            st.markdown(line)

            st.markdown("---")

            # 📚 Wiki文档链接
            if confirmed_item.wiki_links:
                st.markdown("### 📚 相关文档")
                for wiki_url in confirmed_item.wiki_links:
                    from urllib.parse import unquote
                    decoded_url = unquote(wiki_url)
                    st.markdown(f'- [{decoded_url}]({wiki_url})', unsafe_allow_html=True)

            # 🎬 GIF演示链接
            if confirmed_item.gif_links:
                st.markdown("### 🎬 演示视频")
                for gif_url in confirmed_item.gif_links:
                    from urllib.parse import unquote
                    decoded_url = unquote(gif_url)
                    st.markdown(f'- [{decoded_url}]({gif_url})', unsafe_allow_html=True)

            # 📜 脚本文件链接
            if confirmed_item.script_links:
                st.markdown("### 📜 相关脚本")
                for script_url in confirmed_item.script_links:
                    from urllib.parse import unquote
                    # 提取文件名并解码
                    script_name = script_url.split("/")[-1] if "/" in script_url else script_url
                    decoded_name = unquote(script_name)
                    st.markdown(f'- [{decoded_name}]({script_url})', unsafe_allow_html=True)

            # 添加操作按钮
            st.markdown("---")
            if st.button("🔙 返回", key="return_checklist", use_container_width=True,
                       help="返回到检查列表"):
                # 重置已确认项目，回到checklist
                self.state_manager.state.confirmed_item = None
                # 确保当前检查项状态正确
                current_node = self.state_manager.get_current_node()
                if current_node:
                    current_node.confirmed = False
                st.rerun()
        else:
            if confirmed_item.is_refer:
                st.info("引用项目本身无解决方案，请从右侧排查被引用项目的具体原因")
            else:
                st.warning("该检查项暂无解决方案，请返回排查其他项目")

            if st.button("🔙 返回", key="return_checklist_no_solution", use_container_width=True):
                self.state_manager.state.confirmed_item = None
                # 确保当前检查项状态正确
                current_node = self.state_manager.get_current_node()
                if current_node:
                    current_node.confirmed = False
                st.rerun()

    def _render_solution_panel(self):
        """渲染解决方案面板"""
        # 使用更紧凑的标题
        st.markdown("### 🛠️ 解决方案")

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

    
    def _reset_session_state(self):
        """重置会话状态"""
        # 重置状态管理器
        self.state_manager.reset_state()

        # 清除session_state中的业务数据
        keys_to_remove = ['current_issue']
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
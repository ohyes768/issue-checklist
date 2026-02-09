"""
样式管理器
负责管理Streamlit界面的CSS样式
"""

import streamlit as st


class StyleManager:
    """CSS样式管理器"""

    @staticmethod
    def apply_left_panel_styles():
        """应用左侧面板样式"""
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

    @staticmethod
    def apply_compact_card_styles():
        """应用紧凑卡片样式"""
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

    @staticmethod
    def render_excluded_item_card(item) -> str:
        """渲染已排除项目的卡片样式"""
        return f"""
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
        """

    @staticmethod
    def render_normal_item_card(item) -> str:
        """渲染正常项目的卡片样式"""
        return f"""
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
        """

    @staticmethod
    def render_compact_separator(index: int, total: int):
        """渲染紧凑分隔线"""
        if index < total - 1:
            st.markdown("<hr style='margin: 5px 0; border-color: #e1e1e1;'>", unsafe_allow_html=True)

    @staticmethod
    def render_disabled_icon():
        """渲染禁用状态的图标"""
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: center; gap: 5px; height: 100%; margin-top: 5px;">
            <span style="opacity: 0.4; font-size: 1.5em;">🚫</span>
            <span style="opacity: 0.4; font-size: 1.5em;">✅</span>
        </div>
        """, unsafe_allow_html=True)

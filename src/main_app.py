"""
Streamlit主应用类
运维知识库智能排查助手的主入口
"""

import traceback
from pathlib import Path

import streamlit as st

# 添加项目路径
project_root = Path(__file__).parent.parent
import sys
sys.path.insert(0, str(project_root))

from src.controllers.web_controller import WebController


def _initialize_controller():
    """初始化应用控制器"""
    if 'controller' not in st.session_state:
        try:
            st.session_state.controller = WebController()
            print("应用控制器初始化成功")
        except Exception as e:
            st.error(f"初始化失败: {e}")
            print(f"初始化错误: {traceback.format_exc()}")
            st.stop()


def _render_footer():
    """渲染页脚"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
            运维知识库智能排查助手 v1.0 |
            基于 Streamlit 构建 |
            <a href='https://github.com/anthropics/claude-code' target='_blank'>Claude Code</a> 生成
        </div>
        """,
        unsafe_allow_html=True
    )


def main():
    """主函数"""
    # 设置页面配置（必须是第一个Streamlit命令）
    st.set_page_config(
        page_title="运维知识库智能排查助手",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # 设置页面标题样式
    st.html("""
    <style>
    .stApp header {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
    }
    </style>
    """)

    try:
        # 初始化控制器
        _initialize_controller()

        # 渲染主内容区
        controller = st.session_state.controller
        controller.render_main_content()

        # 页脚信息
        _render_footer()

    except Exception as e:
        st.error(f"应用运行错误: {e}")
        print(f"运行错误: {traceback.format_exc()}")

        # 提供重新加载选项
        if st.button("重新加载应用"):
            st.session_state.clear()
            st.rerun()


if __name__ == "__main__":
    main()
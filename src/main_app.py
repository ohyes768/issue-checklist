"""
Streamlit主应用类
运维知识库智能排查助手的主入口
"""

import sys
import traceback
from pathlib import Path

import streamlit as st

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.controllers.web_controller import WebController


class MainApp:
    """Streamlit主应用类"""

    def __init__(self):
        self.controller = None
        self.setup_page_config()

    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="运维知识库智能排查助手",
            page_icon="🔧",
            layout="wide",
            initial_sidebar_state="collapsed"
        )

    def initialize_session_state(self):
        """初始化Streamlit会话状态"""
        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = True
            st.session_state.current_issue = None

            # 初始化控制器
            try:
                self.controller = WebController()
                st.session_state.controller = self.controller
                print("应用控制器初始化成功")
            except Exception as e:
                st.error(f"初始化失败: {e}")
                print(f"初始化错误: {traceback.format_exc()}")
                st.stop()

    def run(self):
        """运行主应用"""
        try:
            # 初始化会话状态
            self.initialize_session_state()

            # 获取控制器
            if 'controller' not in st.session_state:
                st.error("应用未正确初始化，请刷新页面")
                return

            controller = st.session_state.controller

            # 渲染顶部工具栏
            selected_issue = controller.render_top_toolbar()

            # 处理问题选择
            if selected_issue:
                controller.handle_issue_selection(selected_issue)

            # 渲染主内容区
            controller.render_main_content()

            # 页脚信息
            self._render_footer()

        except Exception as e:
            st.error(f"应用运行错误: {e}")
            print(f"运行错误: {traceback.format_exc()}")

            # 提供重新加载选项
            if st.button("🔄 重新加载应用"):
                st.session_state.clear()
                st.rerun()

    def _render_footer(self):
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
    try:
        # 设置错误处理
        def handle_error():
            st.error("应用遇到错误，请刷新页面重试")
            st.text(traceback.format_exc())

        # 设置页面标题
        st.html("""
        <style>
        .stApp header {
            background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        }
        </style>
        """)

        # 创建并运行应用
        app = MainApp()
        app.run()

    except Exception as e:
        print(f"应用启动失败: {e}")
        print(traceback.format_exc())

        # 显示错误页面
        st.error(f"应用启动失败: {e}")
        st.text(traceback.format_exc())


if __name__ == "__main__":
    main()
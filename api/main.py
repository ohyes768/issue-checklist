"""
FastAPI 后端应用入口
提供运维知识库的 RESTful API 接口
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

# 添加项目路径
import sys
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.data_loader import DataLoader
from src.utils.tree_builder import TreeBuilder
from api.serializers import tree_node_to_dict, issue_to_summary_dict

# 创建 FastAPI 应用
app = FastAPI(
    title="运维知识库 API",
    description="运维排查知识库的 RESTful API 接口",
    version="1.0.0"
)

# CORS 配置（允许所有来源访问，方便局域网调试）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=False,  # 使用通配符时必须为 False
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据加载器和树构建器
data_loader = DataLoader(data_dir="data")
data_loader.load_all_issues()
tree_builder = TreeBuilder(data_loader)


@app.get("/")
async def root():
    """API 根路径，返回欢迎信息"""
    return {
        "message": "运维知识库 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "issues": "/api/issues",
            "issues_summary": "/api/issues/summary",
            "issue_tree": "/api/issues/{issue_name}/tree",
            "reload": "/api/reload"
        }
    }


@app.get("/api/issues")
async def get_issues():
    """
    获取所有 display=True 的问题列表

    Returns:
        {
            "issues": ["问题1", "问题2", ...],  # 按优先级降序排列
            "total": 问题总数
        }
    """
    try:
        issues = data_loader.get_issue_names()
        return {
            "issues": issues,
            "total": len(issues)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")


@app.get("/api/issues/summary")
async def get_issues_summary():
    """
    获取所有 display=True 的问题摘要列表（包含详细信息）

    Returns:
        {
            "issues": [
                {
                    "title": "问题标题",
                    "describe": "问题描述",
                    "priority": 8,
                    "version": "版本号",
                    "sourceFile": "文件名",
                    "howToCheck": {
                        "description": "检查方法描述",
                        "knowledgeLinks": [],
                        "gifGuides": [],
                        "scriptLinks": []
                    }
                },
                ...
            ],
            "total": 问题总数
        }
    """
    try:
        all_issues = data_loader.get_all_issues()
        visible_issues = [issue for issue in all_issues.values() if issue.display]
        sorted_issues = sorted(visible_issues, key=lambda x: x.priority, reverse=True)

        issues_summary = [issue_to_summary_dict(issue) for issue in sorted_issues]

        return {
            "issues": issues_summary,
            "total": len(issues_summary)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题摘要列表失败: {str(e)}")


@app.get("/api/issues/{issue_name}/tree")
async def get_issue_tree(issue_name: str):
    """
    获取问题的完整树形结构（包含 refer 引用解析）

    Args:
        issue_name: 问题名称

    Returns:
        TreeChecklistItem 的字典表示
    """
    try:
        tree = tree_builder.build_complete_tree(issue_name)
        if not tree:
            raise HTTPException(status_code=404, detail=f"问题 '{issue_name}' 不存在或无法构建树形结构")

        return tree_node_to_dict(tree)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题树失败: {str(e)}")


@app.post("/api/reload")
async def reload_data():
    """
    重新加载数据文件

    用于在更新 YAML 文件后刷新数据，无需重启服务

    Returns:
        {
            "success": true/false,
            "message": "重新加载结果消息"
        }
    """
    try:
        success = data_loader.reload_data()
        tree_builder.clear_cache()

        if success:
            # 重新统计信息
            stats = data_loader.get_statistics()
            return {
                "success": True,
                "message": "数据重新加载成功",
                "stats": stats
            }
        else:
            return {
                "success": False,
                "message": "数据重新加载失败"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"重新加载数据失败: {str(e)}")


@app.get("/api/stats")
async def get_statistics():
    """
    获取数据统计信息

    Returns:
        {
            "total_issues": 问题总数,
            "total_checklists": 检查项总数,
            "avg_checklists_per_issue": 平均每个问题的检查项数量
        }
    """
    try:
        stats = data_loader.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    print("启动运维知识库 API 服务器...")
    print("API 文档: http://localhost:8000/docs")
    print("问题列表: http://localhost:8000/api/issues")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式，代码修改自动重启
    )

"""
API 测试脚本
测试 FastAPI 后端是否正常工作
"""

import requests
import json
from urllib.parse import urlencode

BASE_URL = "http://localhost:8000"


def test_root():
    """测试根路径"""
    print("=" * 50)
    print("测试: GET /")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_get_issues():
    """测试获取问题列表"""
    print("\n" + "=" * 50)
    print("测试: GET /api/issues")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/api/issues")
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"问题总数: {data.get('total', 0)}")
        print(f"问题列表: {data.get('issues', [])[:5]}...")  # 只显示前5个
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_get_issue_tree():
    """测试获取单个问题的树形结构"""
    print("\n" + "=" * 50)
    print("测试: GET /api/issues/{issue_name}/tree")
    print("=" * 50)

    # 使用一个已知的问题名称
    issue_name = "数据留存相关"
    try:
        url = f"{BASE_URL}/api/issues/{issue_name}/tree"
        print(f"请求 URL: {url}")
        response = requests.get(url)
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            tree = response.json()
            print(f"问题标题: {tree.get('title', '')}")
            print(f"优先级: {tree.get('priority', 0)}")
            print(f"子项数量: {len(tree.get('subCheckItems', []))}")
            print(f"是否引用: {tree.get('isRefer', False)}")
            print(f"来源文件: {tree.get('sourceFile', '')}")
            # 不打印完整的树，太大了
        else:
            print(f"错误响应: {response.text}")

        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False


def test_get_stats():
    """测试获取统计信息"""
    print("\n" + "=" * 50)
    print("测试: GET /api/stats")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"错误: {e}")
        return False


def main():
    """运行所有测试"""
    print("开始测试运维知识库 API...")
    print(f"API 地址: {BASE_URL}")
    print("请确保 API 服务器已启动（运行: uv run uvicorn api.main:app --reload --port 8000）")
    print("\n")

    results = {
        "根路径": test_root(),
        "问题列表": test_get_issues(),
        "问题树形结构": test_get_issue_tree(),
        "统计信息": test_get_stats(),
    }

    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")

    total = len(results)
    passed = sum(results.values())
    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n所有测试通过！API 工作正常。")
    else:
        print(f"\n有 {total - passed} 个测试失败，请检查。")


if __name__ == "__main__":
    main()

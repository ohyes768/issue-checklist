"""
数据质量报告生成器
负责生成和打印数据质量检查报告
"""

import sys
import io
from typing import List, Dict

# 设置标准输出编码为 UTF-8（兼容 Windows）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class DataQualityReporter:
    """数据质量报告生成器"""

    @staticmethod
    def print_report(file_issues: Dict[str, List[str]],
                     invalid_refs: Dict[str, List[Dict]],
                     orphan_issues: List[str]):
        """打印完整的数据质量检查报告"""
        print("\n" + "="*60)
        print("[数据质量检查报告]")
        print("="*60)

        # 1. 显示信息不完整的文件
        DataQualityReporter._print_file_issues(file_issues)

        # 2. 显示无效的引用
        DataQualityReporter._print_reference_issues(invalid_refs)

        # 3. 显示孤立问题
        DataQualityReporter._print_orphan_issues(orphan_issues)

        print("="*60 + "\n")

    @staticmethod
    def _print_file_issues(file_issues: Dict[str, List[str]]):
        """打印文件问题"""
        if file_issues:
            print(f"\n[!] 以下 {len(file_issues)} 个文件信息不完整:")
            for file_path, issues in sorted(file_issues.items()):
                print(f"\n   [FILE] {file_path}:")
                for issue in issues:
                    print(f"      - {issue}")
            print(f"\n   [TIP] 建议: 请补充缺失的字段信息")
        else:
            print("\n[OK] 所有文件信息完整")

    @staticmethod
    def _print_reference_issues(invalid_refs: Dict[str, List[Dict]]):
        """打印引用问题"""
        invalid_refs_not_exist = invalid_refs.get('not_exist', [])
        invalid_refs_not_loaded = invalid_refs.get('not_loaded', [])

        # 打印文件不存在的引用
        if invalid_refs_not_exist:
            print(f"\n[X] 以下 {len(invalid_refs_not_exist)} 个refer引用的文件不存在:")
            for ref_info in invalid_refs_not_exist:
                print(f"   - 问题 '{ref_info['source']}' 引用了 '{ref_info['target']}'，但文件不存在")
            print("   [TIP] 建议: 请创建对应的yml文件")

        # 打印文件存在但未加载的引用
        if invalid_refs_not_loaded:
            print(f"\n[!] 以下 {len(invalid_refs_not_loaded)} 个refer引用指向的文件存在但未成功加载:")
            for ref_info in invalid_refs_not_loaded:
                print(f"   - 问题 '{ref_info['source']}' 引用了 '{ref_info['target']}'")
                print(f"     文件: {ref_info['file_path']}")
                print(f"     原因: {ref_info['reason']}")
            print("   [TIP] 建议: 请检查这些yml文件的格式和内容完整性")

        if not invalid_refs_not_exist and not invalid_refs_not_loaded:
            print("\n[OK] 所有refer引用都有效")

    @staticmethod
    def _print_orphan_issues(orphan_issues: List[str]):
        """打印孤立问题"""
        if orphan_issues:
            print(f"\n[!] 以下 {len(orphan_issues)} 个问题未被任何父问题引用，且display不为true:")
            for issue_name in orphan_issues:
                print(f"   - {issue_name}")
            print("   [TIP] 建议: 这些问题可能需要设置 display: true，或者应该被其他问题引用")
        else:
            print("\n[OK] 所有不可见的问题都已被其他问题引用")

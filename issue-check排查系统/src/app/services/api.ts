/**
 * 知识库 API 服务
 * 负责与后端 FastAPI 通信
 */

import type { CheckItem } from '../types/knowledge-base';

// API 基础 URL（从环境变量读取，默认 localhost:8000）
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

/**
 * 问题摘要接口
 */
export interface IssueSummary {
  title: string;
  describe: string;
  priority: number;
  version: string;
  sourceFile: string;
  checklistCount: number;
  howToCheck: {
    description: string;
    knowledgeLinks: Array<{ id: string; title: string; url: string }>;
    gifGuides: Array<{ id: string; title: string; url: string }>;
    scriptLinks: Array<{ id: string; title: string; url: string }>;
  };
}

/**
 * 知识库 API 接口
 */
export const knowledgeApi = {
  /**
   * 获取所有问题列表
   * @returns 问题名称数组（按优先级降序）
   */
  async getIssues(): Promise<string[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/issues`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      return data.issues || [];
    } catch (error) {
      console.error('获取问题列表失败:', error);
      throw error;
    }
  },

  /**
   * 获取所有问题摘要列表
   * @returns 问题摘要数组（按优先级降序）
   */
  async getIssuesSummary(): Promise<IssueSummary[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/issues/summary`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      return data.issues || [];
    } catch (error) {
      console.error('获取问题摘要列表失败:', error);
      throw error;
    }
  },

  /**
   * 获取指定问题的树形结构
   * @param issueName 问题名称
   * @returns 问题的完整树形结构
   */
  async getIssueTree(issueName: string): Promise<CheckItem> {
    try {
      const encodedName = encodeURIComponent(issueName);
      const response = await fetch(`${API_BASE_URL}/api/issues/${encodedName}/tree`);

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error(`问题 '${issueName}' 不存在`);
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      // 直接使用 response.json()，让浏览器自动解析
      const data = await response.json();

      return data;
    } catch (error) {
      console.error('获取问题树失败:', error);
      throw error;
    }
  },

  /**
   * 重新加载数据文件
   * @returns 是否成功
   */
  async reloadData(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/reload`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return data.success || false;
    } catch (error) {
      console.error('重新加载数据失败:', error);
      throw error;
    }
  },

  /**
   * 获取统计信息
   * @returns 统计数据
   */
  async getStats(): Promise<{
    total_issues: number;
    total_checklists: number;
    avg_checklists_per_issue: number;
  }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/stats`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('获取统计信息失败:', error);
      throw error;
    }
  },
};

/**
 * API 辅助函数：检查 API 是否可用
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/`, { method: 'GET' });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * API 辅助函数：获取 API 基础 URL
 */
export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

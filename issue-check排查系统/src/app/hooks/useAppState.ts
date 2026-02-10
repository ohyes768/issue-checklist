/**
 * 应用状态管理 Hook
 * 管理排查系统的全局状态和操作
 */

import { useState, useCallback, useMemo } from 'react';
import type { CheckItem, ItemState } from '../types/knowledge-base';
import { knowledgeApi, type IssueSummary } from '../services/api';

/**
 * 应用状态管理 Hook
 */
export function useAppState() {
  // ===== 状态定义 =====

  // 问题列表（所有可用的根问题）
  const [issues, setIssues] = useState<IssueSummary[]>([]);

  // 当前选中的问题（树形结构的根）
  const [selectedIssue, setSelectedIssue] = useState<CheckItem | null>(null);

  // 当前导航路径（问题 ID 数组）
  const [currentPath, setCurrentPath] = useState<string[]>([]);

  // 所有检查项的状态（Map<itemId, ItemState>）
  const [issueStates, setIssueStates] = useState<Map<string, ItemState>>(new Map());

  // 已排除的项目 ID 集合
  const [excludedItems, setExcludedItems] = useState<Set<string>>(new Set());

  // 当前已确认的检查项
  const [confirmedItem, setConfirmedItem] = useState<CheckItem | null>(null);

  // 加载状态
  const [isLoading, setIsLoading] = useState(false);

  // 错误信息
  const [error, setError] = useState<string | null>(null);

  // ===== 辅助函数 =====

  /**
   * 查找节点（根据 ID）
   */
  const findNodeById = useCallback((id: string, node: CheckItem): CheckItem | null => {
    if (node.id === id) return node;

    if (node.subCheckItems) {
      for (const child of node.subCheckItems) {
        const found = findNodeById(id, child);
        if (found) return found;
      }
    }

    return null;
  }, []);

  /**
   * 获取当前节点
   */
  const getCurrentNode = useCallback((): CheckItem | null => {
    if (!selectedIssue || currentPath.length === 0) return null;
    const currentId = currentPath[currentPath.length - 1];
    return findNodeById(currentId, selectedIssue);
  }, [selectedIssue, currentPath, findNodeById]);

  /**
   * 获取面包屑路径
   */
  const getBreadcrumbPath = useCallback((): CheckItem[] => {
    if (!selectedIssue || currentPath.length === 0) return [];

    return currentPath
      .map(id => findNodeById(id, selectedIssue))
      .filter(Boolean) as CheckItem[];
  }, [selectedIssue, currentPath, findNodeById]);

  // ===== 数据加载 =====

  /**
   * 加载问题列表
   */
  const loadIssues = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const issueList = await knowledgeApi.getIssuesSummary();
      setIssues(issueList);
    } catch (err) {
      const message = err instanceof Error ? err.message : '获取问题列表失败';
      setError(message);
      console.error('加载问题列表失败:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  /**
   * 选择问题并加载树形结构
   */
  const selectIssue = useCallback(async (issueName: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const tree = await knowledgeApi.getIssueTree(issueName);
      setSelectedIssue(tree);
      setCurrentPath([tree.id]);
      setIssueStates(new Map());
      setExcludedItems(new Set());
      setConfirmedItem(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : '加载问题失败';
      setError(message);
      console.error('选择问题失败:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // ===== 导航操作 =====

  /**
   * 导航到指定节点
   */
  const navigateTo = useCallback((itemId: string) => {
    const node = selectedIssue ? findNodeById(itemId, selectedIssue) : null;
    if (!node) {
      console.warn(`未找到节点: ${itemId}`);
      return;
    }

    const index = currentPath.indexOf(itemId);
    if (index !== -1) {
      // 回退到路径中的某个节点
      setCurrentPath(currentPath.slice(0, index + 1));
    } else {
      // 前进到新节点
      setCurrentPath([...currentPath, itemId]);
    }

    // 清除已确认项
    setConfirmedItem(null);

    // 清除该节点所有直接子节点的状态
    // 这样检查单列表会重置为初始状态
    if (node.subCheckItems && node.subCheckItems.length > 0) {
      const newStates = new Map(issueStates);
      node.subCheckItems.forEach((child) => {
        newStates.delete(child.id);
      });
      setIssueStates(newStates);
    }
  }, [currentPath, selectedIssue, issueStates, findNodeById]);

  /**
   * 返回上一级
   */
  const goBack = useCallback(() => {
    if (currentPath.length > 1) {
      setCurrentPath(currentPath.slice(0, -1));
      setConfirmedItem(null);
    }
  }, [currentPath]);

  /**
   * 返回首页
   */
  const goHome = useCallback(() => {
    setSelectedIssue(null);
    setCurrentPath([]);
    setIssueStates(new Map());
    setExcludedItems(new Set());
    setConfirmedItem(null);
    setError(null);
  }, []);

  // ===== 检查项操作 =====

  /**
   * 确认检查项
   */
  const confirmItem = useCallback((itemId: string) => {
    const node = selectedIssue ? findNodeById(itemId, selectedIssue) : null;
    if (!node) {
      console.warn(`未找到节点: ${itemId}`);
      return;
    }

    // 只对有子项的节点保存确认状态
    // 叶子节点（最终问题）不保存状态，这样返回上一级时会自动重置
    const hasChildren = node.subCheckItems && node.subCheckItems.length > 0;

    if (hasChildren) {
      // 更新状态（仅对有子项的节点）
      const newStates = new Map(issueStates);
      newStates.set(itemId, {
        id: itemId,
        status: 'confirmed',
        confirmedAt: new Date(),
      });
      setIssueStates(newStates);
    }

    // 设置已确认项（用于显示解决方案）
    setConfirmedItem(node);

    // 始终导航到该节点（无论是否有子项）
    // 这样问题详情区域会显示当前节点的内容
    setCurrentPath([...currentPath, itemId]);
  }, [issueStates, selectedIssue, currentPath, findNodeById]);

  /**
   * 排除检查项（可撤销）
   */
  const excludeItem = useCallback((itemId: string) => {
    const newStates = new Map(issueStates);
    const current = newStates.get(itemId);

    if (current?.status === 'excluded') {
      // 撤销排除
      newStates.set(itemId, {
        id: itemId,
        status: 'pending',
      });
      setExcludedItems(prev => {
        const next = new Set(prev);
        next.delete(itemId);
        return next;
      });
    } else {
      // 标记排除
      newStates.set(itemId, {
        id: itemId,
        status: 'excluded',
      });
      setExcludedItems(prev => new Set(prev).add(itemId));
    }

    setIssueStates(newStates);
  }, [issueStates]);

  /**
   * 返回检查列表（从解决方案返回）
   */
  const returnToChecklist = useCallback(() => {
    setConfirmedItem(null);
  }, []);

  // ===== 重置操作 =====

  /**
   * 重置所有状态
   */
  const resetState = useCallback(() => {
    setSelectedIssue(null);
    setCurrentPath([]);
    setIssueStates(new Map());
    setExcludedItems(new Set());
    setConfirmedItem(null);
    setError(null);
  }, []);

  // ===== 导出 =====

  return {
    // 状态
    issues,
    selectedIssue,
    currentPath,
    issueStates,
    excludedItems,
    confirmedItem,
    isLoading,
    error,
    currentNode: getCurrentNode(),
    breadcrumbPath: getBreadcrumbPath(),

    // 数据加载
    loadIssues,
    selectIssue,

    // 导航
    navigateTo,
    goBack,
    goHome,

    // 检查项操作
    confirmItem,
    excludeItem,
    returnToChecklist,

    // 重置
    resetState,
    setError,
  };
}

/**
 * 类型导出：useAppState 返回值类型
 */
export type AppState = ReturnType<typeof useAppState>;

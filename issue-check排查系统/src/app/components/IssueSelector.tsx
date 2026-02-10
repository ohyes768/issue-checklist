import { useEffect, useState, useMemo } from 'react';
import { Button } from '@/app/components/ui/button';
import { Card } from '@/app/components/ui/card';
import { Badge } from '@/app/components/ui/badge';
import { AlertCircle, Loader2, Search } from 'lucide-react';
import type { IssueSummary } from '@/app/services/api';
import { pinyin } from 'pinyin-pro';

interface IssueSelectorProps {
  issues: IssueSummary[];
  isLoading: boolean;
  error: string | null;
  onLoadIssues: () => void;
  onSelectIssue: (issueName: string) => void;
}

/**
 * 问题选择器组件（首页）
 * 显示所有可排查的问题列表
 */
export function IssueSelector({
  issues,
  isLoading,
  error,
  onLoadIssues,
  onSelectIssue,
}: IssueSelectorProps) {
  // 搜索关键词状态
  const [searchKeyword, setSearchKeyword] = useState('');

  // 组件挂载时加载问题列表
  useEffect(() => {
    if (issues.length === 0 && !error) {
      onLoadIssues();
    }
  }, []);

  /**
   * 过滤问题列表（支持中文和拼音模糊搜索）
   */
  const filteredIssues = useMemo(() => {
    if (!searchKeyword.trim()) {
      return issues;
    }

    const keyword = searchKeyword.toLowerCase().trim();

    return issues.filter((issue) => {
      // 1. 匹配中文标题
      if (issue.title.toLowerCase().includes(keyword)) {
        return true;
      }

      // 2. 匹配中文描述
      if (issue.describe.toLowerCase().includes(keyword)) {
        return true;
      }

      // 3. 匹配拼音（全拼）
      try {
        const titlePinyin = pinyin(issue.title, { toneType: 'none', type: 'array' });
        const pinyinString = Array.isArray(titlePinyin) ? titlePinyin.join('').toLowerCase() : String(titlePinyin).toLowerCase();
        if (pinyinString.includes(keyword)) {
          return true;
        }
      } catch (e) {
        // 拼音转换失败时忽略错误，继续其他匹配
      }

      // 4. 匹配拼音首字母
      try {
        const titlePinyinFirst = pinyin(issue.title, { pattern: 'first', toneType: 'none', type: 'array' });
        const pinyinFirstString = Array.isArray(titlePinyinFirst) ? titlePinyinFirst.join('').toLowerCase() : String(titlePinyinFirst).toLowerCase();
        if (pinyinFirstString.includes(keyword)) {
          return true;
        }
      } catch (e) {
        // 拼音转换失败时忽略错误，继续其他匹配
      }

      return false;
    });
  }, [issues, searchKeyword]);

  /**
   * 获取搜索结果数量
   */
  const resultCount = filteredIssues.length;
  const isSearching = searchKeyword.trim().length > 0;

  /**
   * 根据优先级数字获取颜色样式
   */
  const getPriorityColor = (priority: number): string => {
    if (priority >= 8) {
      return 'bg-red-100 text-red-800 border-red-200';
    } else if (priority >= 5) {
      return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    } else {
      return 'bg-green-100 text-green-800 border-green-200';
    }
  };

  /**
   * 根据优先级数字获取标签
   */
  const getPriorityLabel = (priority: number): string => {
    if (priority >= 8) return '高';
    if (priority >= 5) return '中';
    return '低';
  };

  // 加载中状态
  if (isLoading && issues.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-lg text-gray-600">正在加载问题列表...</p>
        </div>
      </div>
    );
  }

  // 错误状态
  if (error && issues.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8 flex items-center justify-center">
        <Card className="max-w-md w-full p-8 text-center">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">加载失败</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <Button onClick={onLoadIssues} variant="outline">
            <RefreshCw className="w-4 h-4 mr-2" />
            重试
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* 标题 */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold mb-3 text-gray-900">大数据平台运维知识库</h1>
          <p className="text-lg text-gray-600">选择您遇到的表象问题，开始排查</p>
        </div>

        {/* 搜索框 */}
        <div className="mb-6 max-w-2xl mx-auto">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="搜索问题（支持中文、拼音、拼音首字母）"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              className="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition-all"
            />
            {searchKeyword && (
              <button
                onClick={() => setSearchKeyword('')}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            )}
          </div>
          {isSearching && (
            <p className="text-sm text-gray-600 mt-2 text-center">
              找到 <span className="font-semibold text-blue-600">{resultCount}</span> 个相关问题
            </p>
          )}
        </div>

        {/* 问题列表 - 4列网格布局 */}
        {filteredIssues.length === 0 ? (
          <Card className="p-12 text-center">
            {isSearching ? (
              <div>
                <p className="text-gray-500 mb-2">未找到匹配的问题</p>
                <button
                  onClick={() => setSearchKeyword('')}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  清除搜索条件
                </button>
              </div>
            ) : (
              <p className="text-gray-500">暂无可排查的问题</p>
            )}
          </Card>
        ) : (
          <div className="grid gap-3 grid-cols-4">
            {filteredIssues.map((issue) => {
              const priority = issue.priority;

              return (
                <Card
                  key={issue.title}
                  className="p-4 hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-blue-300"
                  onClick={() => onSelectIssue(issue.title)}
                >
                  {/* 头部：图标和优先级 */}
                  <div className="flex items-start justify-between mb-2">
                    <AlertCircle className="w-5 h-5 text-blue-600 flex-shrink-0" />
                    <Badge className={getPriorityColor(priority)} variant="outline">
                      P{priority}
                    </Badge>
                  </div>

                  {/* 标题 */}
                  <h3 className="text-base font-semibold mb-2 line-clamp-2">{issue.title}</h3>

                  {/* 描述 */}
                  <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                    {issue.describe}
                  </p>

                  {/* 开始按钮 */}
                  <Button className="w-full" variant="outline" size="sm">
                    开始排查
                  </Button>
                </Card>
              );
            })}
          </div>
        )}

        {/* 统计信息 */}
        <div className="mt-6 text-center text-sm text-gray-500">
          {isSearching ? (
            <>显示 {resultCount} / {issues.length} 个问题</>
          ) : (
            <>共 {issues.length} 个问题可排查</>
          )}
        </div>
      </div>
    </div>
  );
}

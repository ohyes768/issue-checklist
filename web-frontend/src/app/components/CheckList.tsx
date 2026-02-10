import { useMemo } from 'react';
import { CheckItem, ItemState } from '@/app/types/knowledge-base';
import { Button } from '@/app/components/ui/button';
import { Card } from '@/app/components/ui/card';
import { Badge } from '@/app/components/ui/badge';
import { CheckCircle2, XCircle, AlertCircle, Link as LinkIcon } from 'lucide-react';

interface CheckListProps {
  checkItems: CheckItem[];
  issueStates: Map<string, ItemState>;
  onConfirm: (itemId: string) => void;
  onExclude: (itemId: string) => void;
}

/**
 * 检查单列表组件
 * 显示当前层级的检查项，支持确认/排除操作
 */
export function CheckList({
  checkItems,
  issueStates,
  onConfirm,
  onExclude,
}: CheckListProps) {
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

  // 按优先级降序排序
  const sortedItems = useMemo(() => {
    return [...checkItems].sort((a, b) => b.priority - a.priority);
  }, [checkItems]);

  // 空状态
  if (!checkItems || checkItems.length === 0) {
    return (
      <div className="h-full flex flex-col">
        <div className="p-4 border-b">
          <h2 className="font-semibold">检查单列表</h2>
        </div>
        <div className="flex-1 flex items-center justify-center p-6">
          <div className="text-center text-gray-500">
            <AlertCircle className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>此问题没有子检查项</p>
            <p className="text-sm mt-2">这是一个最终确认的问题，请查看修复步骤</p>
          </div>
        </div>
      </div>
    );
  }

  // 统计状态
  const stats = {
    total: checkItems.length,
    confirmed: checkItems.filter((item) => issueStates.get(item.id)?.status === 'confirmed').length,
    excluded: checkItems.filter((item) => issueStates.get(item.id)?.status === 'excluded').length,
    pending: checkItems.filter(
      (item) => !issueStates.get(item.id) || issueStates.get(item.id)?.status === 'pending'
    ).length,
  };

  return (
    <div className="h-full flex flex-col">
      {/* 标题栏 */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between mb-2">
          <h2 className="font-semibold">检查单列表</h2>
          <span className="text-sm text-gray-500">
            {stats.confirmed + stats.excluded} / {stats.total}
          </span>
        </div>
        <div className="flex gap-4 text-xs text-gray-600">
          <span className="flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3 text-green-600" />
            已确认: {stats.confirmed}
          </span>
          <span className="flex items-center gap-1">
            <XCircle className="w-3 h-3 text-gray-400" />
            已排除: {stats.excluded}
          </span>
          <span className="flex items-center gap-1">
            <AlertCircle className="w-3 h-3 text-blue-500" />
            待检查: {stats.pending}
          </span>
        </div>
      </div>

      {/* 检查项列表 */}
      <div className="flex-1 overflow-auto p-4 space-y-3">
        {sortedItems.map((item) => {
          const itemState = issueStates.get(item.id);
          const status = itemState?.status || 'pending';

          return (
            <Card
              key={item.id}
              className={`p-4 transition-all ${
                status === 'confirmed'
                  ? 'bg-green-50 border-green-200'
                  : status === 'excluded'
                  ? 'bg-gray-50 border-gray-200 opacity-60'
                  : 'hover:shadow-md'
              }`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3
                      className={`font-medium ${status === 'excluded' ? 'line-through text-gray-400' : ''}`}
                    >
                      {item.title}
                    </h3>
                    {status === 'confirmed' && (
                      <CheckCircle2 className="w-5 h-5 text-green-600 flex-shrink-0" />
                    )}
                    {status === 'excluded' && (
                      <Badge variant="outline" className="bg-gray-200 text-gray-600 border-gray-300">
                        <XCircle className="w-3 h-3 mr-1" />
                        已排除
                      </Badge>
                    )}
                  </div>
                  <div className="flex gap-2 mb-2">
                    <Badge className={getPriorityColor(item.priority)} variant="outline">
                      {getPriorityLabel(item.priority)} ({item.priority})
                    </Badge>
                    {item.isRefer && (
                      <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                        <LinkIcon className="w-3 h-3 mr-1" />
                        根因复用
                      </Badge>
                    )}
                    <Badge variant="outline">{item.version}</Badge>
                    {item.sourceFile && (
                      <Badge variant="outline" className="text-xs">
                        {item.sourceFile}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>

              <p className={`text-sm mb-3 line-clamp-2 ${
                status === 'excluded' ? 'text-gray-400 line-through' : 'text-gray-600'
              }`}>
                {item.describe}
              </p>

              {/* 操作按钮 */}
              <div className="flex gap-2">
                {status === 'pending' && (
                  <>
                    <Button
                      onClick={() => onConfirm(item.id)}
                      size="sm"
                      className="bg-green-600 hover:bg-green-700"
                    >
                      <CheckCircle2 className="w-4 h-4 mr-1" />
                      确认是此问题
                    </Button>
                    <Button onClick={() => onExclude(item.id)} size="sm" variant="outline">
                      <XCircle className="w-4 h-4 mr-1" />
                      排除
                    </Button>
                  </>
                )}

                {status === 'confirmed' && (
                  <div className="w-full">
                    {item.fixSteps ? (
                      <div className="p-3 bg-green-100 border border-green-300 rounded">
                        <div className="flex items-center gap-2 text-sm text-green-800 font-medium mb-2">
                          <CheckCircle2 className="w-4 h-4" />
                          解决方案
                        </div>
                        <p className="text-sm text-gray-700 whitespace-pre-line">
                          {item.fixSteps.description}
                        </p>
                      </div>
                    ) : item.subCheckItems && item.subCheckItems.length > 0 ? (
                      <div className="flex items-center gap-2 text-sm text-green-700">
                        <CheckCircle2 className="w-4 h-4" />
                        <span className="font-medium">已确认，点击左侧树继续排查子问题</span>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <AlertCircle className="w-4 h-4" />
                        <span>此问题暂无解决方案</span>
                      </div>
                    )}
                  </div>
                )}

                {status === 'excluded' && (
                  <Button
                    onClick={() => onExclude(item.id)}
                    size="sm"
                    variant="outline"
                    className="border-blue-300 text-blue-700 hover:bg-blue-50"
                  >
                    <AlertCircle className="w-4 h-4 mr-1" />
                    恢复此选项
                  </Button>
                )}
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

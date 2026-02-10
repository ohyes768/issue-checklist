import { CheckItem } from '@/app/types/knowledge-base';
import { ChevronRight, ChevronDown, CheckCircle2, XCircle, Circle, MapPin } from 'lucide-react';
import { useState, useEffect, useMemo } from 'react';

interface ProgressTreeProps {
  rootIssue: CheckItem;
  currentPath: string[];
  issueStates: Map<string, 'pending' | 'confirmed' | 'excluded'>;
  onNavigate: (issueId: string) => void;
}

export function ProgressTree({ rootIssue, currentPath, issueStates, onNavigate }: ProgressTreeProps) {
  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="font-semibold">排查进度</h2>
        <p className="text-xs text-gray-500 mt-1">{rootIssue.title}</p>
      </div>
      <div className="flex-1 overflow-auto p-4">
        <TreeNode
          issue={rootIssue}
          level={0}
          currentPath={currentPath}
          issueStates={issueStates}
          onNavigate={onNavigate}
        />
      </div>
    </div>
  );
}

interface TreeNodeProps {
  issue: CheckItem;
  level: number;
  currentPath: string[];
  issueStates: Map<string, 'pending' | 'confirmed' | 'excluded'>;
  onNavigate: (issueId: string) => void;
}

function TreeNode({ issue, level, currentPath, issueStates, onNavigate }: TreeNodeProps) {
  const status = issueStates.get(issue.id) || 'pending';
  const isCurrent = currentPath[currentPath.length - 1] === issue.id;
  const isInPath = currentPath.includes(issue.id);

  // 检查是否有子项
  const hasChildren = issue.subCheckItems && issue.subCheckItems.length > 0;

  // 按优先级降序排序子项
  const sortedChildren = useMemo(() => {
    if (!issue.subCheckItems) return [];
    return [...issue.subCheckItems].sort((a, b) => b.priority - a.priority);
  }, [issue.subCheckItems]);
  
  // 检查子树中是否包含当前路径
  const containsCurrentPath = (item: CheckItem): boolean => {
    if (currentPath.includes(item.id)) return true;
    if (item.subCheckItems) {
      return item.subCheckItems.some(child => containsCurrentPath(child));
    }
    return false;
  };

  const hasCurrentPathInSubtree = hasChildren && sortedChildren.some(child => containsCurrentPath(child));
  
  // 默认收起，但如果子树包含当前路径则展开
  const [isExpanded, setIsExpanded] = useState(false);
  
  // 当路径变化且子树包含当前路径时，自动展开
  useEffect(() => {
    if (hasCurrentPathInSubtree || isInPath) {
      setIsExpanded(true);
    }
  }, [currentPath, hasCurrentPathInSubtree, isInPath]);

  const getStatusIcon = () => {
    // 如果节点在当前路径中，显示已确认状态（表示排查路径上的所有节点）
    if (isInPath) {
      return <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />;
    }

    switch (status) {
      case 'confirmed':
        return <CheckCircle2 className="w-4 h-4 text-green-600 flex-shrink-0" />;
      case 'excluded':
        return <XCircle className="w-4 h-4 text-gray-400 flex-shrink-0" />;
      default:
        return <Circle className="w-4 h-4 text-gray-300 flex-shrink-0" />;
    }
  };

  return (
    <div className="select-none">
      <div
        className={`flex items-center gap-2 py-1.5 px-2 rounded cursor-pointer hover:bg-gray-100 transition-colors ${
          isCurrent ? 'bg-blue-100 border border-blue-300' : isInPath ? 'bg-blue-50' : ''
        } ${status === 'excluded' ? 'opacity-50' : ''}`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
        onClick={() => onNavigate(issue.id)}
      >
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              setIsExpanded(!isExpanded);
            }}
            className="p-0.5 hover:bg-gray-200 rounded flex-shrink-0"
          >
            {isExpanded ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </button>
        ) : (
          <div className="w-5 flex-shrink-0" />
        )}
        
        {getStatusIcon()}
        
        <span className={`text-sm flex-1 ${isCurrent ? 'font-semibold text-blue-700' : isInPath ? 'font-medium text-blue-600' : ''}`}>
          {issue.title}
        </span>
        
        {isCurrent && (
          <MapPin className="w-4 h-4 text-blue-600 flex-shrink-0" title="当前位置" />
        )}
      </div>
      
      {hasChildren && isExpanded && (
        <div>
          {sortedChildren.map(child => (
            <TreeNode
              key={child.id}
              issue={child}
              level={level + 1}
              currentPath={currentPath}
              issueStates={issueStates}
              onNavigate={onNavigate}
            />
          ))}
        </div>
      )}
    </div>
  );
}
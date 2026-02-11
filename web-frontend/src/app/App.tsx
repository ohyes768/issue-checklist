import { useMemo } from 'react';
import { IssueSelector } from '@/app/components/IssueSelector';
import { ProgressTree } from '@/app/components/ProgressTree';
import { IssueDetail } from '@/app/components/IssueDetail';
import { CheckList } from '@/app/components/CheckList';
import { Button } from '@/app/components/ui/button';
import { Home, Loader2, AlertCircle } from 'lucide-react';
import { useAppState } from '@/app/hooks/useAppState';
import { Card } from '@/app/components/ui/card';

/**
 * 主应用组件
 * 使用 useAppState Hook 管理全局状态
 */
function App() {
  const {
    // 状态
    issues,
    selectedIssue,
    currentPath,
    issueStates,
    currentNode,
    isLoading,
    error,

    // 方法
    loadIssues,
    selectIssue,
    navigateTo,
    goBack,
    goHome,
    confirmItem,
    excludeItem,
  } = useAppState();

  // 当前节点的子项（用于 CheckList）
  const currentSubItems = useMemo(() => {
    return currentNode?.subCheckItems || [];
  }, [currentNode]);

  // 首页：问题选择器
  if (!selectedIssue || !currentNode) {
    return (
      <IssueSelector
        issues={issues}
        isLoading={isLoading}
        error={error}
        onLoadIssues={loadIssues}
        onSelectIssue={selectIssue}
      />
    );
  }

  // 全局错误状态
  if (error && !selectedIssue) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50 p-8 flex items-center justify-center">
        <Card className="max-w-md w-full p-8 text-center">
          <AlertCircle className="w-12 h-12 text-red-600 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">系统错误</h2>
          <p className="text-gray-600 mb-6">{error}</p>
          <Button onClick={goHome} variant="outline">
            返回首页
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* 顶部导航栏 */}
      <header className="bg-white border-b px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h1 className="text-xl font-bold text-gray-900">大数据平台运维知识库</h1>
          <span className="text-sm text-gray-500">排查模式</span>
          {isLoading && (
            <Loader2 className="w-4 h-4 text-blue-600 animate-spin" />
          )}
        </div>
        <Button onClick={goHome} variant="outline" size="sm">
          <Home className="w-4 h-4 mr-2" />
          返回首页
        </Button>
      </header>

      {/* 三栏布局 */}
      <div className="flex-1 flex overflow-hidden">
        {/* 左侧：进度树 (25%) */}
        <div className="w-1/4 border-r bg-white overflow-hidden">
          <ProgressTree
            rootIssue={selectedIssue}
            currentPath={currentPath}
            issueStates={issueStates}
            onNavigate={navigateTo}
          />
        </div>

        {/* 中间：问题详情 (40%) */}
        <div className="w-2/5 bg-white border-r overflow-hidden">
          {currentNode ? (
            <IssueDetail
              issue={currentNode}
              onBack={goBack}
              onHome={goHome}
              canGoBack={currentPath.length > 1}
              canGoHome={currentPath.length === 1}
            />
          ) : (
            <div className="h-full flex items-center justify-center">
              <p className="text-gray-500">请从左侧选择一个问题节点</p>
            </div>
          )}
        </div>

        {/* 右侧：检查单列表 (35%) */}
        <div className="w-[35%] bg-white overflow-hidden">
          <CheckList
            checkItems={currentSubItems}
            issueStates={issueStates}
            onConfirm={confirmItem}
            onExclude={excludeItem}
          />
        </div>
      </div>
    </div>
  );
}

export default App;

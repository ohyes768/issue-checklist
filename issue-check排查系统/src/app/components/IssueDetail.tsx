import { CheckItem } from '@/app/types/knowledge-base';
import { Badge } from '@/app/components/ui/badge';
import { Card } from '@/app/components/ui/card';
import { ExternalLink, Home } from 'lucide-react';
import { Button } from '@/app/components/ui/button';

interface IssueDetailProps {
  issue: CheckItem;
  onBack: () => void;
  onHome: () => void;
  canGoBack: boolean;
  canGoHome: boolean;
}

/**
 * 问题详情组件
 * 显示当前问题的详细信息和 HowToCheck
 */
export function IssueDetail({ issue, onBack, onHome, canGoBack, canGoHome }: IssueDetailProps) {
  /**
   * 智能格式化文本：将编号列表转换为行
   * 匹配模式：1. xxx 2. xxx 3. xxx 或 1、xxx 2、xxx 3、xxx
   */
  const formatNumberedList = (text: string): string => {
    // 匹配 "数字. " 或 "数字、" 前面没有换行的情况
    // 在这些编号前插入换行符
    return text.replace(/([^\n])\s+(\d+[\.\、]\s)/g, '$1\n$2');
  };

  // 收集所有相关知识库链接
  const allKnowledgeLinks = [
    ...issue.howToCheck.knowledgeLinks,
    ...(issue.fixSteps?.knowledgeLinks || [])
  ];

  const allGifGuides = [
    ...issue.howToCheck.gifGuides,
    ...(issue.fixSteps?.gifGuides || [])
  ];

  const allScriptLinks = [
    ...issue.howToCheck.scriptLinks,
    ...(issue.fixSteps?.scriptLinks || [])
  ];

  // 判断是否有任何相关链接
  const hasRelatedLinks =
    allKnowledgeLinks.length > 0 ||
    allGifGuides.length > 0 ||
    allScriptLinks.length > 0;

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

  /**
   * 渲染根因分析路径（从根本原因到表象问题）
   */
  const renderRootCausePath = () => {
    if (!issue.originalPath || issue.originalPath.length <= 1) return null;

    // 反转路径，从根本原因到表象问题
    const path = [...issue.originalPath].reverse();

    return (
      <section>
        <h3 className="text-lg font-semibold mb-3 text-orange-700">根因分析路径</h3>
        <Card className="p-4 bg-orange-50 border-orange-200">
          <div className="flex items-center gap-2 flex-wrap text-sm">
            {path.map((pathItem, index) => (
              <div key={index} className="flex items-center gap-2">
                <span className={index === 0 ? 'font-semibold text-orange-900' : 'text-gray-700'}>
                  {pathItem}
                </span>
                {index < path.length - 1 && (
                  <span className="text-orange-400">→</span>
                )}
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-600 mt-2">
            从左到右：根本原因 → ... → 表象问题
          </p>
        </Card>
      </section>
    );
  };

  return (
    <div className="h-full flex flex-col">
      {/* 标题栏 */}
      <div className="p-4 border-b flex items-center justify-between">
        <h2 className="font-semibold">问题详情</h2>
        {canGoBack && (
          <Button onClick={onBack} variant="outline" size="sm">
            返回上一级
          </Button>
        )}
        {canGoHome && (
          <Button onClick={onHome} variant="outline" size="sm">
            <Home className="w-4 h-4 mr-2" />
            返回首页
          </Button>
        )}
      </div>

      <div className="flex-1 overflow-auto p-6">
        {/* 问题标题 */}
        <div className="mb-6">
          <div className="flex items-center gap-3 mb-4 flex-wrap">
            <h1 className="text-2xl font-bold">{issue.title}</h1>
            <Badge className={getPriorityColor(issue.priority)}>
              优先级: {getPriorityLabel(issue.priority)} ({issue.priority})
            </Badge>
            <Badge variant="outline">{issue.version}</Badge>
            {issue.sourceFile && (
              <Badge variant="outline" className="text-xs">
                来源: {issue.sourceFile}
              </Badge>
            )}
          </div>
        </div>

        <div className="space-y-6">
          {/* HowToCheck 部分 */}
          <section>
            <h3 className="text-lg font-semibold mb-3">如何确认（How to Check）</h3>
            <Card className="p-4">
              <div className="text-gray-700 space-y-3">
                {formatNumberedList(issue.howToCheck.description).split('\n').map((line, index) => (
                  line.trim() && (
                    <p key={index} className="leading-relaxed">
                      {line}
                    </p>
                  )
                ))}
              </div>
            </Card>
          </section>

          {/* 根因分析路径 */}
          {renderRootCausePath()}

          {/* FixSteps 部分（如果有解决方案） */}
          {issue.fixSteps && (
            <>
              <div className="border-t pt-6">
                <section>
                  <h3 className="text-lg font-semibold mb-3 text-green-700">修复步骤（Fix Steps）</h3>
                  <Card className="p-4 bg-green-50 border-green-200">
                    <div className="text-gray-700 space-y-3">
                      {formatNumberedList(issue.fixSteps.description).split('\n').map((line, index) => (
                        line.trim() && (
                          <p key={index} className="leading-relaxed">
                            {line}
                          </p>
                        )
                      ))}
                    </div>
                  </Card>
                </section>
              </div>
            </>
          )}

          {/* 相关知识库（集中展示所有链接） */}
          {hasRelatedLinks && (
            <div className="border-t pt-6">
              <section>
                <h3 className="text-lg font-semibold mb-3 text-purple-700">相关知识库</h3>
                <Card className="p-4 bg-purple-50 border-purple-200">
                  <div className="space-y-4">
                    {/* 知识库链接 */}
                    {allKnowledgeLinks.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {allKnowledgeLinks.map((link, index) => (
                          <a
                            key={link.id}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1"
                          >
                            wiki{index + 1}
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        ))}
                      </div>
                    )}

                    {/* GIF 指引 */}
                    {allGifGuides.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {allGifGuides.map((guide, index) => (
                          <a
                            key={guide.id}
                            href={guide.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1"
                          >
                            gif{index + 1}
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        ))}
                      </div>
                    )}

                    {/* 脚本链接 */}
                    {allScriptLinks.length > 0 && (
                      <div className="flex flex-wrap gap-2">
                        {allScriptLinks.map((script, index) => (
                          <a
                            key={script.id}
                            href={script.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1"
                          >
                            脚本{index + 1}
                            <ExternalLink className="w-3 h-3" />
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                </Card>
              </section>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// 知识库数据类型定义

/**
 * 优先级类型：数字 1-10，数字越大越重要
 */
export type Priority = number; // 1-10

/**
 * 参考链接
 */
export interface Reference {
  id: string;
  title: string;
  url: string;
}

/**
 * HowToCheck 信息
 */
export interface HowToCheck {
  description: string;
  knowledgeLinks: Reference[];
  gifGuides: Reference[];
  scriptLinks: Reference[];
}

/**
 * 解决方案步骤
 */
export interface FixSteps {
  description: string;
  knowledgeLinks: Reference[];
  gifGuides: Reference[];
  scriptLinks: Reference[];
}

/**
 * 检查项（核心数据结构）
 */
export interface CheckItem {
  // 基本信息
  id: string;                    // 唯一标识（路径连接）
  title: string;                 // 现象描述（对应 status 字段）
  describe: string;              // 详细说明
  version: string;               // 影响版本
  priority: Priority;            // 优先级 1-10

  // HowToCheck 信息
  howToCheck: HowToCheck;

  // FixSteps（如果有解决方案）
  fixSteps?: FixSteps;

  // 来源和路径信息
  sourceFile: string;            // 来源 YAML 文件
  originalPath: string[];        // 完整路径

  // 引用相关
  isRefer: boolean;              // 是否为引用项
  parentRef?: string;            // 父级引用来源

  // 子项
  subCheckItems?: CheckItem[];
}

/**
 * 检查项状态
 */
export interface ItemState {
  id: string;
  status: 'pending' | 'confirmed' | 'excluded';
  confirmedAt?: Date;
}

/**
 * 应用状态
 */
export interface AppState {
  selectedIssue: CheckItem | null;
  currentPath: string[];
  issueStates: Map<string, ItemState>;
  excludedItems: Set<string>;
  confirmedItem: CheckItem | null;
  isLoading: boolean;
  error: string | null;
}

/**
 * 导航节点（用于面包屑）
 */
export interface NavigationNode {
  id: string;
  title: string;
  path: string[];
}

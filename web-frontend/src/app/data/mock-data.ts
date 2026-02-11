import { CheckItem } from '@/app/types/knowledge-base';

// 模拟的知识库数据
export const mockIssues: CheckItem[] = [
  {
    id: 'issue-1',
    title: '数据查询响应慢',
    howToCheck: {
      description: '观察用户查询请求的响应时间是否超过5秒。检查监控面板中的查询延迟指标。',
      knowledgeLinks: [
        { id: 'kb-1', title: '性能监控指南', url: '#' },
        { id: 'kb-2', title: '查询优化最佳实践', url: '#' }
      ],
      gifGuides: [
        { id: 'gif-1', title: '如何查看查询延迟', url: '#' }
      ],
      scriptLinks: [
        { id: 'script-1', title: 'query-performance-check.sh', url: '#' }
      ]
    },
    version: 'v3.0+',
    priority: 'high',
    subCheckItems: [
      {
        id: 'issue-1-1',
        title: 'SQL查询执行慢',
        howToCheck: {
          description: '检查执行计划，查看是否有全表扫描或缺失索引的情况。使用EXPLAIN命令分析查询。',
          knowledgeLinks: [
            { id: 'kb-3', title: 'SQL执行计划分析', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-2', title: 'explain-analyzer.sh', url: '#' }
          ]
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-1-1-1',
            title: '索引问题',
            howToCheck: {
              description: '分析查询涉及的表索引使用情况，检查是否存在索引缺失、索引失效或索引选择不当的问题。',
              knowledgeLinks: [
                { id: 'kb-4', title: '索引设计指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: [
                { id: 'script-3', title: 'index-analyzer.sh', url: '#' }
              ]
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-1-1-1-1',
                title: '缺失索引',
                howToCheck: {
                  description: '检查WHERE、JOIN、ORDER BY字段是否建立了合适的索引。查看执行计划中的Table Scan标识。',
                  knowledgeLinks: [
                    { id: 'kb-5', title: '索引缺失检测', url: '#' }
                  ],
                  gifGuides: [
                    { id: 'gif-2', title: '如何识别缺失索引', url: '#' }
                  ],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 分析查询语句中的过滤、连接和排序条件\n2. 在相关字段上创建单列或组合索引\n3. 考虑索引的选择性和基数\n4. 重新执行查询验证性能提升',
                  knowledgeLinks: [
                    { id: 'kb-6', title: '如何创建索引', url: '#' },
                    { id: 'kb-7', title: '索引设计最佳实践', url: '#' }
                  ],
                  gifGuides: [
                    { id: 'gif-3', title: '索引创建演示', url: '#' }
                  ],
                  scriptLinks: [
                    { id: 'script-4', title: 'create-index.sh', url: '#' }
                  ]
                }
              },
              {
                id: 'issue-1-1-1-2',
                title: '索引失效',
                howToCheck: {
                  description: '检查查询条件是否导致索引失效，如使用函数、隐式类型转换、LIKE左模糊等。',
                  knowledgeLinks: [
                    { id: 'kb-8', title: '索引失效场景', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 重写查询避免索引失效场景\n2. 使用函数索引或表达式索引\n3. 调整查询条件的数据类型匹配\n4. 考虑使用覆盖索引优化',
                  knowledgeLinks: [
                    { id: 'kb-9', title: '索引优化技巧', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-1-1-3',
                title: '索引选择不当',
                howToCheck: {
                  description: '检查优化器是否选择了最优索引，或者因为统计信息不准确导致选错索引。',
                  knowledgeLinks: [
                    { id: 'kb-10', title: '查询优化器原理', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'medium',
                fixSteps: {
                  description: '1. 使用FORCE INDEX强制指定索引\n2. 更新表统计信息\n3. 分析索引基数和选择性\n4. 考虑调整查询hint',
                  knowledgeLinks: [
                    { id: 'kb-11', title: '索引选择调优', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          },
          {
            id: 'issue-1-1-2',
            title: '统计信息过期',
            howToCheck: {
              description: '检查表的统计信息最后更新时间，是否超过7天未更新或数据变化超过20%。',
              knowledgeLinks: [
                { id: 'kb-12', title: '统计信息维护', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: [
                { id: 'script-5', title: 'check-statistics.sh', url: '#' }
              ]
            },
            version: 'v3.0+',
            priority: 'medium',
            fixSteps: {
              description: '1. 执行ANALYZE命令更新统计信息\n2. 设置自动统计信息收集任务\n3. 验证执行计划是否改善\n4. 对于大表考虑采样统计',
              knowledgeLinks: [
                { id: 'kb-13', title: '统计信息更新指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: [
                { id: 'script-6', title: 'update-statistics.sh', url: '#' }
              ]
            }
          },
          {
            id: 'issue-1-1-3',
            title: 'SQL语句编写问题',
            howToCheck: {
              description: '检查SQL语句存在性能问题，如子查询、多表JOIN、大数据量排序等。',
              knowledgeLinks: [
                { id: 'kb-14', title: 'SQL编写规范', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-1-1-3-1',
                title: '复杂子查询',
                howToCheck: {
                  description: '检查是否使用了多层嵌套子查询或关联子查询，导致重复执行。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 将子查询改写为JOIN\n2. 使用WITH子句（CTE）优化\n3. 考虑拆分为多个简单查询\n4. 使用临时表存储中间结果',
                  knowledgeLinks: [
                    { id: 'kb-15', title: '子查询优化', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-1-3-2',
                title: '过多表JOIN',
                howToCheck: {
                  description: '检查查询是否JOIN了过多表（超过5个），导致笛卡尔积或执行计划复杂。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'medium',
                fixSteps: {
                  description: '1. 优化JOIN顺序，小表驱动大表\n2. 增加WHERE过滤条件减少中间结果集\n3. 考虑数据预聚合或宽表设计\n4. 分步查询减少JOIN数量',
                  knowledgeLinks: [
                    { id: 'kb-16', title: 'JOIN优化技巧', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-1-3-3',
                title: '大数据量排序',
                howToCheck: {
                  description: '检查是否对大结果集进行ORDER BY或DISTINCT操作，导致磁盘排序。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'medium',
                fixSteps: {
                  description: '1. 在排序字段上建立索引利用索引排序\n2. 增加sort_buffer_size配置\n3. 先过滤再排序减少数据量\n4. 考虑应用层分页和排序',
                  knowledgeLinks: [
                    { id: 'kb-17', title: '排序优化', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          }
        ]
      },
      {
        id: 'issue-1-2',
        title: '网络延迟高',
        howToCheck: {
          description: '使用ping和traceroute检查客户端到服务器的网络延迟和路径，正常应小于10ms。',
          knowledgeLinks: [
            { id: 'kb-18', title: '网络诊断指南', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-7', title: 'network-check.sh', url: '#' }
          ]
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-1-2-1',
            title: '跨地域访问',
            howToCheck: {
              description: '检查客户端和服务器是否在不同地域或机房，存在跨地域网络传输。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 部署就近接入节点或CDN\n2. 使用专线连接提升带宽\n3. 启用数据压缩减少传输量\n4. 考虑多地域部署',
              knowledgeLinks: [
                { id: 'kb-19', title: '跨地域优化方案', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-1-2-2',
            title: '网络设备故障',
            howToCheck: {
              description: '检查交换机、路由器等网络设备存在丢包、延迟抖动等异常。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 检查网络设备日志和监控\n2. 排查端口故障或线路问题\n3. 重启或更换故障设备\n4. 优化网络拓扑结构',
              knowledgeLinks: [
                { id: 'kb-20', title: '网络设备运维手册', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-1-2-3',
            title: '带宽拥塞',
            howToCheck: {
              description: '检查网络带宽使用率是否接近上限，存在大量数据传输占用带宽。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'medium',
            fixSteps: {
              description: '1. 分析带宽占用来源\n2. 设置QoS优先级策略\n3. 扩容网络带宽\n4. 优化数据传输策略',
              knowledgeLinks: [
                { id: 'kb-21', title: '带宽管理指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-1-3',
        title: '服务器资源不足',
        howToCheck: {
          description: '检查CPU使用率、内存使用率、磁盘IO等指标是否接近100%。使用top、free、iostat等命令。',
          knowledgeLinks: [
            { id: 'kb-22', title: '资源监控指南', url: '#' }
          ],
          gifGuides: [
            { id: 'gif-4', title: '如何查看资源使用情况', url: '#' }
          ],
          scriptLinks: [
            { id: 'script-8', title: 'resource-check.sh', url: '#' }
          ]
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-1-3-1',
            title: 'CPU使用率过高',
            howToCheck: {
              description: '检查top命令输出，CPU使用率持续超过80%，系统负载load average过高。',
              knowledgeLinks: [
                { id: 'kb-23', title: 'CPU性能分析', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-1-3-1-1',
                title: '慢查询占用CPU',
                howToCheck: {
                  description: '检查是否有大量慢查询导致CPU使用率高，查看数据库慢查询日志。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 分析慢查询日志定位问题SQL\n2. 优化查询语句和索引\n3. 限制并发查询数量\n4. 启用查询缓存',
                  knowledgeLinks: [
                    { id: 'kb-24', title: '慢查询优化', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-3-1-2',
                title: '后台任务占用CPU',
                howToCheck: {
                  description: '检查是否有数据导入、备份、统计分析等后台任务在运行。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'medium',
                fixSteps: {
                  description: '1. 调整后台任务执行时间到业务低峰期\n2. 限制后台任务资源使用\n3. 优化任务执行逻辑\n4. 考虑分布式执行',
                  knowledgeLinks: [
                    { id: 'kb-25', title: '后台任务调优', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-3-1-3',
                title: 'GC频繁导致CPU高',
                howToCheck: {
                  description: '检查Java进程的GC日志，是否频繁进行Full GC或GC时间过长。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 调整JVM堆内存大小\n2. 优化GC参数和垃圾回收器\n3. 排查内存泄漏问题\n4. 减少大对象创建',
                  knowledgeLinks: [
                    { id: 'kb-26', title: 'JVM调优指南', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          },
          {
            id: 'issue-1-3-2',
            title: '内存不足',
            howToCheck: {
              description: '检查free命令输出，可用内存小于总内存的10%，存在大量swap使用。',
              knowledgeLinks: [
                { id: 'kb-27', title: '内存管理指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-1-3-2-1',
                title: '数据库缓存占用过多',
                howToCheck: {
                  description: '检查数据库buffer pool或cache配置是否过大，占用了大量内存。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 调整数据库缓存配置到合理值\n2. 监控缓存命中率\n3. 考虑使用外部缓存（Redis）\n4. 清理无用的缓存数据',
                  knowledgeLinks: [
                    { id: 'kb-28', title: '数据库缓存优化', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-3-2-2',
                title: '应用程序内存泄漏',
                howToCheck: {
                  description: '检查应用程序内存使用是否持续增长不释放，使用内存分析工具排查。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 使用jmap、MAT等工具分析堆转储\n2. 定位内存泄漏代码位置\n3. 修复代码释放资源\n4. 重启应用程序',
                  knowledgeLinks: [
                    { id: 'kb-29', title: '内存泄漏排查', url: '#' }
                  ],
                  gifGuides: [
                    { id: 'gif-5', title: '内存分析工具使用', url: '#' }
                  ],
                  scriptLinks: []
                }
              }
            ]
          },
          {
            id: 'issue-1-3-3',
            title: '磁盘IO瓶颈',
            howToCheck: {
              description: '检查iostat输出，磁盘使用率util%接近100%，await时间过长。',
              knowledgeLinks: [
                { id: 'kb-30', title: '磁盘IO分析', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-1-3-3-1',
                title: '大量随机读写',
                howToCheck: {
                  description: '检查存在大量小文件随机读写操作，IOPS达到磁盘上限。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 调整数据库页大小和缓冲区\n2. 使用SSD替换机械硬盘\n3. 优化数据访问模式减少随机IO\n4. 增加内存减少磁盘访问',
                  knowledgeLinks: [
                    { id: 'kb-31', title: '磁盘IO优化', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-1-3-3-2',
                title: '日志写入过多',
                howToCheck: {
                  description: '检查数据库日志、应用日志写入量是否过大，占用大量IO。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'medium',
                fixSteps: {
                  description: '1. 调整日志级别减少日志量\n2. 使用异步日志写入\n3. 日志文件放到独立磁盘\n4. 定期清理旧日志文件',
                  knowledgeLinks: [
                    { id: 'kb-32', title: '日志管理最佳实践', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          }
        ]
      },
      {
        id: 'issue-1-4',
        title: '数据库连接池问题',
        howToCheck: {
          description: '检查数据库连接池配置和使用情况，存在连接耗尽或连接泄漏。',
          knowledgeLinks: [
            { id: 'kb-33', title: '连接池原理', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-9', title: 'connection-pool-check.sh', url: '#' }
          ]
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-1-4-1',
            title: '连接池耗尽',
            howToCheck: {
              description: '检查连接池活跃连接数是否达到最大值，新请求无法获取连接。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 增加连接池最大连接数\n2. 优化慢查询减少连接占用时间\n3. 设置合理的连接超时时间\n4. 检查并修复连接泄漏',
              knowledgeLinks: [
                { id: 'kb-34', title: '连接池调优', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-1-4-2',
            title: '连接泄漏',
            howToCheck: {
              description: '检查应用代码是否正确关闭数据库连接，导致连接无法释放。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 审查代码确保使用try-finally或try-with-resources\n2. 启用连接泄漏检测\n3. 修复未关闭连接的代码\n4. 重启应用释放泄漏连接',
              knowledgeLinks: [
                { id: 'kb-35', title: '连接泄漏排查', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      }
    ]
  },
  {
    id: 'issue-2',
    title: '数据同步失败',
    howToCheck: {
      description: '检查同步任务日志，查看是否有错误信息或同步进度停滞。监控同步延迟和数据一致性。',
      knowledgeLinks: [
        { id: 'kb-36', title: '数据同步架构', url: '#' }
      ],
      gifGuides: [
        { id: 'gif-6', title: '查看同步任务状态', url: '#' }
      ],
      scriptLinks: [
        { id: 'script-10', title: 'sync-status-check.sh', url: '#' }
      ]
    },
    version: 'v2.5+',
    priority: 'high',
    subCheckItems: [
      {
        id: 'issue-2-1',
        title: '源端连接问题',
        howToCheck: {
          description: '尝试从目标端连接源端数据库，检查网络连通性和认证是否正常。',
          knowledgeLinks: [
            { id: 'kb-37', title: '数据源连接配置', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-11', title: 'test-connection.sh', url: '#' }
          ]
        },
        version: 'v2.5+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-2-1-1',
            title: '网络不通',
            howToCheck: {
              description: '使用telnet或nc测试源端数据库端口是否可达。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 检查防火墙规则是否开放端口\n2. 验证安全组配置\n3. 检查网络路由是否正确\n4. 确认源端数据库服务正在运行',
              knowledgeLinks: [
                { id: 'kb-38', title: '网络连通性排查', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-2-1-2',
            title: '认证失败',
            howToCheck: {
              description: '检查数据库用户名、密码是否正确，用户是否有足够权限。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-2-1-2-1',
                title: '密码错误或过期',
                howToCheck: {
                  description: '验证配置的密码是否正确，检查数据库账号是否过期或被锁定。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v2.5+',
                priority: 'high',
                fixSteps: {
                  description: '1. 重置数据库账号密码\n2. 更新同步配置中的密码\n3. 解锁被锁定的账号\n4. 设置密码永不过期策略',
                  knowledgeLinks: [
                    { id: 'kb-39', title: '数据库账号管理', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-2-1-2-2',
                title: '权限不足',
                howToCheck: {
                  description: '检查同步账号是否有SELECT、REPLICATION权限。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v2.5+',
                priority: 'high',
                fixSteps: {
                  description: '1. 为同步账号授予必要权限\n2. 验证权限生效\n3. 检查是否需要SUPER权限\n4. 重新测试连接',
                  knowledgeLinks: [
                    { id: 'kb-40', title: '同步账号权限配置', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          },
          {
            id: 'issue-2-1-3',
            title: '连接数限制',
            howToCheck: {
              description: '检查源端数据库连接数是否达到上限，无法创建新连接。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'medium',
            fixSteps: {
              description: '1. 增加数据库最大连接数配置\n2. 优化连接池配置\n3. 关闭不必要的连接\n4. 检查是否存在连接泄漏',
              knowledgeLinks: [
                { id: 'kb-41', title: '数据库连接数管理', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-2-2',
        title: '数据格式不兼容',
        howToCheck: {
          description: '检查源端和目标端的表结构、数据类型、字符集是否一致或兼容。',
          knowledgeLinks: [
            { id: 'kb-42', title: '数据类型映射表', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-12', title: 'schema-compare.sh', url: '#' }
          ]
        },
        version: 'v2.5+',
        priority: 'medium',
        subCheckItems: [
          {
            id: 'issue-2-2-1',
            title: '字段类型不匹配',
            howToCheck: {
              description: '对比源端和目标端相同字段的数据类型，检查存在不兼容。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 修改目标端字段类型匹配源端\n2. 配置数据类型转换规则\n3. 处理可能的数据截断或溢出\n4. 重新启动同步任务',
              knowledgeLinks: [
                { id: 'kb-43', title: '数据类型转换配置', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-2-2-2',
            title: '字符集编码问题',
            howToCheck: {
              description: '检查源端和目标端的字符集配置，存在中文乱码或特殊字符丢失。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'medium',
            fixSteps: {
              description: '1. 统一源端和目标端字符集为UTF8\n2. 配置字符集转换\n3. 处理已同步的乱码数据\n4. 验证数据正确性',
              knowledgeLinks: [
                { id: 'kb-44', title: '字符集配置指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-2-3',
        title: '同步任务配置错误',
        howToCheck: {
          description: '检查同步任务的配置文件，包括表映射、过滤条件、同步模式等设置。',
          knowledgeLinks: [
            { id: 'kb-45', title: '同步任务配置说明', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v2.5+',
        priority: 'medium',
        subCheckItems: [
          {
            id: 'issue-2-3-1',
            title: '表映射配置错误',
            howToCheck: {
              description: '检查源表和目标表的映射关系是否正确，表名、库名是否匹配。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 核对表映射配置\n2. 修正错误的表名或库名\n3. 验证映射关系\n4. 重启同步任务',
              knowledgeLinks: [
                { id: 'kb-46', title: '表映射配置示例', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-2-3-2',
            title: '过滤条件配置错误',
            howToCheck: {
              description: '检查WHERE过滤条件是否正确，是否导致数据被错误过滤。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'medium',
            fixSteps: {
              description: '1. ���查过滤条件逻辑\n2. 调整过滤规则\n3. 清理错误数据重新同步\n4. 验证同步结果',
              knowledgeLinks: [
                { id: 'kb-47', title: '过滤条件配置', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-2-4',
        title: '数据冲突',
        howToCheck: {
          description: '检查同步过程中存在主键冲突、唯一索引冲突等数据冲突问题。',
          knowledgeLinks: [
            { id: 'kb-48', title: '数据冲突处理策略', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v2.5+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-2-4-1',
            title: '主键冲突',
            howToCheck: {
              description: '检查同步日志中存在Duplicate key错误，主键重复导致插入失败。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 配置冲突处理策略（覆盖/忽略/报错）\n2. 清理目标端重复数据\n3. 检查主键生成策略是否正确\n4. 重新同步数据',
              knowledgeLinks: [
                { id: 'kb-49', title: '主键冲突解决方案', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-2-4-2',
            title: '外键约束冲突',
            howToCheck: {
              description: '检查存在外键约束导致数据无法插入或删除。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v2.5+',
            priority: 'medium',
            fixSteps: {
              description: '1. 临时禁用外键约束\n2. 调整同步顺序先同步父表\n3. 修复引用关系\n4. 重新启用外键约束',
              knowledgeLinks: [
                { id: 'kb-50', title: '外键约束处理', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      }
    ]
  },
  {
    id: 'issue-3',
    title: '任务调度异常',
    howToCheck: {
      description: '检查调度系统状态，查看任务是否按预期时间执行，存在任务堆积或失败。',
      knowledgeLinks: [
        { id: 'kb-51', title: '调度系统架构', url: '#' }
      ],
      gifGuides: [],
      scriptLinks: [
        { id: 'script-13', title: 'scheduler-check.sh', url: '#' }
      ]
    },
    version: 'v3.0+',
    priority: 'medium',
    subCheckItems: [
      {
        id: 'issue-3-1',
        title: '调度器服务问题',
        howToCheck: {
          description: '检查调度器进程状态、端口监听、服务健康检查等。',
          knowledgeLinks: [
            { id: 'kb-52', title: '调度器运维手册', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-3-1-1',
            title: '调度器服务未启动',
            howToCheck: {
              description: '使用ps命令检查调度器进程存在，端口是否监听。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 启动调度器服务\n2. 检查启动日志确认无错误\n3. 验证端口正常监听\n4. 测试任务能否正常调度',
              knowledgeLinks: [
                { id: 'kb-53', title: '调度器启动指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: [
                { id: 'script-14', title: 'start-scheduler.sh', url: '#' }
              ]
            }
          },
          {
            id: 'issue-3-1-2',
            title: '调度器服务宕机',
            howToCheck: {
              description: '检查调度器进程异常退出，查看系统日志和应用日志。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-3-1-2-1',
                title: 'OOM导致进程被杀',
                howToCheck: {
                  description: '检查系统日志存在Out of Memory Killer记录。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 增加JVM堆内存配置\n2. 分析内存使用情况\n3. 优化调度器内存占用\n4. 重启服务并监控',
                  knowledgeLinks: [
                    { id: 'kb-54', title: 'OOM问题排查', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              },
              {
                id: 'issue-3-1-2-2',
                title: '未捕获异常导致崩溃',
                howToCheck: {
                  description: '查看调度器日志存在未处理异常堆栈信息。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.0+',
                priority: 'high',
                fixSteps: {
                  description: '1. 分析异常堆栈定位问题代码\n2. 修复Bug或增加异常处理\n3. 升级到修复版本\n4. 重启服务',
                  knowledgeLinks: [
                    { id: 'kb-55', title: '异常排查流程', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          }
        ]
      },
      {
        id: 'issue-3-2',
        title: '任务配置问题',
        howToCheck: {
          description: '检查任务定义、cron表达式、依赖关系、参数配置等是否正确。',
          knowledgeLinks: [
            { id: 'kb-56', title: '任务配置说明', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.0+',
        priority: 'medium',
        subCheckItems: [
          {
            id: 'issue-3-2-1',
            title: 'Cron表达式错误',
            howToCheck: {
              description: '验证cron表达式格式正确，能正确解析触发时间。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 使用在线工具验证cron表达式\n2. 修正错误的表达式\n3. 重新加载任务配置\n4. 验证下次触发时间',
              knowledgeLinks: [
                { id: 'kb-57', title: 'Cron表达式语法', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-3-2-2',
            title: '任务依赖配置错误',
            howToCheck: {
              description: '检查任务依赖关系正确，存在循环依赖或依赖的任务不存在。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'medium',
            fixSteps: {
              description: '1. 梳理任务依赖关系\n2. 修正依赖配置\n3. 解除循环依赖\n4. 重新提交任务',
              knowledgeLinks: [
                { id: 'kb-58', title: '任务依赖管理', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-3-2-3',
            title: '任务参数错误',
            howToCheck: {
              description: '检查任务参数配置正确，参数值格式、类型匹配。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'low',
            fixSteps: {
              description: '1. 验证参数格式和取值范围\n2. 修正错误参数\n3. 更新任务配置\n4. 手动触发测试',
              knowledgeLinks: [
                { id: 'kb-59', title: '任务参数配置', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-3-3',
        title: '任务执行失败',
        howToCheck: {
          description: '检查任务执行日志，查看失败原因和错误信息。',
          knowledgeLinks: [
            { id: 'kb-60', title: '任务日志分析', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-3-3-1',
            title: '任务超时',
            howToCheck: {
              description: '检查任务执行时间超过超时限制，任务被强制终止。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 增加任务超时时间配置\n2. 优化任务执行逻辑\n3. 分拆大任务为多个子任务\n4. 重新执行任务',
              knowledgeLinks: [
                { id: 'kb-61', title: '任务超时处理', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-3-3-2',
            title: '执行脚本错误',
            howToCheck: {
              description: '检查任务执行的脚本存在语法错误或运行时错误。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 修复脚本中的错误\n2. 本地测试脚本执行\n3. 更新任务脚本\n4. 重新运行任务',
              knowledgeLinks: [
                { id: 'kb-62', title: '脚本调试指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-3-3-3',
            title: '资源不足导致失败',
            howToCheck: {
              description: '检查任务执行时系统资源使用情况，存在资源不足导致失败。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'medium',
            fixSteps: {
              description: '1. 分配更多资源给任务\n2. 调整任务执行时间避开高峰\n3. 优化任务资源使用\n4. 考虑资源隔离或限流',
              knowledgeLinks: [
                { id: 'kb-63', title: '任务资源管理', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      },
      {
        id: 'issue-3-4',
        title: '任务队列堆积',
        howToCheck: {
          description: '检查调度队列存在大量任务等待执行，任务处理速度跟不上提交速度。',
          knowledgeLinks: [
            { id: 'kb-64', title: '队列监控指南', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.0+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-3-4-1',
            title: '执行器资源不足',
            howToCheck: {
              description: '检查执行器数量和并发度配置，无法满足任务执行需求。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 增加执行器实例数量\n2. 提高单个执行器并发度\n3. 优化任务执行效率\n4. 清理不必要的任务',
              knowledgeLinks: [
                { id: 'kb-65', title: '执行器扩容指南', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-3-4-2',
            title: '长时间任务阻塞',
            howToCheck: {
              description: '检查存在少数任务执行时间过长，阻塞其他任务执行。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.0+',
            priority: 'high',
            fixSteps: {
              description: '1. 识别并优化长时间任务\n2. 设置任务优先级和分组\n3. 使用独立队列隔离长任务\n4. 考虑任务分片并行执行',
              knowledgeLinks: [
                { id: 'kb-66', title: '任务性能优化', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      }
    ]
  },
  {
    id: 'issue-4',
    title: '集群节点异常',
    howToCheck: {
      description: '检查集群各节点健康状态，存在节点宕机、网络分区或数据不一致。',
      knowledgeLinks: [
        { id: 'kb-67', title: '集群架构说明', url: '#' }
      ],
      gifGuides: [
        { id: 'gif-7', title: '集群监控面板', url: '#' }
      ],
      scriptLinks: [
        { id: 'script-15', title: 'cluster-health-check.sh', url: '#' }
      ]
    },
    version: 'v3.5+',
    priority: 'high',
    subCheckItems: [
      {
        id: 'issue-4-1',
        title: '节点宕机',
        howToCheck: {
          description: '检查集群监控系统，存在节点状态Down或Unreachable。',
          knowledgeLinks: [
            { id: 'kb-68', title: '节点状态说明', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.5+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-4-1-1',
            title: '硬件故障',
            howToCheck: {
              description: '检查服务器硬件状态，包括CPU、内存、磁盘、电源等存在故障指示。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 联系硬件供应商维修或更换\n2. 从集群中移除故障节点\n3. 添加新节点到集群\n4. 触发数据再平衡',
              knowledgeLinks: [
                { id: 'kb-69', title: '节点替换流程', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-4-1-2',
            title: '进程崩溃',
            howToCheck: {
              description: '检查节点关键进程正常运行，查看进程崩溃日志。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.5+',
            priority: 'high',
            subCheckItems: [
              {
                id: 'issue-4-1-2-1',
                title: '核心转储分析',
                howToCheck: {
                  description: '检查生成core dump文件，分析崩溃原因。',
                  knowledgeLinks: [],
                  gifGuides: [],
                  scriptLinks: []
                },
                version: 'v3.5+',
                priority: 'high',
                fixSteps: {
                  description: '1. 使用gdb等工具分析core dump\n2. 定位崩溃代码位置\n3. 修复Bug或升级到稳定版本\n4. 重启进程并监控',
                  knowledgeLinks: [
                    { id: 'kb-70', title: 'Core Dump分析', url: '#' }
                  ],
                  gifGuides: [],
                  scriptLinks: []
                }
              }
            ]
          }
        ]
      },
      {
        id: 'issue-4-2',
        title: '网络分区',
        howToCheck: {
          description: '检查集群节点之间网络连通性，存在部分节点无法互相通信情况。',
          knowledgeLinks: [
            { id: 'kb-71', title: '网络分区检测', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        },
        version: 'v3.5+',
        priority: 'high',
        fixSteps: {
          description: '1. 排查网络故障恢复连通性\n2. 处理脑裂问题选择主分区\n3. 重新加入被隔离的节点\n4. 同步数据保证一致性',
          knowledgeLinks: [
            { id: 'kb-72', title: '网络分区处理', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: []
        }
      },
      {
        id: 'issue-4-3',
        title: '数据副本不一致',
        howToCheck: {
          description: '检查数据各副本之间是否一致，存在副本数据损坏或丢失。',
          knowledgeLinks: [
            { id: 'kb-73', title: '数据一致性检查', url: '#' }
          ],
          gifGuides: [],
          scriptLinks: [
            { id: 'script-16', title: 'data-consistency-check.sh', url: '#' }
          ]
        },
        version: 'v3.5+',
        priority: 'high',
        subCheckItems: [
          {
            id: 'issue-4-3-1',
            title: '副本同步延迟',
            howToCheck: {
              description: '检查主副本和从副本之间同步延迟，存在超过阈值。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.5+',
            priority: 'medium',
            fixSteps: {
              description: '1. 检查从副本复制线程状态\n2. 优化网络带宽和延迟\n3. 调整复制并发度\n4. 考虑重建严重落后的副本',
              knowledgeLinks: [
                { id: 'kb-74', title: '副本同步优化', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          },
          {
            id: 'issue-4-3-2',
            title: '数据损坏',
            howToCheck: {
              description: '检查数据文件校验和，存在数据块损坏或读取错误。',
              knowledgeLinks: [],
              gifGuides: [],
              scriptLinks: []
            },
            version: 'v3.5+',
            priority: 'high',
            fixSteps: {
              description: '1. 标记损坏数据块\n2. 从健康副本恢复数据\n3. 修复文件系统错误\n4. 验证数据完整性',
              knowledgeLinks: [
                { id: 'kb-75', title: '数据修复流程', url: '#' }
              ],
              gifGuides: [],
              scriptLinks: []
            }
          }
        ]
      }
    ]
  }
];
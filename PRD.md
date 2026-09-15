# LabelMaker MVP 产品需求规格

## 1. 目标与边界

LabelMaker 是一个 Windows 本地离线的 YOLO 检测数据集标签治理工具。它的目标是减少因客户缺陷标准变化带来的检索、批量改类、人工复核、回退和训练集导出成本。

第一版只支持 YOLO 目标检测矩形框（`class x_center y_center width height`），不负责模型训练，也不支持分割、多边形、关键点、多人协作或云端同步。

## 2. 核心术语

| 术语 | 定义 |
| --- | --- |
| 项目 | 一个可携带的数据集根目录；元数据保存于 `.labelmaker/`。 |
| 图片资产 | 原始图片及其稳定 `sample_id`；不因标签标准变化复制。 |
| 图片集合版本 | 哪些样本参与数据集、训练划分及排除原因的不可变快照，例如 `R2`。 |
| 标签标准 | 类别、YOLO class ID、判定规则、示例、框选规范及变更说明，例如 `S3`。 |
| 标签修订 | 某一标签标准下实际框标注与审核状态的不可变版本。 |
| 训练发布包 | 指定“图片集合版本 + 标签标准/修订 + 审核条件”生成的标准 YOLO 目录。 |

## 3. 项目目录

```text
dataset-root/
├─ images/                     # 原始图像，保持用户现有目录结构
├─ labels/                     # 导入时的原始 YOLO 标签，可保留只读
├─ data.yaml                   # 导入数据集的类别真源
└─ .labelmaker/
   ├─ project.db               # SQLite 元数据、审计与版本图
   ├─ label-revisions/         # 各标签修订的标签文件
   ├─ exports/                 # 可删除的 YOLO 训练发布包
   └─ cleanup/                 # 待物理清理项目的清单
```

项目使用相对路径，随整个目录可移动或备份。导出的 `images/` 优先使用硬链接，无法链接时由用户选择复制。

## 4. 必须实现的流程

### 4.1 导入与校验

1. 选择 YOLO 数据集根目录。
2. 读取 `data.yaml` 或 `classes.txt`，展示类别及其 ID；内置默认标签只能作为新项目模板，不能重排导入类别 ID。
3. 校验图片/标签匹配、重复样本名、类别 ID 越界、坐标非法、图片不可读与缺失划分。
4. 正常样本导入项目，异常样本进入修复队列；禁止静默跳过。
5. 保存原始图片集合版本 `R1`、初始标签标准 `S1` 与标签修订。

### 4.2 检索、标注与质检

图片级检索必须支持类别：任一（OR）、同时全部（AND）、仅有（EXACT）、不含、目标数量范围和无标注图片；还可叠加集合版本、训练划分、审核状态与 CSV 导入的自定义元数据。

单图编辑支持创建、移动、缩放、删除框和变更框类别。批量操作仅允许修改命中框的类别、删除指定类别框及修改审核状态，不允许批量移动框。

审核状态绑定到“样本 + 标签标准/修订”：

```text
未标注 → 待复核 → 已通过
             ├→ 需返工 → 待复核
             └→ 已排除
```

### 4.3 标准迁移与回退

任何批量修改均先生成影响范围、样本数、类别 ID 映射和冲突的预览，用户确认后才创建新的标签修订；历史版本不可覆盖。

- 改名、类别合并、保留框的 ID 映射属于结构性迁移，可在预览确认后自动执行。
- 尺寸阈值、严重度、边界画法、漏标规则等属于语义/几何迁移，只能生成待复核候选集，不能自动宣称完成清理。
- 每个标准应记录类别名、ID、文字定义、正反例、框选规则、变更说明和生效时间。

### 4.4 图片增删与清理

新增图片创建新的图片集合版本，初始状态为未标注。删除快捷键仅把当前图片从新的集合版本排除并写入待清理清单，支持撤销。

物理删除必须在项目收尾页从清单中勾选并二次确认；仍被任一历史集合版本引用的图片或标签不能清理。

### 4.5 导出

用户选择图片集合版本、标签修订、训练/验证/测试划分以及审核门槛（默认仅“已通过”），生成包含 `images/`、`labels/`、`data.yaml`、样本清单和校验报告的标准 YOLO 训练发布包。

## 5. 页面结构

1. **项目主页**：版本摘要、导入校验、最近导出、待复核/待清理数量。
2. **数据浏览与搜索**：筛选器、缩略图列表、元数据和批量操作入口。
3. **标注复核工作台**：图片画布、类别列表、框属性、审核状态、版本信息。
4. **标准与迁移**：标准定义卡、比较视图、迁移预览、候选复核队列。
5. **版本与导出**：集合/标签版本树、变更记录、回退、YOLO 导出。
6. **设置**：默认标签模板、CSV 字段映射、快捷键。

## 6. 快捷键

所有快捷键可单独设置、检查冲突并恢复默认值；本机保存而不写入数据集版本。第一版必须提供：上一张、下一张、开始标注、上一个标签、下一个标签、删除当前图片（排除）、保存并下一张、撤销。

## 7. 最小数据模型

| 实体 | 关键字段 |
| --- | --- |
| `projects` | id、root_path、created_at |
| `samples` | id、relative_image_path、width、height、content_hash |
| `collection_revisions` | id、parent_id、name、created_at、reason |
| `collection_memberships` | revision_id、sample_id、split、excluded_reason |
| `label_standards` | id、name、parent_id、description、effective_at |
| `classes` | standard_id、class_id、name、definition、drawing_rule |
| `label_revisions` | id、standard_id、collection_revision_id、parent_id、created_at |
| `annotations` | label_revision_id、sample_id、class_id、x_center、y_center、width、height |
| `review_states` | label_revision_id、sample_id、state、reviewer、updated_at |
| `operations` | id、kind、input_revision、output_revision、parameters、operator、created_at |
| `cleanup_candidates` | sample_id、reason、created_at、physical_delete_at |

## 8. 验收场景

给定已有 YOLO 数据集，用户能导入并处理校验异常；检索含 A 或 B 的图片；预览并将 A/B 合并到 C，生成新标准版本；完成受影响图片的人工复核；排除坏图并查看待清理清单；导出仅含已通过样本的 YOLO 训练包；并从任一迁移结果回退、复现旧版本。

## 9. 非目标

- 内置训练、调参、指标分析或模型仓库。
- 分割、关键点、分类等非检测标签。
- 多人并发编辑、在线账户、远程同步、权限系统。
- 未经用户确认的批量覆盖、自动删除或静默数据修复。

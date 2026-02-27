import sqlite3
import datetime
import random

DB_PATH = 'backend/blog.db'

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data for a fresh start
    cursor.execute('DELETE FROM posts')
    cursor.execute('DELETE FROM tasks')
    cursor.execute('DELETE FROM notes')

    now = datetime.datetime.now()

    # Seed Posts (Rich Markdown Data)
    posts = [
        (
            '给未来的自己一封信',
            '黄昏于万物之间，临于天地之时。记录下这段时间的心路历程与技术思考。',
            '''# 序言
在时间的洪流中，我们总是走得太急，往往忽略了沿途的风景。这不仅是一场技术的探索，更是一次心灵的回归。

## 技术的更迭
去年我开始将核心架构从传统的单体架构迁移到基于微服务的设计中。这个过程中遇到过无数的坑...

- 数据库一致性问题
- 分布式追踪链路的搭建
- 团队对新栈的适应期

但这都是值得的，系统变得更有弹性。

> “Stay hungry, stay foolish.”

![代码缩影](https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&q=80)

## 设计美学
关于博客 V2的设计，我试图将真实的物理世界材质（如磨砂玻璃）与极简排版结合起来。我想要一种呼吸感。
日落云海不仅仅是一个背景，它代表了某种「空、境」的哲学概念。
            ''',
            '随笔',
            'Deep',
            'https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=2)).isoformat(),
            345, 12
        ),
        (
            '春日漫步：代官山摄影集',
            '周末带着富士相机去代官山走街串巷，记录下这座城市安静的一面。',
            '全系列采用富士经典负片滤镜直出，无需多言，感受城市的脉搏吧。',
            '摄影',
            'Calm',
            'https://images.unsplash.com/photo-1517427677506-ade074eb1432?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=5)).isoformat(),
            892, 45
        ),
        (
            '街角咖啡店：午后的光影',
            '在这个充斥着拿铁香气的午后，几本书和一杯咖啡成了最好的陪伴者。',
            '静静地看着窗外人来人往...',
            '摄影',
            'Inspired',
            'https://images.unsplash.com/photo-1497935586351-b67a49e012bf?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=12)).isoformat(),
            512, 23
        ),
        (
            '如何优雅地使用 Vue 3 Composition API',
            '本文总结了过去一年在实际业务中深入使用 Composition API 沉淀的一些最佳实践。',
            '''# Composition API 最佳实践

在 Vue 3 中，提供了一种全新的组织代码的方式。最大的好处是可以将逻辑按功能点提取为 hooks。

## `ref` vs `reactive`
日常开发中，建议简单基本类型使用 `ref`，对于高度内聚的表单数据对象使用 `reactive`。

```javascript
import { ref, reactive } from 'vue'

const count = ref(0)
const userForm = reactive({
  username: '',
  password: ''
})
```
            ''',
            '项目',
            'Tech',
            'https://images.unsplash.com/photo-1550439062-609e1531270e?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=20)).isoformat(),
            1205, 88
        ),
        (
            '深入理解玻璃态UI设计（Glassmorphism）',
            '探讨如何用现代 CSS 技巧打造极其通透且不影响阅读体验的毛玻璃视觉风格。',
            '主要用到了 `backdrop-filter: blur(x)` 技术。',
            '项目',
            'Tech',
            'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=25)).isoformat(),
            670, 42
        ),
        (
            '雨夜归途',
            '霓虹灯倒映在积水的马路上，这个城市的夜晚总是带着几分赛博朋克的迷离。',
            '下雨天最适合听着爵士乐开车，不过还是要慢点开。',
            '摄影',
            'Melancholy',
            'https://images.unsplash.com/photo-1515895309288-a3815ab7cf81?auto=format&fit=crop&w=800&q=80',
            (now - datetime.timedelta(days=3)).isoformat(),
            908, 67
        )
    ]

    cursor.executemany('''
        INSERT INTO posts (title, summary, content, category, mood, cover_image, date, views, likes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', posts)

    # Seed Tasks
    tasks = [
        ('整理 V2 博客的设计思路文档', '其他', '普通', 0),
        ('修复关于页面中的图表动画渲染卡顿问题', '重要', '高', 0),
        ('给小猫喂罐头并清理猫砂', '生活', '普通', 1),
        ('阅读《设计心理学》第 3 章', '其他', '普通', 0)
    ]
    cursor.executemany('''
        INSERT INTO tasks (title, tag, priority, done)
        VALUES (?, ?, ?, ?)
    ''', tasks)

    # Seed Notes
    notes = [
        ('刚才散步时想到：极简并不是一无所有，而是把最重要的东西凸显出来。这也许就是 UI 设计中的“留白”艺术。', now.isoformat()),
        ('看到一篇有趣的论文提到了用 WebGL 渲染玻璃光谱，不知道能不能应用到博客的新背景板上，周末可以研究一下。', (now - datetime.timedelta(hours=2)).isoformat()),
        ('“黄昏于万物之间，临于天地之时。”—— 每次读这句话都觉得充满力量。', (now - datetime.timedelta(days=1)).isoformat())
    ]
    cursor.executemany('''
        INSERT INTO notes (content, created_at)
        VALUES (?, ?)
    ''', notes)

    conn.commit()
    conn.close()
    print("Database seeded completely with rich mock data.")

if __name__ == '__main__':
    seed_database()

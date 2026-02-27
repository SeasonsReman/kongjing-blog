import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "blog.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            mood TEXT NOT NULL,
            cover_image TEXT,
            date TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            tag TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT '普通',
            done INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)

    # Seed posts if empty
    cur.execute("SELECT COUNT(*) FROM posts")
    if cur.fetchone()[0] == 0:
        posts = [
            ("留白的艺术：少即是多的数字空间",
             "在信息过载的时代，我们如何在数字界面中寻找呼吸感？探讨极简主义不仅仅是一种视觉风格，更是一种思维方式。",
             "全文内容……极简主义的核心在于聚焦。每一个空白都是一次有意识的放弃。",
             "设计哲学", "Calm", None, "2024-10-24", 1200, 48),
            ("构建高性能的前端动画引擎",
             "深入解析 requestAnimationFrame 与 CSS 变换的协同工作原理，打造丝滑的交互体验。",
             "全文内容……GPU 加速的关键是 will-change 属性和 transform 的正确使用。",
             "技术笔记", "Tech", None, "2024-09-15", 856, 124),
            ("雨天的咖啡馆与一本旧书",
             "那个午后，窗外的雨声成了最好的背景音，书页翻动的声音，是时间流逝最温柔的注脚。",
             "全文内容……有些下午适合什么都不做，只是存在着。",
             "生活随笔", "Calm", None, "2024-08-30", 532, 67),
            ("秋日私语：关于独处的思考",
             "在落叶纷飞的午后，重新审视孤独的价值。不是逃避，而是回归内心的宁静之所。",
             "全文内容……真正的独处不是孤独，是与自己的相遇。",
             "随笔 essay", "Deep", "/covers/leaf.jpg", "2024-10-12", 890, 73),
            ("京都：千年的回响",
             "在祇园的石板路上，寻找时间的足迹。",
             "全文内容……京都是一座会呼吸的博物馆，每一块石砖都有故事。",
             "摄影 photography", "Journey", "/covers/kyoto.jpg", "2024-08-03", 1100, 95),
            ("设计中的留白艺术",
             "少即是多。在繁杂的信息流中，如何通过空间构建呼吸感，让视觉重获自由。",
             "全文内容……留白是设计师的沉默，是最响亮的语言。",
             "设计哲学", "Inspired", None, "2024-09-28", 630, 41),
            ("重构生活系统",
             "利用 Notion 和数字化工具，打造第二大脑，释放创造力。",
             "全文内容……GTD 方法的核心是清空大脑，让系统来记忆。",
             "生活 life", "Tech", None, "2024-07-20", 780, 58),
            ("夜读《悉达多》",
             "每个人都要走自己的河流。听河水的声音，学会与流动和解。",
             "全文内容……黑塞用一个故事道尽了悟的全部路径。",
             "读书 reading", "Deep", None, "2024-09-15", 450, 89),
            ("雨声入梦",
             "一场夏雨，洗净了城市的喧嚣。",
             "全文内容……雨天是城市暂时放下面具的时刻。",
             "生活 life", "Calm", None, "2024-06-11", 310, 34),
        ]
        cur.executemany(
            "INSERT INTO posts (title,summary,content,category,mood,cover_image,date,views,likes) VALUES (?,?,?,?,?,?,?,?,?)",
            posts
        )

    # Seed tasks if empty
    cur.execute("SELECT COUNT(*) FROM tasks")
    if cur.fetchone()[0] == 0:
        tasks = [
            ("深入学习 TypeScript", "学习", "高优先级"),
            ("整理书房", "生活", "普通"),
            ("购买绿植", "购物", "普通"),
            ("练习书法", "兴趣", "普通"),
            ("给父母打电话", "家庭", "普通"),
        ]
        cur.executemany("INSERT INTO tasks (title,tag,priority) VALUES (?,?,?)", tasks)

    conn.commit()
    conn.close()

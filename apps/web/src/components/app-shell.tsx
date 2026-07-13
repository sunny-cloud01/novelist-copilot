import { BookOpen, ChevronRight, FileText, Home, Network, PenLine, Settings, ShieldAlert, Sparkles } from "lucide-react";
import { Link, Outlet } from "react-router-dom";

const navItems = [
  { to: "/workspaces/demo-workspace", label: "Home", description: "工作台", icon: Home },
  { to: "/sources", label: "Sources", description: "来源与拆书", icon: BookOpen },
  { to: "/knowledge", label: "Knowledge", description: "知识包", icon: Network },
  { to: "/projects", label: "Projects", description: "小说项目", icon: FileText },
  { to: "/projects/01JZPROJECT000000000000001/writing/01JZWRITING00000000000001", label: "Writing", description: "章节生成", icon: PenLine },
  { to: "/review", label: "Review", description: "异常处理", icon: ShieldAlert },
  { to: "/reports", label: "Reports", description: "质量反馈", icon: Sparkles },
  { to: "/settings", label: "Settings", description: "模型配置", icon: Settings },
];

export function AppShell() {
  return (
    <div className="nf-shell">
      <aside className="nf-sidebar">
        <div className="nf-brand">
          <h1>Novel Factory</h1>
          <p>上传参考作品，自动拆书，沉淀可复用知识，再生成原创章节。</p>
        </div>
        <nav aria-label="主导航">
          <ul className="nf-nav-list">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <li key={`${item.label}-${item.to}`}>
                  <Link className="nf-nav-link" to={item.to}>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
                      <Icon aria-hidden="true" size={18} />
                      <span>
                        <strong>{item.label}</strong>
                        <span style={{ display: "block", color: "var(--nf-muted)", fontSize: 12 }}>{item.description}</span>
                      </span>
                    </span>
                    <ChevronRight aria-hidden="true" size={16} />
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>
      </aside>
      <main className="nf-main">
        <header className="nf-topbar">
          <div>
            <h2>创作者工作台</h2>
            <p>少输入，自动运行，只在异常和关键确认处打断。</p>
          </div>
          <span
            style={{
              border: "1px solid var(--nf-border)",
              borderRadius: 999,
              color: "var(--nf-success)",
              padding: "6px 10px",
              fontSize: 12,
              fontWeight: 700,
            }}
          >
            Demo workspace
          </span>
        </header>
        <div className="nf-content-frame">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

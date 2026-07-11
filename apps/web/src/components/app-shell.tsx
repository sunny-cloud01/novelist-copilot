import { Link, Outlet } from "react-router-dom";

const navItems = [
  { to: "/workspaces/demo-workspace", label: "工作台首页" },
  { to: "/sources", label: "来源书库" },
  { to: "/knowledge/review", label: "知识审核" },
  { to: "/graph", label: "故事图谱" },
  { to: "/projects", label: "小说项目" },
  { to: "/feedback", label: "反馈看板" },
  { to: "/configuration", label: "配置中心" },
];

export function AppShell() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
      <aside style={{ borderRight: "1px solid #d4d4d8", padding: "24px" }}>
        <h1>小说工坊</h1>
        <nav aria-label="主导航">
          <ul style={{ display: "grid", gap: "12px", padding: 0, listStyle: "none" }}>
            {navItems.map((item) => (
              <li key={item.to}>
                <Link to={item.to}>{item.label}</Link>
              </li>
            ))}
          </ul>
        </nav>
      </aside>
      <main style={{ padding: "24px" }}>
        <Outlet />
      </main>
    </div>
  );
}

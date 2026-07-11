import { Link, Outlet } from "react-router-dom";

const navItems = [
  { to: "/workspaces/demo-workspace", label: "Workspace Home" },
  { to: "/sources", label: "Source Library" },
  { to: "/knowledge/review", label: "Knowledge Review" },
  { to: "/graph", label: "Story Graph Viewer" },
  { to: "/projects", label: "Novel Projects" },
  { to: "/feedback", label: "Feedback Dashboard" },
  { to: "/configuration", label: "Configuration" },
];

export function AppShell() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "100vh" }}>
      <aside style={{ borderRight: "1px solid #d4d4d8", padding: "24px" }}>
        <h1>Novel Factory</h1>
        <nav aria-label="Primary">
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

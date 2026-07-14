import { BookOpen, PenLine, Settings } from "lucide-react";
import { useState } from "react";
import { Link, Outlet, useLocation } from "react-router-dom";

import { Separator } from "@/components/ui/separator";

type Lane = "deconstruct" | "write";

const lanes = [
  {
    id: "deconstruct" as Lane,
    icon: BookOpen,
    label: "拆书",
    hint: "上传参考作品，自动拆解为知识",
    color: "amber",
    path: "/sources",
  },
  {
    id: "write" as Lane,
    icon: PenLine,
    label: "写书",
    hint: "基于知识包生成原创章节",
    color: "indigo",
    path: "/projects",
  },
] as const;

export function AppShell() {
  const location = useLocation();
  const currentLane: Lane = location.pathname.startsWith("/projects")
    ? "write"
    : "deconstruct";
  const [activeLane, setActiveLane] = useState<Lane>(currentLane);

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* ===== Left Rail: 56px icon-only sidebar ===== */}
      <aside className="flex w-14 shrink-0 flex-col items-center gap-3 border-r border-border bg-sidebar py-4">
        {/* Brand mark */}
        <div className="mb-2 flex h-8 w-8 items-center justify-center rounded-lg bg-primary/15">
          <span className="font-['Playfair_Display',Georgia,serif] text-xs font-bold text-primary">
            NF
          </span>
        </div>

        <Separator className="w-8" />

        {/* Two main lanes: Deconstruct (amber) and Write (indigo) */}
        {lanes.map((lane) => {
          const Icon = lane.icon;
          const isActive = activeLane === lane.id;
          return (
            <Link
              key={lane.id}
              to={lane.path}
              onClick={() => setActiveLane(lane.id)}
              title={lane.hint}
              className={`flex h-9 w-9 items-center justify-center rounded-lg transition-all duration-200 hover:bg-accent ${
                isActive
                  ? lane.color === "amber"
                    ? "bg-secondary/15 text-secondary shadow-sm shadow-secondary/10"
                    : "bg-primary/15 text-primary shadow-sm shadow-primary/10"
                  : "text-muted-foreground"
              }`}
            >
              <Icon size={18} />
            </Link>
          );
        })}

        {/* Spacer pushes settings to bottom */}
        <div className="flex-1" />

        <Separator className="w-8" />

        <Link
          to="/settings"
          className="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-all duration-200 hover:bg-accent hover:text-foreground"
          title="设置"
        >
          <Settings size={18} />
        </Link>
      </aside>

      {/* ===== Right: Workspace ===== */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* Top bar: context-aware header */}
        <header className="flex h-12 shrink-0 items-center justify-between border-b border-border px-6">
          <div className="flex items-center gap-3">
            <h1 className="font-['Playfair_Display',Georgia,serif] text-sm font-semibold tracking-wide text-foreground">
              {activeLane === "deconstruct" ? "拆书工作台" : "写书工作台"}
            </h1>
            <span className="hidden text-xs text-muted-foreground sm:inline">
              {activeLane === "deconstruct"
                ? "上传 → 自动拆解 → 知识沉淀"
                : "选择知识包 → 生成章节 → 审核发布"}
            </span>
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span className="inline-flex h-1.5 w-1.5 rounded-full bg-success" />
            Demo workspace
          </div>
        </header>

        {/* Divider with breathing animation — signature element */}
        <div className="relative h-px shrink-0 bg-gradient-to-r from-secondary/40 via-primary/20 to-transparent">
          <div className="absolute inset-0 animate-breathe bg-gradient-to-r from-secondary/20 via-primary/30 to-transparent" />
        </div>

        {/* Scrollable content area */}
        <main className="flex-1 overflow-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

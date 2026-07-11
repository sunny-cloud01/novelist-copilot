import { createBrowserRouter } from "react-router-dom";

import { AppShell } from "./components/app-shell";
import {
  ConfigurationPage,
  ExtractionRunPage,
  FeedbackPage,
  GraphPage,
  KnowledgeReviewPage,
  PlannerPage,
  ProjectHomePage,
  ProjectListPage,
  SourceBookPage,
  SourceLibraryPage,
  WorkspaceHomePage,
  WritingStudioPage,
} from "./pages";

export const routes = [
  {
    path: "/",
    element: <AppShell />,
    children: [
      { path: "workspaces/:workspaceId", element: <WorkspaceHomePage /> },
      { path: "sources", element: <SourceLibraryPage /> },
      { path: "sources/:bookId", element: <SourceBookPage /> },
      { path: "extraction-runs/:runId", element: <ExtractionRunPage /> },
      { path: "knowledge/review", element: <KnowledgeReviewPage /> },
      { path: "graph", element: <GraphPage /> },
      { path: "projects", element: <ProjectListPage /> },
      { path: "projects/:projectId", element: <ProjectHomePage /> },
      { path: "projects/:projectId/planner", element: <PlannerPage /> },
      { path: "projects/:projectId/writing/:writingRunId", element: <WritingStudioPage /> },
      { path: "feedback", element: <FeedbackPage /> },
      { path: "configuration", element: <ConfigurationPage /> },
    ],
  },
];

export const router = createBrowserRouter(routes);

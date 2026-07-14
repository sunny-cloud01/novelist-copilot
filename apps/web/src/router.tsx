import { createBrowserRouter } from "react-router-dom";

import { AppShell } from "@/components/app-shell";
import { BookAnalysisCenterPage } from "@/features/book-analysis/book-analysis-center-page";
import { SourceDetailPage } from "@/features/sources/source-detail-page";
import { SourceLibraryPage } from "@/features/sources/source-library-page";
import { KnowledgeHomePage } from "@/features/knowledge/knowledge-home-page";
import { KnowledgePackageDetailPage } from "@/features/knowledge/knowledge-package-detail-page";
import { StoryBibleWizardPage } from "@/features/projects/story-bible-wizard-page";
import { ChapterDirectionSetupPage } from "@/features/projects/chapter-direction-setup-page";
import { WritingRunDetailPage } from "@/features/projects/writing-run-detail-page";
import { ReportsPage } from "@/features/reports/reports-page";
import { ReviewQueuePage } from "@/features/review/review-queue-page";
import { QualityReviewPage } from "@/features/review/quality-review-page";
import { ChapterApprovalPage } from "@/features/review/chapter-approval-page";
import {
  ConfigurationPage,
  ExtractionRunPage,
  FeedbackPage,
  GraphPage,
  KnowledgeReviewPage,
  PlannerPage,
  ProjectHomePage,
  ProjectListPage,
  WorkspaceHomePage,
  WritingStudioPage,
} from "@/pages";

export const routes = [
  {
    path: "/",
    element: <AppShell />,
    children: [
      { path: "workspaces/:workspaceId", element: <WorkspaceHomePage /> },
      { path: "sources", element: <SourceLibraryPage /> },
      { path: "sources/:bookId", element: <SourceDetailPage /> },
      { path: "sources/:bookId/analysis", element: <BookAnalysisCenterPage /> },
      { path: "extraction-runs/:runId", element: <ExtractionRunPage /> },
      { path: "knowledge", element: <KnowledgeHomePage /> },
      { path: "knowledge/review", element: <KnowledgeReviewPage /> },
      {
        path: "knowledge-packages/:packageId",
        element: <KnowledgePackageDetailPage />,
      },
      { path: "review", element: <ReviewQueuePage /> },
      { path: "graph", element: <GraphPage /> },
      { path: "projects", element: <ProjectListPage /> },
      { path: "projects/new/story-bible", element: <StoryBibleWizardPage /> },
      { path: "projects/:projectId", element: <ProjectHomePage /> },
      { path: "projects/:projectId/planner", element: <PlannerPage /> },
      {
        path: "projects/:projectId/chapters/:chapterIndex/setup",
        element: <ChapterDirectionSetupPage />,
      },
      {
        path: "projects/:projectId/writing-runs/:writingRunId",
        element: <WritingRunDetailPage />,
      },
      {
        path: "projects/:projectId/writing/:writingRunId",
        element: <WritingStudioPage />,
      },
      {
        path: "projects/:projectId/writing-runs/:writingRunId/quality-review",
        element: <QualityReviewPage />,
      },
      {
        path: "projects/:projectId/writing-runs/:writingRunId/approval",
        element: <ChapterApprovalPage />,
      },
      { path: "feedback", element: <FeedbackPage /> },
      { path: "reports", element: <ReportsPage /> },
      { path: "configuration", element: <ConfigurationPage /> },
      { path: "settings", element: <ConfigurationPage /> },
    ],
  },
];

export const router = createBrowserRouter(routes, {
  future: {
    v7_startTransition: true,
  },
});

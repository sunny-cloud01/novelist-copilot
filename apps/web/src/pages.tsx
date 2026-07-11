function Page({ title, body }: { title: string; body: string }) {
  return (
    <section>
      <h2>{title}</h2>
      <p>{body}</p>
    </section>
  );
}

export const WorkspaceHomePage = () => <Page title="Workspace Home" body="Recent tasks, pending reviews, and workspace entry point." />;
export const SourceLibraryPage = () => <Page title="Source Library" body="Upload reference books and inspect chapter import state." />;
export const SourceBookPage = () => <Page title="Source Book Detail" body="Inspect chapter segmentation and source file metadata." />;
export const ExtractionRunPage = () => <Page title="Extraction Run Detail" body="Track extraction status, errors, and run reports." />;
export const KnowledgeReviewPage = () => <Page title="Knowledge Review" body="Approve, reject, merge alias, or request re-extract on candidates." />;
export const GraphPage = () => <Page title="Story Graph Viewer" body="Browse graph nodes, edges, and snapshot details." />;
export const ProjectListPage = () => <Page title="Novel Projects" body="List projects, story bibles, and chapter progress." />;
export const ProjectHomePage = () => <Page title="Novel Project Home" body="Review story bible, chapter list, and project status." />;
export const PlannerPage = () => <Page title="Chapter Planner" body="Review chapter, scene, and beat planning outputs." />;
export const WritingStudioPage = () => <Page title="Writing Studio" body="Inspect writing run state, drafts, critic issues, and quality results." />;
export const FeedbackPage = () => <Page title="Feedback Dashboard" body="Inspect cost, AI flavor, edit distance, and strategy suggestions." />;
export const ConfigurationPage = () => <Page title="Configuration" body="Manage model profiles, quality thresholds, and prompt versions." />;

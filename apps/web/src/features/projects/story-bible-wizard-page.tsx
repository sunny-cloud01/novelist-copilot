import { FormEvent, useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { createNovelFactoryApiClient } from "../../lib/api-client";

type KnowledgeSource = {
  source_ref: string;
  label: string;
  status: string;
  knowledge_object_count: number;
  evidence_count: number;
};

export function StoryBibleWizardPage() {
  const navigate = useNavigate();
  const apiBaseUrl = import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL as string | undefined;
  const apiClient = useMemo(() => (apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null), [apiBaseUrl]);
  const [sources, setSources] = useState<KnowledgeSource[]>([]);
  const [selectedRefs, setSelectedRefs] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient) return;
    apiClient.listKnowledgeSources({ status: "committed" })
      .then((payload) => setSources(((payload as { items?: KnowledgeSource[] }).items ?? [])))
      .catch((caught) => setError(caught instanceof Error ? caught.message : "Knowledge sources load failed"));
  }, [apiClient]);

  function toggleSource(sourceRef: string, checked: boolean) {
    setSelectedRefs((current) => checked ? [...new Set([...current, sourceRef])] : current.filter((item) => item !== sourceRef));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    const form = new FormData(event.currentTarget);
    const payload = {
      title: String(form.get("title") ?? ""),
      genre_scope: String(form.get("genreScope") ?? ""),
      allowed_knowledge_source_refs: selectedRefs,
      story_bible_payload: {
        premise: String(form.get("premise") ?? ""),
        protagonist: String(form.get("protagonist") ?? ""),
        core_conflict: String(form.get("coreConflict") ?? ""),
        style_target: String(form.get("styleTarget") ?? ""),
        forbidden_similarities: String(form.get("forbiddenSimilarities") ?? ""),
      },
    };
    if (!apiClient) {
      setError("请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后创建 Story Bible。");
      return;
    }
    try {
      const created = await apiClient.createNovelProject(payload) as { project?: { project_id?: string } };
      navigate(`/projects/${created.project?.project_id ?? ""}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Story Bible create failed");
    }
  }

  return (
    <section className="nf-source-page">
      <div className="nf-analysis-hero">
        <div>
          <h2>Story Bible Wizard</h2>
          <p>选择已提交知识源，生成新书世界观、主角、冲突和原创边界草稿。</p>
        </div>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>创建原创项目与 Story Bible</CardTitle>
          <CardDescription>知识源进入项目级 allowed_knowledge_source_refs。</CardDescription>
        </CardHeader>
        <CardContent>
          <form aria-label="Story Bible Wizard" className="nf-form-grid" onSubmit={handleSubmit}>
            <label className="nf-field">项目标题<input name="title" defaultValue="原创仙侠项目" /></label>
            <label className="nf-field">题材范围<input name="genreScope" defaultValue="仙侠成长流" /></label>
            <fieldset className="nf-field">
              <legend>选择知识来源</legend>
              {sources.length === 0 ? <p>暂无 API 知识源；提交前请先完成知识包。</p> : null}
              {sources.map((source) => (
                <label key={source.source_ref}>
                  <input type="checkbox" onChange={(event) => toggleSource(source.source_ref, event.target.checked)} />
                  {source.label} · {source.status} · 知识 {source.knowledge_object_count} · 证据 {source.evidence_count}
                </label>
              ))}
            </fieldset>
            <label className="nf-field">故事前提<textarea name="premise" defaultValue="少年从边陲小镇踏入修行世界。" /></label>
            <label className="nf-field">主角<input name="protagonist" defaultValue="林澈" /></label>
            <label className="nf-field">核心冲突<textarea name="coreConflict" defaultValue="底层修士与宗门规则之间的成长冲突。" /></label>
            <label className="nf-field">风格目标<input name="styleTarget" defaultValue="克制、证据充分、节奏稳步升级" /></label>
            <label className="nf-field">禁用相似点<textarea name="forbiddenSimilarities" defaultValue="不复刻原作人物名、金手指机制和关键桥段。" /></label>
            {error ? <p role="alert">{error}</p> : null}
            <Button type="submit">Create Story Bible</Button>
          </form>
        </CardContent>
      </Card>
    </section>
  );
}

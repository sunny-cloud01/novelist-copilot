import { ChangeEvent, FormEvent, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { DEMO_BOOK_ID } from "../../components/phase-two-state";
import { createNovelFactoryApiClient } from "../../lib/api-client";
import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../../components/ui/card";
import { usePhaseTwo } from "../../state/phase-two-provider";

export function SourceLibraryPage() {
  const navigate = useNavigate();
  const { state, uploadBook } = usePhaseTwo();
  const apiBaseUrl = import.meta.env.VITE_NOVEL_FACTORY_API_BASE_URL as string | undefined;
  const apiClient = useMemo(() => (apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null), [apiBaseUrl]);
  const [error, setError] = useState<string | null>(null);
  const [sourceText, setSourceText] = useState("第一章 乌坦城风起……");
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    setError(null);
    const file = event.currentTarget.files?.[0];
    if (!file) {
      setSelectedFileName(null);
      return;
    }
    const isTxt = file.type === "text/plain" || file.name.toLowerCase().endsWith(".txt");
    if (!isTxt) {
      setSelectedFileName(null);
      setError("仅支持 .txt 文本文件。");
      event.currentTarget.value = "";
      return;
    }
    try {
      const text = await file.text();
      if (!text.trim()) {
        setSelectedFileName(null);
        setError("TXT 文件为空，请重新选择。");
        event.currentTarget.value = "";
        return;
      }
      setSourceText(text);
      setSelectedFileName(file.name);
    } catch {
      setSelectedFileName(null);
      setError("TXT 文件读取失败，请重新选择。");
      event.currentTarget.value = "";
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    const form = new FormData(event.currentTarget);
    const title = String(form.get("title") ?? "");
    const authorName = String(form.get("authorName") ?? "");
    const sourceType = String(form.get("sourceType") ?? "reference_novel");
    if (apiClient) {
      try {
        const book = await apiClient.createBook({
          title,
          author_name: authorName,
          source_type: sourceType,
          platform: String(form.get("platform") ?? ""),
          genre: String(form.get("genre") ?? ""),
          usage_boundary: String(form.get("usageBoundary") ?? ""),
          source_text: String(form.get("sourceText") ?? ""),
        }) as { book_id: string };
        await apiClient.createExtractionRun(book.book_id);
        navigate(`/sources/${book.book_id}/analysis`);
        return;
      } catch (caught) {
        setError(caught instanceof Error ? caught.message : "Upload failed");
        return;
      }
    }
    uploadBook({ title, authorName, sourceType });
    navigate(`/sources/${DEMO_BOOK_ID}/analysis`);
  }

  return (
    <section className="nf-source-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="success">Sources</Badge>
          <h2>上传参考作品，自动拆书学习</h2>
          <p>确认来源边界后，系统自动完成章节切分、对象抽取、证据绑定、套路节奏分析和知识包准备。</p>
        </div>
        <div className="nf-analysis-actions">
          <Button asChild variant="secondary">
            <Link to={`/sources/${state.book.bookId}/analysis`}>继续分析中心</Link>
          </Button>
        </div>
      </div>

      <div className="nf-source-grid">
        <Card>
          <CardHeader>
            <CardTitle>Upload Source</CardTitle>
            <CardDescription>少填字段，上传后直接进入自动分析。</CardDescription>
          </CardHeader>
          <CardContent>
            <form aria-label="上传来源书籍" className="nf-form-grid" onSubmit={handleSubmit}>
              <label className="nf-field">
                书名
                <input name="title" defaultValue="Battle Through the Heavens" />
              </label>
              <label className="nf-field">
                作者
                <input name="authorName" defaultValue="Tian Can Tu Dou" />
              </label>
              <label className="nf-field">
                平台
                <input name="platform" defaultValue="起点中文网" />
              </label>
              <label className="nf-field">
                题材
                <input name="genre" defaultValue="玄幻升级流" />
              </label>
              <label className="nf-field">
                来源类型
                <select name="sourceType" defaultValue="reference_novel">
                  <option value="reference_novel">参考小说</option>
                  <option value="outline">大纲</option>
                </select>
              </label>
              <label className="nf-field">
                文本粘贴 / TXT 文件
                <input aria-label="选择 TXT 文件" accept=".txt,text/plain" name="sourceFile" onChange={handleFileChange} type="file" />
                <textarea aria-label="文本粘贴 / TXT 文件内容" name="sourceText" rows={4} value={sourceText} onChange={(event) => setSourceText(event.target.value)} />
                <span>{selectedFileName ? `已读取 ${selectedFileName}，可继续编辑文本。` : "可粘贴文本，或选择 .txt 文件自动填入。"}</span>
              </label>
              <label className="nf-field">
                用途边界
                <input name="usageBoundary" defaultValue="仅供结构学习，不直接复写原文。" />
              </label>
              {error ? <p role="alert">{error}</p> : null}
              <Button type="submit">Upload and Analyze</Button>
            </form>
          </CardContent>
        </Card>

        <div className="nf-analysis-stack">
          <Card>
            <CardHeader>
              <CardTitle>Recent analysis</CardTitle>
              <CardDescription>最近来源与自动拆书状态。</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="nf-source-list">
                <li className="nf-source-item">
                  <div className="nf-row-between">
                    <h3>{state.book.title}</h3>
                    <Badge variant="warning">{state.run.status}</Badge>
                  </div>
                  <p>{state.book.authorName} · {state.book.sourceType} · 章节 {state.run.chapterCount} · 证据 {state.run.evidenceCount}</p>
                  <p>下一步：处理 {state.bookAnalysisSummary.needsAttentionCount} 个异常后提交知识包。</p>
                  <Button asChild size="sm" variant="secondary">
                    <Link to={`/sources/${state.book.bookId}/analysis`}>打开拆书分析中心</Link>
                  </Button>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Usage boundary</CardTitle>
              <CardDescription>平台只学习结构、节奏、证据和套路，不直接复写原文。</CardDescription>
            </CardHeader>
            <CardContent>
              <p>上传来源用于抽取可追踪知识资产：人物、势力、事件、冲突、悬念、爽点、Pattern、Rhythm、Asset 与 Rule。</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}

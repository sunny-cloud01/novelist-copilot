import { ChangeEvent, FormEvent, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { resolveApiBaseUrl } from "@/lib/api-base";
import { createNovelFactoryApiClient } from "@/lib/api-client";

type RecentBook = {
  bookId: string;
  title: string;
  authorName: string;
  sourceType: string;
};

export function SourceLibraryPage() {
  const navigate = useNavigate();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const [error, setError] = useState<string | null>(null);
  const [sourceText, setSourceText] = useState("第一章 乌坦城风起……");
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [lastApiBook, setLastApiBook] = useState<RecentBook | null>(null);

  const recentBook: RecentBook | null = lastApiBook;

  async function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    setError(null);
    const file = event.currentTarget.files?.[0];
    if (!file) {
      setSelectedFileName(null);
      return;
    }
    const isTxt =
      file.type === "text/plain" || file.name.toLowerCase().endsWith(".txt");
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
    setSubmitting(true);
    const form = new FormData(event.currentTarget);
    const title = String(form.get("title") ?? "");
    const authorName = String(form.get("authorName") ?? "");
    const sourceType = String(form.get("sourceType") ?? "reference_novel");
    if (!apiClient) {
      setError("请配置 VITE_NOVEL_FACTORY_API_BASE_URL 后再上传。");
      setSubmitting(false);
      return;
    }
    try {
      const book: any = await apiClient.createBook({
        title,
        author_name: authorName,
        source_type: sourceType,
        platform: String(form.get("platform") ?? ""),
        genre: String(form.get("genre") ?? ""),
        usage_boundary: String(form.get("usageBoundary") ?? ""),
        source_text: String(form.get("sourceText") ?? ""),
      });
      await apiClient.createExtractionRun(book.book_id);
      setLastApiBook({ bookId: book.book_id, title, authorName, sourceType });
      setSubmitting(false);
      navigate(`/sources/${book.book_id}/analysis`);
      return;
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Upload failed");
      setSubmitting(false);
      return;
    }
  }

  return (
    <div className="space-y-6">
      {/* Hero banner */}
      <div className="flex flex-wrap items-start justify-between gap-4 rounded-xl border border-border bg-card p-6">
        <div>
          <Badge variant="success" className="mb-2">
            Sources
          </Badge>
          <h2 className="mt-1 text-xl font-semibold tracking-tight">
            上传参考作品，自动拆书学习
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            确认来源边界后，系统自动完成章节切分、对象抽取、证据绑定、套路节奏分析和知识包准备。
          </p>
        </div>
        {lastApiBook ? (
          <Button asChild variant="secondary">
            <Link to={`/sources/${lastApiBook.bookId}/analysis`}>
              继续分析中心
            </Link>
          </Button>
        ) : null}
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-[1fr_1.2fr]">
        {/* Upload form */}
        <Card>
          <CardHeader>
            <CardTitle>Upload Source</CardTitle>
            <CardDescription>
              少填字段，上传后直接进入自动分析。
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form
              aria-label="上传来源书籍"
              className="space-y-4"
              onSubmit={handleSubmit}
            >
              <div className="space-y-2">
                <label className="text-sm font-medium">书名</label>
                <input
                  name="title"
                  defaultValue="Battle Through the Heavens"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">作者</label>
                <input
                  name="authorName"
                  defaultValue="Tian Can Tu Dou"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">平台</label>
                <input
                  name="platform"
                  defaultValue="起点中文网"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">题材</label>
                <input
                  name="genre"
                  defaultValue="玄幻升级流"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">来源类型</label>
                <select
                  name="sourceType"
                  defaultValue="reference_novel"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                >
                  <option value="reference_novel">参考小说</option>
                  <option value="outline">大纲</option>
                </select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  文本粘贴 / TXT 文件
                </label>
                <input
                  aria-label="选择 TXT 文件"
                  accept=".txt,text/plain"
                  name="sourceFile"
                  onChange={handleFileChange}
                  type="file"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
                <textarea
                  aria-label="文本粘贴 / TXT 文件内容"
                  name="sourceText"
                  rows={4}
                  value={sourceText}
                  onChange={(event) => setSourceText(event.target.value)}
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                />
                {selectedFileName && (
                  <span className="text-xs text-muted-foreground">
                    {selectedFileName}
                  </span>
                )}
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">使用边界</label>
                <select
                  name="usageBoundary"
                  defaultValue="analysis_only"
                  className="w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                >
                  <option value="analysis_only">仅分析</option>
                  <option value="fragment_reuse">片段复用</option>
                </select>
              </div>
              {error && <p className="text-sm text-destructive">{error}</p>}
              <Button type="submit" className="w-full" disabled={submitting}>
                {submitting ? "上传中..." : "上传并开始拆书"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Recent uploads + activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Sources</CardTitle>
            <CardDescription>最近上传的参考作品</CardDescription>
          </CardHeader>
          <CardContent>
            {recentBook ? (
              <div className="rounded-lg border border-border p-4">
                <h3 className="font-medium">{recentBook.title}</h3>
                <p className="text-sm text-muted-foreground">
                  {recentBook.authorName} · {recentBook.sourceType}
                </p>
                <Button asChild variant="outline" size="sm" className="mt-3">
                  <Link to={`/sources/${recentBook.bookId}`}>查看详情</Link>
                </Button>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                暂无上传记录。上传第一本参考作品开始拆书。
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

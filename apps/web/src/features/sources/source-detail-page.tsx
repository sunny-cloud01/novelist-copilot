import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { Badge } from "../../components/ui/badge";
import { Button } from "../../components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../../components/ui/card";
import { createNovelFactoryApiClient } from "@/lib/api-client";
import { resolveApiBaseUrl } from "@/lib/api-base";

type ApiChapter = {
  chapter_id: string;
  chapter_index: number;
  title: string;
  segmentation_status: string;
};

type ApiBook = {
  book_id: string;
  title: string;
  author_name: string;
  source_type: string;
  import_status: string;
  trace_id: string;
};

export function SourceDetailPage() {
  const { bookId } = useParams();
  const apiBaseUrl = resolveApiBaseUrl();
  const apiClient = useMemo(
    () =>
      apiBaseUrl ? createNovelFactoryApiClient({ baseUrl: apiBaseUrl }) : null,
    [apiBaseUrl]
  );
  const activeBookId = bookId ?? "";

  const [apiBook, setApiBook] = useState<ApiBook | null>(null);
  const [apiChapters, setApiChapters] = useState<ApiChapter[] | null>(null);
  const [loading, setLoading] = useState(Boolean(apiClient));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!apiClient || !activeBookId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);
    void Promise.all([
      apiClient.getBook(activeBookId) as Promise<ApiBook>,
      apiClient.listBookChapters(activeBookId) as Promise<{
        items: ApiChapter[];
      }>,
    ])
      .then(([book, chaptersPayload]) => {
        if (cancelled) return;
        setApiBook(book);
        setApiChapters(chaptersPayload.items ?? []);
      })
      .catch((caught) => {
        if (cancelled) return;
        setError(caught instanceof Error ? caught.message : "来源书加载失败");
        setApiBook(null);
        setApiChapters(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [activeBookId, apiClient]);

  const book: any = apiBook;
  const chapters = apiChapters ?? [];
  const importStatus = apiBook?.import_status ?? "";
  const traceId = apiBook?.trace_id ?? "";

  if (!apiClient) {
    return (
      <section className="nf-source-page">
        <h2>请配置 API</h2>
        <p>设置 VITE_NOVEL_FACTORY_API_BASE_URL 后刷新页面。</p>
      </section>
    );
  }
  if (loading) {
    return (
      <section className="nf-source-page">
        <h2>正在加载来源书...</h2>
      </section>
    );
  }
  if (error) {
    return (
      <section className="nf-source-page">
        <h2>来源书加载失败</h2>
        <p role="alert">{error}</p>
      </section>
    );
  }

  return (
    <section className="nf-source-page">
      <div className="nf-analysis-hero">
        <div>
          <Badge variant="warning">{importStatus}</Badge>
          <h2>来源书详情</h2>
          <p>查看《{book.title}》的来源元数据、章节切分和自动分析入口。</p>
        </div>
        <div className="nf-analysis-actions">
          <Button asChild>
            <Link to={`/sources/${activeBookId}/analysis`}>
              进入拆书分析中心
            </Link>
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>来源元数据</CardTitle>
          <CardDescription>{traceId}</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="nf-metric-grid">
            <div className="nf-metric">
              <span>书籍 ID</span>
              <strong>{activeBookId}</strong>
            </div>
            <div className="nf-metric">
              <span>作者</span>
              <strong>{book.authorName ?? (book as any).author_name}</strong>
            </div>
            <div className="nf-metric">
              <span>来源类型</span>
              <strong>{book.sourceType ?? (book as any).source_type}</strong>
            </div>
            <div className="nf-metric">
              <span>章节数</span>
              <strong>{chapters.length}</strong>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>章节列表</CardTitle>
          <CardDescription>
            已完成基础切章，下一步进入自动拆书分析。
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="nf-source-list">
            {chapters.map((chapter: any) => (
              <li
                className="nf-source-item"
                key={chapter.chapterId ?? chapter.chapter_id}
              >
                <h3>
                  第 {chapter.chapterIndex ?? chapter.chapter_index} 章：
                  {chapter.title}
                </h3>
                <p>
                  {chapter.segmentationStatus ?? chapter.segmentation_status}
                </p>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </section>
  );
}

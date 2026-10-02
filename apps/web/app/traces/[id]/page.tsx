import { getTrace } from "../../lib";

export default async function TraceDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const detail = await getTrace(id);
  if (!detail) return <h1>Trace not found</h1>;
  return (
    <>
      <div className="topline">
        <div>
          <h1>{detail.trace.name}</h1>
          <p>{detail.trace.id}</p>
        </div>
        <span className={`pill ${detail.trace.status}`}>{detail.trace.status}</span>
      </div>
      <section className="trace-flow">
        {detail.spans.map((span) => (
          <article className="span" key={span.id}>
            <div>
              <div className="label">{span.type}</div>
              <strong>{span.name}</strong>
              <p>{span.provider || "local"} {span.model ? `· ${span.model}` : ""}</p>
            </div>
            <div className="code">
              <pre>{JSON.stringify({ input: span.input, output: span.output }, null, 2)}</pre>
            </div>
            <div>
              <span className={`pill ${span.status}`}>{span.status}</span>
              <p>{span.duration_ms ?? 0} ms</p>
              <p>{span.token_usage?.total_tokens ?? 0} tokens</p>
            </div>
          </article>
        ))}
      </section>
    </>
  );
}


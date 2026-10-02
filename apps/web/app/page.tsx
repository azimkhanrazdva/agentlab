import Link from "next/link";
import { getTraces } from "./lib";

export default async function Dashboard() {
  const traces = await getTraces();
  const ok = traces.filter((trace) => trace.status === "ok").length;
  const errors = traces.filter((trace) => trace.status === "error").length;

  return (
    <>
      <div className="topline">
        <div>
          <h1>AgentLab Control Plane</h1>
          <p>Open-source DevTools and security testing platform for AI agents.</p>
        </div>
        <span className="pill">Gateway: /v1/chat/completions</span>
      </div>
      <section className="grid stats">
        <div className="card"><div className="label">Traces</div><div className="metric">{traces.length}</div></div>
        <div className="card"><div className="label">Successful</div><div className="metric">{ok}</div></div>
        <div className="card"><div className="label">Errors</div><div className="metric">{errors}</div></div>
        <div className="card"><div className="label">Attack Lab</div><div className="metric">1 planned</div></div>
      </section>
      <div style={{ height: 18 }} />
      <section className="card">
        <h2>First run</h2>
        <p>Point an OpenAI-compatible client at AgentLab, run the demo agent, then inspect the trace.</p>
        <div className="code">
          <pre>{`python examples/basic-agent/main.py\nopen http://localhost:3000/traces`}</pre>
        </div>
      </section>
      <div style={{ height: 18 }} />
      <section>
        <h2>Recent traces</h2>
        <table className="table">
          <tbody>
            {traces.slice(0, 6).map((trace) => (
              <tr key={trace.id}>
                <td><Link href={`/traces/${trace.id}`}>{trace.name}</Link></td>
                <td><span className={`pill ${trace.status}`}>{trace.status}</span></td>
                <td>{new Date(trace.started_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}


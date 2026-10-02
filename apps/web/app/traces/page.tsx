import Link from "next/link";
import { getTraces } from "../lib";

export default async function TracesPage() {
  const traces = await getTraces();
  return (
    <>
      <div className="topline">
        <div>
          <h1>Traces</h1>
          <p>Every gateway request becomes a trace with spans, usage and provider metadata.</p>
        </div>
      </div>
      <table className="table">
        <thead>
          <tr><th>Name</th><th>Status</th><th>Session</th><th>Started</th></tr>
        </thead>
        <tbody>
          {traces.map((trace) => (
            <tr key={trace.id}>
              <td><Link href={`/traces/${trace.id}`}>{trace.name}</Link></td>
              <td><span className={`pill ${trace.status}`}>{trace.status}</span></td>
              <td>{trace.session_id || "none"}</td>
              <td>{new Date(trace.started_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}


export default function SecurityPage() {
  return (
    <>
      <h1>Security</h1>
      <p>Implemented now: deterministic risk scoring, policy decisions and secret redaction API. Security event timelines are planned after controlled tool execution lands.</p>
      <div className="card">
        <div className="label">Policy endpoint</div>
        <div className="code"><pre>{`POST /api/v1/tools/evaluate`}</pre></div>
      </div>
    </>
  );
}


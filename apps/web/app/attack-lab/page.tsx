export default function AttackLabPage() {
  return (
    <>
      <h1>Attack Lab</h1>
      <p>Run the included indirect prompt injection scenario through the backend API and inspect whether unsafe attempts are blocked by policy.</p>
      <div className="card">
        <div className="label">Scenario</div>
        <div className="code"><pre>{`curl -X POST http://localhost:8000/api/v1/attacks/run \\\n  -H "content-type: application/json" \\\n  -d '{"scenario_path":"examples/vulnerable-agent/scenario.yml"}'`}</pre></div>
      </div>
    </>
  );
}

import type { Metadata } from "next";
import { Activity, FlaskConical, Shield, TerminalSquare } from "lucide-react";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgentLab",
  description: "DevTools and security testing for AI agents.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="sidebar">
            <div className="brand">AgentLab</div>
            <div className="tagline">Observe, control, attack, debug and replay agentic systems.</div>
            <nav className="nav" aria-label="Primary">
              <Link href="/"><Activity size={18} /> Dashboard</Link>
              <Link href="/traces"><TerminalSquare size={18} /> Traces</Link>
              <Link href="/security"><Shield size={18} /> Security</Link>
              <Link href="/attack-lab"><FlaskConical size={18} /> Attack Lab</Link>
            </nav>
          </aside>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}


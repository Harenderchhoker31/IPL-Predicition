import React from 'react';
import { useFetch } from '../hooks/useFetch';
import { teamColor } from '../constants';

const TAGS = ['Python','Node.js','React','Recharts','Scikit-learn','Random Forest','EDA','Generative AI'];

const INSIGHTS_L = [
  ['🏆', 'Mumbai Indians',  'Most wins — 151 across 18 seasons'],
  ['🏏', 'Virat Kohli',     'Top run scorer — 8,671 runs'],
  ['🎯', 'YS Chahal',       'Top wicket taker — 229 wickets'],
];
const INSIGHTS_R = [
  ['⭐', 'AB de Villiers',  'Most Player of Match — 25 awards'],
  ['🪙', '51.6%',           'Toss win → match win rate (near-random!)'],
  ['⚡', 'Death Overs',     'Highest run rate phase — decides matches'],
];

export default function Home() {
  const { data, loading, error } = useFetch('/api/analytics/overview');

  return (
    <div>
      <p className="hero-title">🏏 IPL Analytics Dashboard</p>
      <p className="hero-sub">Indian Premier League · 2008–2025 · 18 Seasons · Complete Ball-by-Ball Analysis</p>

      <div className="tags">
        {TAGS.map(t => <span key={t} className="tag">{t}</span>)}
      </div>

      <div className="kpi-grid">
        {[
          ['1,169',  'Total Matches',  '#f97316'],
          ['278K+',  'Deliveries',     '#3b82f6'],
          ['14',     'Teams',          '#22c55e'],
          ['18',     'Seasons',        '#a855f7'],
          ['8,671',  "Kohli's Runs",   '#f97316'],
        ].map(([val, lbl, color]) => (
          <div key={lbl} className="metric-card">
            <div className="metric-value" style={{ color }}>{val}</div>
            <div className="metric-label">{lbl}</div>
          </div>
        ))}
      </div>

      <p className="section-header">📌 Key Findings</p>
      <div className="col-grid-2" style={{ marginBottom: 24 }}>
        <div>{INSIGHTS_L.map(([e, b, t]) => (
          <div key={b} className="insight-box">{e} <b>{b}</b> — {t}</div>
        ))}</div>
        <div>{INSIGHTS_R.map(([e, b, t]) => (
          <div key={b} className="insight-box">{e} <b>{b}</b> — {t}</div>
        ))}</div>
      </div>

      <p className="section-header">🏆 IPL Champions Timeline</p>
      {loading && <div className="loading">Loading champions...</div>}
      {error   && <div className="error-msg">Error: {error}</div>}
      {data && (
        <div className="champions-grid">
          {data.champions.map(({ season, champion }) => {
            const color = teamColor(champion);
            return (
              <div key={season} className="champion-card" style={{ borderTop: `3px solid ${color}` }}>
                <div className="champion-year" style={{ color }}>{season}</div>
                <div className="champion-name">{champion}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

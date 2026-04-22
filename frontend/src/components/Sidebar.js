import React from 'react';

const PAGES = [
  { id: 'home',     label: '🏠 Home & Overview' },
  { id: 'teams',    label: '📊 Team Analysis' },
  { id: 'players',  label: '🏏 Player Analysis' },
  { id: 'insights', label: '⚡ Match Insights' },
  { id: 'predict',  label: '🤖 ML Prediction' },
  { id: 'h2h',      label: '🔍 Head-to-Head' },
];

export default function Sidebar({ page, setPage, seasons, fromSeason, toSeason, setFrom, setTo, matchCount, delivCount }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-title">🏏 IPL Analytics</div>
      <hr className="sidebar-divider" />

      {PAGES.map(p => (
        <button
          key={p.id}
          className={`nav-btn${page === p.id ? ' active' : ''}`}
          onClick={() => setPage(p.id)}
        >
          {p.label}
        </button>
      ))}

      <hr className="sidebar-divider" />

      <div className="season-filter">
        <label>📅 From Season</label>
        <select value={fromSeason} onChange={e => setFrom(Number(e.target.value))}>
          {seasons.map(s => <option key={s} value={s}>{s}</option>)}
        </select>
        <label>To Season</label>
        <select value={toSeason} onChange={e => setTo(Number(e.target.value))}>
          {seasons.filter(s => s >= fromSeason).map(s => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      <div className="sidebar-stats">
        📁 {matchCount?.toLocaleString()} matches<br />
        🎯 {delivCount?.toLocaleString()} deliveries<br />
        📅 {fromSeason} – {toSeason}
      </div>
    </aside>
  );
}

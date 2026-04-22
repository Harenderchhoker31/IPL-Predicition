import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  LineChart, Line, Area, AreaChart, Cell,
} from 'recharts';
import { useFetch } from '../hooks/useFetch';
import { teamColor, ACC1, ACC2, ACC3 } from '../constants';

const TABS = ['🏆 Win Records', '🔥 Season Heatmap', '📈 Season Trends'];

export default function Teams({ from, to }) {
  const [tab, setTab] = useState(0);
  const { data, loading, error } = useFetch(`/api/analytics/teams?from=${from}&to=${to}`);

  if (loading) return <div className="loading">Loading team data...</div>;
  if (error)   return <div className="error-msg">Error: {error}</div>;

  const winData = Object.entries(data.winCounts)
    .sort((a,b) => b[1]-a[1]).slice(0,12)
    .map(([team, wins]) => ({ team: team.replace(' ', '\n'), fullName: team, wins }));

  const seasonData = Object.entries(data.matchesPerSeason)
    .sort((a,b) => a[0]-b[0])
    .map(([season, matches]) => ({ season: Number(season), matches }));

  return (
    <div>
      <p className="section-header">📊 Team Analysis</p>
      <div className="tabs">
        {TABS.map((t, i) => (
          <button key={t} className={`tab-btn${tab===i?' active':''}`} onClick={() => setTab(i)}>{t}</button>
        ))}
      </div>

      {tab === 0 && (
        <div className="col-grid-2">
          <div className="chart-box">
            <div className="chart-title">Most Wins by Team</div>
            <ResponsiveContainer width="100%" height={340}>
              <BarChart data={winData} layout="vertical" margin={{ left: 120, right: 40 }}>
                <XAxis type="number" tick={{ fill: '#8b949e', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="fullName" tick={{ fill: '#e6edf3', fontSize: 11 }} width={120} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} labelStyle={{ color: '#e6edf3' }} itemStyle={{ color: '#f97316' }} />
                <Bar dataKey="wins" radius={[0,4,4,0]}>
                  {winData.map(d => <Cell key={d.fullName} fill={teamColor(d.fullName)} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div>
            <div className="chart-title" style={{ marginBottom: 8 }}>🥇 Win Table</div>
            <table className="data-table">
              <thead><tr><th>#</th><th>Team</th><th>Wins</th></tr></thead>
              <tbody>
                {Object.entries(data.winCounts).sort((a,b)=>b[1]-a[1]).slice(0,12).map(([team, wins], i) => (
                  <tr key={team}>
                    <td style={{ color: '#8b949e' }}>{i+1}</td>
                    <td><span style={{ color: teamColor(team), fontWeight: 700 }}>●</span> {team}</td>
                    <td style={{ fontWeight: 700 }}>{wins}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === 1 && (
        <div className="chart-box">
          <div className="chart-title">Win % Heatmap — Top 6 Teams by Season</div>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table" style={{ minWidth: 700 }}>
              <thead>
                <tr>
                  <th>Team</th>
                  {Object.keys(data.heatmap[data.top6[0]] || {}).sort().map(s => <th key={s}>{s}</th>)}
                </tr>
              </thead>
              <tbody>
                {data.top6.map(team => (
                  <tr key={team}>
                    <td style={{ color: teamColor(team), fontWeight: 700 }}>{team}</td>
                    {Object.entries(data.heatmap[team] || {}).sort((a,b)=>a[0]-b[0]).map(([s, pct]) => {
                      const intensity = pct / 100;
                      const bg = pct === 0 ? '#161b22' : `rgba(249,115,22,${0.15 + intensity * 0.75})`;
                      return <td key={s} style={{ background: bg, textAlign: 'center', fontWeight: pct > 0 ? 600 : 400, color: pct > 50 ? '#fff' : '#e6edf3' }}>{pct > 0 ? `${pct}%` : '—'}</td>;
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p style={{ color: '#8b949e', fontSize: '0.78rem', marginTop: 8 }}>💡 — = team didn't participate that season</p>
        </div>
      )}

      {tab === 2 && (
        <div className="col-grid-2">
          <div className="chart-box">
            <div className="chart-title">Matches Per Season</div>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={seasonData}>
                <defs>
                  <linearGradient id="gm" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor={ACC2} stopOpacity={0.3} />
                    <stop offset="95%" stopColor={ACC2} stopOpacity={0} />
                  </linearGradient>
                </defs>
                <XAxis dataKey="season" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} labelStyle={{ color: '#e6edf3' }} itemStyle={{ color: ACC2 }} />
                <Area type="monotone" dataKey="matches" stroke={ACC2} fill="url(#gm)" strokeWidth={2} dot={{ fill: ACC2, r: 3 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-box">
            <div className="chart-title">Total Runs Per Season</div>
            <ResponsiveContainer width="100%" height={220}>
              <AreaChart data={seasonData.map(d => ({ ...d, runs: 0 }))}>
                <XAxis dataKey="season" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} />
              </AreaChart>
            </ResponsiveContainer>
            <p style={{ color: '#8b949e', fontSize: '0.78rem', textAlign: 'center', marginTop: 8 }}>
              (Runs per season available via insights endpoint)
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

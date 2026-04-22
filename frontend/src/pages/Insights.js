import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  PieChart, Pie, Legend,
} from 'recharts';
import { useFetch } from '../hooks/useFetch';
import { teamColor, ACC1, ACC2, ACC3, ACC4 } from '../constants';

const TABS = ['🪙 Toss Analysis', '📍 Venues', '🏟️ Phase Analysis'];

export default function Insights({ from, to }) {
  const [tab, setTab] = useState(0);
  const { data, loading, error } = useFetch(`/api/analytics/insights?from=${from}&to=${to}`);

  if (loading) return <div className="loading">Loading insights...</div>;
  if (error)   return <div className="error-msg">Error: {error}</div>;

  return (
    <div>
      <p className="section-header">⚡ Match Insights</p>
      <div className="tabs">
        {TABS.map((t, i) => (
          <button key={t} className={`tab-btn${tab===i?' active':''}`} onClick={() => setTab(i)}>{t}</button>
        ))}
      </div>

      {tab === 0 && (
        <div>
          <div className="col-grid-3" style={{ marginBottom: 20 }}>
            {[
              [data.tossWinPct + '%', 'Toss Win → Match Win', ACC1],
              [data.fieldPct + '%',   'Choose to Field First', ACC2],
              [(100 - data.fieldPct).toFixed(1) + '%', 'Choose to Bat First', ACC3],
            ].map(([val, lbl, color]) => (
              <div key={lbl} className="metric-card">
                <div className="metric-value" style={{ color }}>{val}</div>
                <div className="metric-label">{lbl}</div>
              </div>
            ))}
          </div>

          <div className="col-grid-2">
            <div className="chart-box">
              <div className="chart-title">Toss Win → Match Win?</div>
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Won Match', value: data.tossWinPct },
                      { name: 'Lost Match', value: 100 - data.tossWinPct },
                    ]}
                    cx="50%" cy="50%" outerRadius={90}
                    dataKey="value" label={({ name, value }) => `${name}: ${value}%`}
                    labelLine={false}
                  >
                    <Cell fill={ACC1} />
                    <Cell fill="#30363d" />
                  </Pie>
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="chart-box">
              <div className="chart-title">Toss Win Rate by Team</div>
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={data.tossWinByTeam} layout="vertical" margin={{ left: 140, right: 40 }}>
                  <XAxis type="number" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} domain={[0, 100]} />
                  <YAxis type="category" dataKey="team" tick={{ fill: '#e6edf3', fontSize: 10 }} width={140} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC2 }} formatter={v => `${v}%`} />
                  <Bar dataKey="pct" radius={[0,4,4,0]}>
                    {data.tossWinByTeam.map(d => <Cell key={d.team} fill={teamColor(d.team)} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {tab === 1 && (
        <div className="col-grid-2">
          <div className="chart-box">
            <div className="chart-title">Top Venues by Matches Hosted</div>
            <ResponsiveContainer width="100%" height={340}>
              <BarChart data={data.topVenues} layout="vertical" margin={{ left: 180, right: 40 }}>
                <XAxis type="number" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="venue" tick={{ fill: '#e6edf3', fontSize: 10 }} width={180} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC4 }} />
                <Bar dataKey="matches" fill={ACC4} radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div>
            <div className="chart-title" style={{ marginBottom: 8 }}>Venue Table</div>
            <table className="data-table">
              <thead><tr><th>#</th><th>Venue</th><th>Matches</th></tr></thead>
              <tbody>
                {data.topVenues.map((v, i) => (
                  <tr key={v.venue}>
                    <td style={{ color: '#8b949e' }}>{i+1}</td>
                    <td>{v.venue.slice(0, 35)}</td>
                    <td style={{ color: ACC4, fontWeight: 700 }}>{v.matches}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {tab === 2 && (
        <div>
          <div className="col-grid-2" style={{ marginBottom: 20 }}>
            <div className="chart-box">
              <div className="chart-title">Avg Runs per Ball by Phase</div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={data.phaseData}>
                  <XAxis dataKey="phase" tick={{ fill: '#e6edf3', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC3 }} />
                  <Bar dataKey="avgRuns" radius={[4,4,0,0]}>
                    <Cell fill={ACC3} /><Cell fill={ACC2} /><Cell fill={ACC1} />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="chart-box">
              <div className="chart-title">Total Wickets by Phase</div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={data.phaseData}>
                  <XAxis dataKey="phase" tick={{ fill: '#e6edf3', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC1 }} />
                  <Bar dataKey="wickets" radius={[4,4,0,0]}>
                    <Cell fill={ACC3} /><Cell fill={ACC2} /><Cell fill={ACC1} />
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="chart-box">
            <div className="chart-title">🏏 Dismissal Types Distribution</div>
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.dismissals} margin={{ bottom: 40 }}>
                <XAxis dataKey="type" tick={{ fill: '#e6edf3', fontSize: 10 }} angle={-20} textAnchor="end" interval={0} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC2 }} />
                <Bar dataKey="count" radius={[4,4,0,0]}>
                  {data.dismissals.map((_, i) => <Cell key={i} fill={`hsl(${200 + i * 20}, 65%, 55%)`} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

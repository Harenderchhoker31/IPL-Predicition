import React, { useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts';
import { useFetch } from '../hooks/useFetch';
import { teamColor, ACC1, ACC2 } from '../constants';

export default function H2H({ from, to }) {
  const { data: meta } = useFetch('/api/analytics/teams/list');
  const teams = meta?.teams || [];

  const [t1, setT1] = useState('');
  const [t2, setT2] = useState('');

  const t2Opts = teams.filter(t => t !== t1);
  const url = t1 && t2 ? `/api/analytics/h2h?team1=${encodeURIComponent(t1)}&team2=${encodeURIComponent(t2)}&from=${from}&to=${to}` : null;
  const { data, loading, error } = useFetch(url);

  const seasonData = data
    ? Object.entries(data.seasonWins).sort((a,b) => a[0]-b[0]).map(([season, wins]) => ({
        season: Number(season),
        [t1]: wins[t1] || 0,
        [t2]: wins[t2] || 0,
      }))
    : [];

  return (
    <div>
      <p className="section-header">🔍 Head-to-Head Analysis</p>

      <div className="col-grid-2" style={{ marginBottom: 20 }}>
        <div className="form-group">
          <label>Team 1</label>
          <select value={t1} onChange={e => { setT1(e.target.value); setT2(''); }}>
            <option value="">Select team...</option>
            {teams.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
        <div className="form-group">
          <label>Team 2</label>
          <select value={t2} onChange={e => setT2(e.target.value)}>
            <option value="">Select team...</option>
            {t2Opts.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </div>
      </div>

      {loading && <div className="loading">Loading head-to-head data...</div>}
      {error   && <div className="error-msg">Error: {error}</div>}

      {data && data.total === 0 && (
        <div className="insight-box">⚠️ No matches found between these teams in the selected season range.</div>
      )}

      {data && data.total > 0 && (
        <div>
          <div className="col-grid-3" style={{ marginBottom: 20 }}>
            <div className="metric-card">
              <div className="metric-value" style={{ color: teamColor(t1) }}>{data.t1Wins}</div>
              <div className="metric-label">{t1.slice(0,20)} Wins</div>
            </div>
            <div className="metric-card">
              <div className="metric-value" style={{ color: '#8b949e' }}>{data.total}</div>
              <div className="metric-label">Total Matches</div>
            </div>
            <div className="metric-card">
              <div className="metric-value" style={{ color: teamColor(t2) }}>{data.t2Wins}</div>
              <div className="metric-label">{t2.slice(0,20)} Wins</div>
            </div>
          </div>

          <div className="col-grid-2" style={{ marginBottom: 20 }}>
            <div className="chart-box">
              <div className="chart-title">Head-to-Head Win Share</div>
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie
                    data={[
                      { name: t1, value: data.t1Wins },
                      { name: t2, value: data.t2Wins },
                    ]}
                    cx="50%" cy="50%" outerRadius={85}
                    dataKey="value"
                    label={({ name, value }) => `${name.split(' ')[0]}: ${value}`}
                  >
                    <Cell fill={teamColor(t1)} />
                    <Cell fill={teamColor(t2)} />
                  </Pie>
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div>
              <div className="chart-title" style={{ marginBottom: 8 }}>📋 Match History</div>
              <table className="data-table">
                <thead><tr><th>Season</th><th>Winner</th><th>By Runs</th><th>By Wkts</th></tr></thead>
                <tbody>
                  {data.history.slice(0, 15).map((m, i) => (
                    <tr key={i}>
                      <td>{m.season}</td>
                      <td style={{ color: teamColor(m.winner), fontWeight: 700 }}>{m.winner}</td>
                      <td>{m.byRuns || '—'}</td>
                      <td>{m.byWickets || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {seasonData.length > 0 && (
            <div className="chart-box">
              <div className="chart-title">📅 Season-wise Results</div>
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={seasonData}>
                  <XAxis dataKey="season" tick={{ fill: '#e6edf3', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} allowDecimals={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} />
                  <Bar dataKey={t1} fill={teamColor(t1)} radius={[4,4,0,0]} />
                  <Bar dataKey={t2} fill={teamColor(t2)} radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

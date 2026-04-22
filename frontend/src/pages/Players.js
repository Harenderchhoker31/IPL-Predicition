import React, { useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
} from 'recharts';
import { useFetch } from '../hooks/useFetch';
import { ACC1, ACC2, ACC3, ACC4 } from '../constants';

const TABS = ['🏏 Batsmen', '🎯 Bowlers', '⭐ Player of Match'];

export default function Players({ from, to }) {
  const [tab, setTab] = useState(0);
  const [topN, setTopN] = useState(10);
  const { data, loading, error } = useFetch(`/api/analytics/players?from=${from}&to=${to}`);

  if (loading) return <div className="loading">Loading player data...</div>;
  if (error)   return <div className="error-msg">Error: {error}</div>;

  const batData  = data.topBatsmen.slice(0, topN);
  const bowlData = data.topBowlers.slice(0, topN);

  return (
    <div>
      <p className="section-header">🏏 Player Analysis</p>
      <div className="tabs">
        {TABS.map((t, i) => (
          <button key={t} className={`tab-btn${tab===i?' active':''}`} onClick={() => setTab(i)}>{t}</button>
        ))}
      </div>

      {tab === 0 && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <label style={{ color: '#8b949e', fontSize: '0.85rem' }}>Top N:</label>
            <input type="range" min={5} max={20} value={topN} onChange={e => setTopN(Number(e.target.value))} style={{ accentColor: ACC1 }} />
            <span style={{ color: '#f97316', fontWeight: 700 }}>{topN}</span>
          </div>
          <div className="col-grid-2">
            <div className="chart-box">
              <div className="chart-title">Top {topN} Run Scorers</div>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={batData} margin={{ bottom: 60 }}>
                  <XAxis dataKey="name" tick={{ fill: '#e6edf3', fontSize: 9 }} angle={-30} textAnchor="end" interval={0} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} labelStyle={{ color: '#e6edf3' }} itemStyle={{ color: ACC1 }} />
                  <Bar dataKey="runs" radius={[4,4,0,0]}>
                    {batData.map((_, i) => <Cell key={i} fill={`hsl(${25 + i * 4}, 90%, ${55 - i * 1.5}%)`} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div>
              <div className="chart-title" style={{ marginBottom: 8 }}>Run Scorers Table</div>
              <table className="data-table">
                <thead><tr><th>#</th><th>Batsman</th><th>Runs</th><th>Balls</th></tr></thead>
                <tbody>
                  {batData.map((p, i) => (
                    <tr key={p.name}>
                      <td style={{ color: '#8b949e' }}>{i+1}</td>
                      <td>{p.name}</td>
                      <td style={{ color: ACC1, fontWeight: 700 }}>{p.runs.toLocaleString()}</td>
                      <td style={{ color: '#8b949e' }}>{p.balls.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <p className="section-header" style={{ fontSize: '1rem', marginTop: 24 }}>⚡ Highest Strike Rate (min 200 balls)</p>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.strikeRates} layout="vertical" margin={{ left: 130, right: 50 }}>
                <XAxis type="number" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fill: '#e6edf3', fontSize: 11 }} width={130} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC4 }} />
                <Bar dataKey="sr" fill={ACC4} radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {tab === 1 && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 16 }}>
            <label style={{ color: '#8b949e', fontSize: '0.85rem' }}>Top N:</label>
            <input type="range" min={5} max={20} value={topN} onChange={e => setTopN(Number(e.target.value))} style={{ accentColor: ACC2 }} />
            <span style={{ color: ACC2, fontWeight: 700 }}>{topN}</span>
          </div>
          <div className="col-grid-2">
            <div className="chart-box">
              <div className="chart-title">Top {topN} Wicket Takers</div>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={bowlData} margin={{ bottom: 60 }}>
                  <XAxis dataKey="name" tick={{ fill: '#e6edf3', fontSize: 9 }} angle={-30} textAnchor="end" interval={0} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC2 }} />
                  <Bar dataKey="wickets" fill={ACC2} radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div>
              <div className="chart-title" style={{ marginBottom: 8 }}>Wicket Takers Table</div>
              <table className="data-table">
                <thead><tr><th>#</th><th>Bowler</th><th>Wickets</th></tr></thead>
                <tbody>
                  {bowlData.map((p, i) => (
                    <tr key={p.name}>
                      <td style={{ color: '#8b949e' }}>{i+1}</td>
                      <td>{p.name}</td>
                      <td style={{ color: ACC2, fontWeight: 700 }}>{p.wickets}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <p className="section-header" style={{ fontSize: '1rem', marginTop: 24 }}>💰 Best Economy Rate (min 120 balls)</p>
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={data.economy} layout="vertical" margin={{ left: 130, right: 50 }}>
                <XAxis type="number" tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
                <YAxis type="category" dataKey="name" tick={{ fill: '#e6edf3', fontSize: 11 }} width={130} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC3 }} />
                <Bar dataKey="economy" fill={ACC3} radius={[0,4,4,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {tab === 2 && (
        <div className="chart-box">
          <div className="chart-title">Most Player of the Match Awards</div>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={data.topPom} margin={{ bottom: 60 }}>
              <XAxis dataKey="name" tick={{ fill: '#e6edf3', fontSize: 9 }} angle={-30} textAnchor="end" interval={0} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#8b949e', fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip contentStyle={{ background: '#161b22', border: '1px solid #30363d', borderRadius: 8 }} itemStyle={{ color: ACC1 }} />
              <Bar dataKey="awards" radius={[4,4,0,0]}>
                {data.topPom.map((_, i) => <Cell key={i} fill={`hsl(${270 + i * 6}, 70%, ${55 - i}%)`} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

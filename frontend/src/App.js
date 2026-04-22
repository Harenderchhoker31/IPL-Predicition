import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Home     from './pages/Home';
import Teams    from './pages/Teams';
import Players  from './pages/Players';
import Insights from './pages/Insights';
import Predict  from './pages/Predict';
import H2H      from './pages/H2H';

export default function App() {
  const [page, setPage]       = useState('home');
  const [seasons, setSeasons] = useState([2008, 2025]);
  const [from, setFrom]       = useState(2008);
  const [to, setTo]           = useState(2025);
  const [stats, setStats]     = useState({ matches: 0, deliveries: 0 });

  useEffect(() => {
    fetch('/api/analytics/teams/list')
      .then(r => r.json())
      .then(d => {
        if (d.seasons?.length) {
          setSeasons(d.seasons);
          setFrom(d.seasons[0]);
          setTo(d.seasons[d.seasons.length - 1]);
        }
      })
      .catch(() => {});

    fetch('/api/analytics/overview')
      .then(r => r.json())
      .then(d => setStats({ matches: d.totalMatches, deliveries: d.totalDeliveries }))
      .catch(() => {});
  }, []);

  const pages = { home: <Home />, teams: <Teams from={from} to={to} />, players: <Players from={from} to={to} />, insights: <Insights from={from} to={to} />, predict: <Predict />, h2h: <H2H from={from} to={to} /> };

  return (
    <div className="app-layout">
      <Sidebar
        page={page} setPage={setPage}
        seasons={seasons}
        fromSeason={from} toSeason={to}
        setFrom={setFrom} setTo={setTo}
        matchCount={stats.matches}
        delivCount={stats.deliveries}
      />
      <main className="main-content">
        {pages[page]}
        <footer className="footer">
          🏏 IPL Analytics Dashboard &nbsp;|&nbsp; Built with React · Node.js · Python · Scikit-learn
          &nbsp;|&nbsp; Dataset: Kaggle IPL 2008–2025 &nbsp;|&nbsp; <b>Placement Project</b>
        </footer>
      </main>
    </div>
  );
}

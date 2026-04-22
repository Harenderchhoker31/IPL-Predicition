const router = require('express').Router();
const { getDb } = require('../dataLoader');

// Helper: group & count
function countBy(arr, key) {
  return arr.reduce((acc, row) => {
    const k = row[key];
    if (k) acc[k] = (acc[k] || 0) + 1;
    return acc;
  }, {});
}

function sumBy(arr, key) {
  return arr.reduce((acc, row) => acc + (Number(row[key]) || 0), 0);
}

// GET /api/analytics/overview
router.get('/overview', (req, res) => {
  const { matches, deliv, valid, finals } = getDb();
  const seasons = [...new Set(matches.map(m => m.season))].sort();
  const finalsIds = new Set(finals.map(f => f.id));
  const champions = valid
    .filter(m => finalsIds.has(m.match_id))
    .map(m => ({ season: m.season, champion: m.match_winner }))
    .sort((a, b) => a.season - b.season);

  res.json({
    totalMatches: matches.length,
    totalDeliveries: deliv.length,
    seasons: seasons.length,
    seasonRange: [seasons[0], seasons[seasons.length - 1]],
    champions,
  });
});

// GET /api/analytics/teams?from=2008&to=2025
router.get('/teams', (req, res) => {
  const { matches, valid } = getDb();
  const from = Number(req.query.from) || 2008;
  const to   = Number(req.query.to)   || 2025;

  const fValid = valid.filter(m => m.season >= from && m.season <= to);
  const fAll   = matches.filter(m => m.season >= from && m.season <= to);

  // Win counts
  const winCounts = countBy(fValid, 'match_winner');

  // Matches per season
  const matchesPerSeason = {};
  fAll.forEach(m => { matchesPerSeason[m.season] = (matchesPerSeason[m.season] || 0) + 1; });

  // Win % heatmap for top 6 teams
  const top6 = Object.entries(winCounts).sort((a,b) => b[1]-a[1]).slice(0,6).map(e => e[0]);
  const heatmap = {};
  top6.forEach(team => {
    heatmap[team] = {};
    const seasons = [...new Set(fAll.map(m => m.season))].sort();
    seasons.forEach(s => {
      const played = fAll.filter(m => m.season === s && (m.team1 === team || m.team2 === team)).length;
      const won    = fValid.filter(m => m.season === s && m.match_winner === team).length;
      heatmap[team][s] = played > 0 ? Math.round(won / played * 100) : 0;
    });
  });

  res.json({ winCounts, matchesPerSeason, heatmap, top6 });
});

// GET /api/analytics/players?from=2008&to=2025
router.get('/players', (req, res) => {
  const { deliv, matches } = getDb();
  const from = Number(req.query.from) || 2008;
  const to   = Number(req.query.to)   || 2025;

  const fd = deliv.filter(d => d.season_id >= from && d.season_id <= to);

  // Top batsmen by runs
  const runMap = {};
  const ballMap = {};
  fd.forEach(d => {
    runMap[d.batter]  = (runMap[d.batter]  || 0) + (Number(d.batter_runs) || 0);
    ballMap[d.batter] = (ballMap[d.batter] || 0) + 1;
  });
  const topBatsmen = Object.entries(runMap)
    .sort((a,b) => b[1]-a[1]).slice(0,20)
    .map(([name, runs]) => ({ name, runs, balls: ballMap[name] || 0 }));

  // Strike rates (min 200 balls)
  const strikeRates = Object.entries(runMap)
    .filter(([name]) => (ballMap[name] || 0) >= 200)
    .map(([name, runs]) => ({ name, sr: Math.round(runs / ballMap[name] * 100 * 10) / 10 }))
    .sort((a,b) => b.sr - a.sr).slice(0, 10);

  // Top bowlers by wickets
  const wicketMap = {};
  const bowlerBalls = {};
  const bowlerRuns = {};
  fd.forEach(d => {
    bowlerBalls[d.bowler] = (bowlerBalls[d.bowler] || 0) + 1;
    bowlerRuns[d.bowler]  = (bowlerRuns[d.bowler]  || 0) + (Number(d.total_runs) || 0);
    if (d.is_wicket) wicketMap[d.bowler] = (wicketMap[d.bowler] || 0) + 1;
  });
  const topBowlers = Object.entries(wicketMap)
    .sort((a,b) => b[1]-a[1]).slice(0,20)
    .map(([name, wickets]) => ({ name, wickets }));

  // Economy rates (min 120 balls)
  const economy = Object.entries(bowlerBalls)
    .filter(([, balls]) => balls >= 120)
    .map(([name, balls]) => ({
      name,
      economy: Math.round(bowlerRuns[name] / (balls / 6) * 100) / 100,
    }))
    .sort((a,b) => a.economy - b.economy).slice(0, 10);

  // Player of match
  const fm = matches.filter(m => m.season >= from && m.season <= to);
  const pomCounts = countBy(fm, 'pom_name');
  const topPom = Object.entries(pomCounts)
    .filter(([k]) => k && k !== 'null')
    .sort((a,b) => b[1]-a[1]).slice(0,15)
    .map(([name, awards]) => ({ name, awards }));

  res.json({ topBatsmen, strikeRates, topBowlers, economy, topPom });
});

// GET /api/analytics/insights?from=2008&to=2025
router.get('/insights', (req, res) => {
  const { matches, deliv, valid } = getDb();
  const from = Number(req.query.from) || 2008;
  const to   = Number(req.query.to)   || 2025;

  const fValid = valid.filter(m => m.season >= from && m.season <= to);
  const fAll   = matches.filter(m => m.season >= from && m.season <= to);
  const fd     = deliv.filter(d => d.season_id >= from && d.season_id <= to);

  // Toss analysis
  const tossWinMatchWin = fValid.filter(m => m.toss_winner === m.match_winner).length;
  const tossWinPct = Math.round(tossWinMatchWin / fValid.length * 1000) / 10;
  const fieldPct   = Math.round(fAll.filter(m => m.toss_decision === 'field').length / fAll.length * 1000) / 10;

  // Toss win rate by team
  const tossTeams = {};
  fValid.forEach(m => {
    if (!tossTeams[m.toss_winner]) tossTeams[m.toss_winner] = { won: 0, total: 0 };
    tossTeams[m.toss_winner].total++;
    if (m.toss_winner === m.match_winner) tossTeams[m.toss_winner].won++;
  });
  const tossWinByTeam = Object.entries(tossTeams)
    .map(([team, { won, total }]) => ({ team, pct: Math.round(won / total * 1000) / 10 }))
    .sort((a,b) => b.pct - a.pct).slice(0, 10);

  // Venues
  const venueCounts = countBy(fAll, 'venue');
  const topVenues = Object.entries(venueCounts)
    .sort((a,b) => b[1]-a[1]).slice(0,12)
    .map(([venue, matches]) => ({ venue, matches }));

  // Phase analysis
  const phases = ['Powerplay (1-6)', 'Middle (7-15)', 'Death (16-20)'];
  const phaseRuns = {}, phaseWkts = {}, phaseBalls = {};
  phases.forEach(p => { phaseRuns[p] = 0; phaseWkts[p] = 0; phaseBalls[p] = 0; });
  fd.forEach(d => {
    if (phases.includes(d.phase)) {
      phaseRuns[d.phase]  += Number(d.total_runs) || 0;
      phaseBalls[d.phase] += 1;
      if (d.is_wicket) phaseWkts[d.phase]++;
    }
  });
  const phaseData = phases.map(p => ({
    phase: p,
    avgRuns: phaseBalls[p] > 0 ? Math.round(phaseRuns[p] / phaseBalls[p] * 1000) / 1000 : 0,
    wickets: phaseWkts[p],
  }));

  // Dismissal types
  const dismissalMap = {};
  fd.filter(d => d.is_wicket).forEach(d => {
    dismissalMap[d.wicket_kind] = (dismissalMap[d.wicket_kind] || 0) + 1;
  });
  const dismissals = Object.entries(dismissalMap)
    .sort((a,b) => b[1]-a[1])
    .map(([type, count]) => ({ type, count }));

  // Runs per season
  const runsPerSeason = {};
  fd.forEach(d => {
    runsPerSeason[d.season_id] = (runsPerSeason[d.season_id] || 0) + (Number(d.total_runs) || 0);
  });

  res.json({ tossWinPct, fieldPct, tossWinByTeam, topVenues, phaseData, dismissals, runsPerSeason });
});

// GET /api/analytics/h2h?team1=X&team2=Y&from=2008&to=2025
router.get('/h2h', (req, res) => {
  const { matches, valid } = getDb();
  const { team1, team2 } = req.query;
  const from = Number(req.query.from) || 2008;
  const to   = Number(req.query.to)   || 2025;

  if (!team1 || !team2) return res.status(400).json({ error: 'team1 and team2 required' });

  const h2h = matches.filter(m =>
    m.season >= from && m.season <= to &&
    ((m.team1 === team1 && m.team2 === team2) || (m.team1 === team2 && m.team2 === team1))
  );
  const h2hValid = h2h.filter(m => m.result === 'win');

  const t1Wins = h2hValid.filter(m => m.match_winner === team1).length;
  const t2Wins = h2hValid.filter(m => m.match_winner === team2).length;

  // Season-wise
  const seasonWins = {};
  h2hValid.forEach(m => {
    if (!seasonWins[m.season]) seasonWins[m.season] = { [team1]: 0, [team2]: 0 };
    seasonWins[m.season][m.match_winner] = (seasonWins[m.season][m.match_winner] || 0) + 1;
  });

  const history = h2hValid
    .map(m => ({ season: m.season, winner: m.match_winner, byRuns: m.win_by_runs, byWickets: m.win_by_wickets }))
    .sort((a,b) => b.season - a.season);

  res.json({ total: h2h.length, t1Wins, t2Wins, seasonWins, history });
});

// GET /api/analytics/teams/list
router.get('/teams/list', (req, res) => {
  const { valid, matches } = getDb();
  const teams = [...new Set(valid.map(m => m.match_winner).filter(Boolean))].sort();
  const venues = [...new Set(matches.map(m => m.venue).filter(Boolean))].sort();
  const seasons = [...new Set(matches.map(m => m.season))].sort();
  res.json({ teams, venues, seasons });
});

module.exports = router;

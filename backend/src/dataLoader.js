const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

const DATA_DIR = path.join(__dirname, '../../data');

const db = {};

function readCsv(filename) {
  const content = fs.readFileSync(path.join(DATA_DIR, filename), 'utf8');
  return parse(content, { columns: true, skip_empty_lines: true, cast: true });
}

async function loadAllData() {
  const teams   = readCsv('all_teams_data.csv');
  const players = readCsv('all_players-data-updated.csv');
  const finals  = readCsv('IPL_finals.csv');

  const tMap = Object.fromEntries(teams.map(t => [t.team_id, t.team_name]));
  const pMap = Object.fromEntries(players.map(p => [p.player_id, p.player_name]));

  const matches = readCsv('all_ipl_matches_data.csv').map(m => ({
    ...m,
    team1:        tMap[m.team1]        ?? m.team1,
    team2:        tMap[m.team2]        ?? m.team2,
    toss_winner:  tMap[m.toss_winner]  ?? m.toss_winner,
    match_winner: tMap[m.match_winner] ?? m.match_winner,
    pom_name:     pMap[m.player_of_match] ?? null,
    season:       parseInt(String(m.season).replace('/21', '')),
  }));

  const deliv = readCsv('all_ball_by_ball_data.csv').map(d => ({
    ...d,
    team_batting: tMap[d.team_batting] ?? d.team_batting,
    team_bowling: tMap[d.team_bowling] ?? d.team_bowling,
    season_id:    parseInt(String(d.season_id).replace('/21', '')),
    phase: d.over_number < 6 ? 'Powerplay (1-6)'
         : d.over_number < 15 ? 'Middle (7-15)'
         : 'Death (16-20)',
  }));

  db.matches  = matches;
  db.deliv    = deliv;
  db.teams    = teams;
  db.players  = players;
  db.finals   = finals;
  db.tMap     = tMap;
  db.pMap     = pMap;
  db.valid    = matches.filter(m => m.result === 'win');

  console.log(`Loaded: ${matches.length} matches, ${deliv.length} deliveries`);
}

function getDb() { return db; }

module.exports = { loadAllData, getDb };

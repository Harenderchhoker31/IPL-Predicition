export const TEAM_COLORS = {
  'Mumbai Indians':              '#004BA0',
  'Chennai Super Kings':         '#F4C430',
  'Kolkata Knight Riders':       '#3A225D',
  'Royal Challengers Bangalore': '#EC1C24',
  'Royal Challengers Bengaluru': '#EC1C24',
  'Sunrisers Hyderabad':         '#FF822A',
  'Punjab Kings':                '#AA4545',
  'Kings XI Punjab':             '#AA4545',
  'Delhi Capitals':              '#0078BC',
  'Delhi Daredevils':            '#0078BC',
  'Rajasthan Royals':            '#2D68C4',
  'Gujarat Titans':              '#1C4B9C',
  'Lucknow Super Giants':        '#00A86B',
  'Deccan Chargers':             '#FDB913',
  'Rising Pune Supergiant':      '#6F1D78',
  'Rising Pune Supergiants':     '#6F1D78',
  'Gujarat Lions':               '#E8461A',
  'Kochi Tuskers Kerala':        '#F26522',
  'Pune Warriors':               '#1C4B9C',
};

export const ACC1 = '#f97316';
export const ACC2 = '#3b82f6';
export const ACC3 = '#22c55e';
export const ACC4 = '#a855f7';

export function teamColor(name) {
  return TEAM_COLORS[name] || ACC1;
}

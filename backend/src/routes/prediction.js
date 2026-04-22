const router = require('express').Router();
const { spawn } = require('child_process');
const path = require('path');

// POST /api/predict
router.post('/', (req, res) => {
  const { team1, team2, tossWinner, tossDecision, venue, season } = req.body;
  if (!team1 || !team2 || !tossWinner || !tossDecision || !venue || !season) {
    return res.status(400).json({ error: 'All fields required' });
  }

  const scriptPath = path.join(__dirname, '../../predict.py');
  const input = JSON.stringify({ team1, team2, tossWinner, tossDecision, venue, season });

  const py = spawn('python3', [scriptPath, input]);
  let output = '';
  let errOut = '';

  py.stdout.on('data', d => { output += d.toString(); });
  py.stderr.on('data', d => { errOut += d.toString(); });

  py.on('close', code => {
    if (code !== 0) return res.status(500).json({ error: errOut || 'Prediction failed' });
    try {
      res.json(JSON.parse(output));
    } catch {
      res.status(500).json({ error: 'Invalid prediction output' });
    }
  });
});

module.exports = router;

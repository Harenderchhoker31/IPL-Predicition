const express = require('express');
const cors = require('cors');
const { loadAllData } = require('./dataLoader');
const analyticsRouter = require('./routes/analytics');
const predictionRouter = require('./routes/prediction');

const app = express();
app.use(cors());
app.use(express.json());

// Load all CSV data once at startup
loadAllData().then(() => {
  app.use('/api/analytics', analyticsRouter);
  app.use('/api/predict', predictionRouter);

  app.get('/api/health', (_, res) => res.json({ status: 'ok' }));

  const PORT = process.env.PORT || 5000;
  app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
}).catch(err => {
  console.error('Failed to load data:', err);
  process.exit(1);
});

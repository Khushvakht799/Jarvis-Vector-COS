import express from 'express';
import cors from 'cors';
import { config } from 'dotenv';
import apiRoutes from './routes/api.js';  // Добавь .js

config();

const app = express();
const PORT = process.env.API_PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api', apiRoutes);

// Health check
app.get('/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        service: 'Jarvis API',
        timestamp: new Date().toISOString()
    });
});

// Error handling
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
    console.error('Error:', err);
    res.status(500).json({ error: 'Internal Server Error' });
});

app.listen(PORT, () => {
    console.log(`🚀 Jarvis API server running on port ${PORT}`);
});

export default app;
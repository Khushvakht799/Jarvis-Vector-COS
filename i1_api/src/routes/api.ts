import { Router } from 'express';
import { queryController } from '../controllers/queryController.js';  // Добавь .js

const router = Router();

router.post('/query', queryController);
router.get('/status', (req, res) => {
    res.json({ status: 'active', service: 'Jarvis Vector COS' });
});

export default router;
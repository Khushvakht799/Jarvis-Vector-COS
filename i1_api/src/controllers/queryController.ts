import { Request, Response } from 'express';

export const queryController = async (req: Request, res: Response) => {
    try {
        const { prompt } = req.body;
        
        console.log('🔵 API received prompt:', prompt);
        console.log('🔵 Full request body:', req.body);
        
        if (!prompt) {
            console.log('❌ No prompt received');
            return res.status(400).json({ error: 'Prompt is required' });
        }

        try {
            // Send request to Go service
            console.log('🔄 Sending request to Go service...');
            const goResponse = await fetch('http://localhost:8081/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: prompt })
            });

            console.log('📡 Go service response status:', goResponse.status);

            if (!goResponse.ok) {
                throw new Error(`Go service error: ${goResponse.status}`);
            }

            const goData = await goResponse.json();
            console.log('✅ Go service response:', goData);

            // Success response with Go data
            const response = {
                ...goData,
                apiService: 'Node.js API',
                fullService: 'Jarvis AI Platform',
                integrated: true
            };

            res.json(response);

        } catch (goError) {
            console.error('❌ Go service integration failed:', goError);
            
            // Fallback - respond without Go service
            const fallbackResponse = {
                answer: "API received: " + prompt + " (Go service unavailable)",
                prompt: prompt,
                timestamp: new Date().toISOString(),
                service: "Node.js API (Standalone)",
                integrated: false,
                error: "Go service connection failed"
            };
            
            res.json(fallbackResponse);
        }

    } catch (error) {
        console.error('💥 Query controller error:', error);
        res.status(500).json({ 
            error: 'Internal server error'
        });
    }
};
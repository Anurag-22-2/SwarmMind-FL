const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const mongoose = require('mongoose');

const app = express();
app.use(cors({ origin: '*' }));
app.use(express.json());

mongoose.connect('mongodb://127.0.0.1:27017/SwarmMindDB');

app.post('/api/generate', (req, res) => {
    const { prompt } = req.body;
    if (!prompt) return res.status(400).json({ error: "Prompt required." });

    const cleanPrompt = prompt.replace(/"/g, '\\"');
  
    const pythonExecutable = 'D:\\SwarmMind\\ai_env\\Scripts\\python.exe';
    const pythonScript = 'D:\\SwarmMind\\SwarmMind\\edge_nodes\\run_inference.py';



  const pyProcess = spawn(pythonExecutable, [pythonScript, cleanPrompt], {
        env: { ...process.env }
    });

    let aiResponse = "";
    pyProcess.stdout.on('data', (data) => { aiResponse += data.toString(); });

  
    pyProcess.stderr.on('data', (data) => {
        console.error(`PYTHON ERROR: ${data.toString()}`);
    });

    pyProcess.on('close', async (code) => {
        if (code !== 0) return res.status(500).json({ error: "AI failure." });
        res.json({ response: aiResponse.trim() });
    });
});

app.listen(3000, () => console.log("Bridge running on port 3000"));
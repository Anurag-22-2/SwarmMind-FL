const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const mongoose = require('mongoose');

const app = express();
app.use(cors({ origin: '*' }));
app.use(express.json());

mongoose.connect('mongodb://127.0.0.1:27017/SwarmMindDB');

// app.post('/api/generate', (req, res) => {
//     const { prompt } = req.body;
//     if (!prompt) return res.status(400).json({ error: "Prompt required." });

//     const cleanPrompt = prompt.replace(/"/g, '\\"');
  
//     const pythonExecutable = 'D:\\SwarmMind\\ai_env\\Scripts\\python.exe';
//     const pythonScript = 'D:\\SwarmMind\\SwarmMind\\edge_nodes\\run_inference.py';



//   const pyProcess = spawn(pythonExecutable, [pythonScript, cleanPrompt], {
//         env: { ...process.env }
//     });

//     let aiResponse = "";
//     pyProcess.stdout.on('data', (data) => { aiResponse += data.toString(); });

  
//     pyProcess.stderr.on('data', (data) => {
//         console.error(`PYTHON ERROR: ${data.toString()}`);
//     });

//     pyProcess.on('close', async (code) => {
//         if (code !== 0) return res.status(500).json({ error: "AI failure." });
//         res.json({ response: aiResponse.trim() });
//     });
// });

// app.listen(3000, () => console.log("Bridge running on port 3000"));


// Yahan hum spawn ko hata kar fetch API ka use kar rahe hain
// Yahan hum spawn ko hata kar fetch API ka use kar rahe hain
// Yahan hum spawn ko hata kar fetch API ka use kar rahe hain
app.post('/api/generate', async (req, res) => {
    const { prompt } = req.body;
    if (!prompt) return res.status(400).json({ error: "Prompt required." });

    try {
        // Node.js ab seedha Python FastAPI ko request bhejega
        const pythonResponse = await fetch('http://127.0.0.1:8000/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: prompt })
        });

        if (!pythonResponse.ok) {
            throw new Error(`Python API responded with status ${pythonResponse.status}`);
        }

        const data = await pythonResponse.json();
        // Instant response frontend ko bhej do
        res.json({ response: data.response });

    } catch (error) {
        console.error(`BRIDGE ERROR: ${error.message}`);
        res.status(500).json({ error: "AI Engine is not running or encountered an error." });
    }
});app.listen(3000, () => console.log("Bridge running on port 3000"));
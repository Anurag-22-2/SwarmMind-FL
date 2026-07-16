const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const mongoose = require('mongoose');

const app = express();
const PORT = 3000;


mongoose.connect('mongodb://127.0.0.1:27017/SwarmMindDB')
    .then(() => console.log("MongoDB Connected Successfully"))
    .catch(err => console.error(" MongoDB Connection Error:", err));

const ChatSchema = new mongoose.Schema({
    prompt: String,
    response: String,
    timestamp: { type: Date, default: Date.now }
});
const ChatHistory = mongoose.model('ChatHistory', ChatSchema);

app.use(cors({ origin: '*' })); 
app.use(express.json());

app.post('/api/generate', (req, res) => {
    const { prompt } = req.body;
    
    if (!prompt) {
        return res.status(400).json({ error: "Prompt required." });
    }

    console.log(`📡 Local Request Received: "${prompt}"`);

    
    const cleanPrompt = prompt.replace(/[\r\n]+/g, ' ').replace(/"/g, '\\"');

    
const pythonExecutable = 'D:\\SwarmMind\\.venv\\Scripts\\python.exe';


const pythonScript = 'D:\\SwarmMind\\SwarmMind\\edge_nodes\\run_inference.py';

    console.log(`🧠 Routing matrix arrays to isolated backend context...`);

    
    const pyProcess = spawn(pythonExecutable, [pythonScript, cleanPrompt]);

    let aiResponse = "";
    let errorResponse = "";

    pyProcess.stdout.on('data', (data) => {
        aiResponse += data.toString();
    });

    pyProcess.stderr.on('data', (data) => {
        errorResponse += data.toString();
       
        console.error(`\n PYTHON CRASH LOG: ${data.toString()}\n`); 
    });

    pyProcess.on('close', async (code) => { 
        if (code !== 0) {
            console.error(`Python Error Code: ${code}`);
            return res.status(500).json({ error: "Local AI compute failure.", details: errorResponse });
        }
        
        const finalResponse = aiResponse.trim();
        
        try {
            const newLog = new ChatHistory({ prompt, response: finalResponse });
            await newLog.save();
            console.log(" Chat logged to MongoDB");
        } catch (dbErr) {
            console.error(" Failed to log to DB:", dbErr);
        }

        res.json({ response: finalResponse });
    });
});

app.listen(PORT, () => {
    console.log(``);
    console.log(`SWARMMIND CENTRAL BRIDGE RUNNING ON PORT ${PORT}`);
    console.log(``);
});
# SwarmMind-FL 

A decentralized computing system that keeps sensitive data private by training and running models locally on individual edge devices rather than a central server.

 **Live Demo:** [swarm-mind-fl.vercel.app](https://swarm-mind-fl.vercel.app)

---

##  Overview

Traditional tracking and environment monitoring systems rely on centralized cloud architectures, which introduce high latency and critical privacy risks. **SwarmMind-FL** shifts the paradigm to **Edge Intelligence**. It creates an autonomous, decentralized network of edge nodes that collaboratively monitor and interpret the status of an environment in real-time without ever transmitting sensitive data to an external cloud.

## Key Features

* **Privacy-First (No Cloud):** Sensitive presence data is processed strictly on local edge hardware.
* **Zero Latency:** Edge-native processing ensures real-time decision-making without network dependency.
* **Heavyweight Local AI:** Powered by advanced large language models (like Qwen2.5-72B-Instruct) optimized for high-VRAM local execution.
* **Decentralized Aggregation:** Individual nodes operate independently while seamlessly syncing with a local aggregator server.

## Tech Stack

* **AI/Inference Engine:** Python, PyTorch, Hugging Face Transformers
* **Local Server & Aggregator:** Node.js, Express.js, MongoDB
* **Frontend/Dashboard:** React.js, HTML, CSS, JavaScript
* **Models Used:** Qwen2.5-72B-Instruct

##  Local Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/Anurag-22-2/SwarmMind-FL.git](https://github.com/Anurag-22-2/SwarmMind-FL.git)
cd SwarmMind-FL

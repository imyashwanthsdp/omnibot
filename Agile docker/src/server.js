const express = require("express");
const path = require("path");
const GeneralChatbotEngine = require("./chatbot");

const app = express();
const PORT = process.env.PORT || 3000;
const bot = new GeneralChatbotEngine();

app.use(express.json());
app.use(express.static(path.join(__dirname, "../public")));

// API Endpoint: Send Chat Message
app.post("/api/chat", (req, res) => {
  const { message } = req.body;
  const response = bot.processMessage(message);
  res.json(response);
});

// API Endpoint: Healthcheck for Jenkins Validation Stage & Monitoring
app.get("/api/health", (req, res) => {
  res.json({
    status: "UP",
    appName: "General-Chatbot-App",
    botName: bot.botName,
    version: bot.version,
    timestamp: new Date().toISOString()
  });
});

// Serve Frontend
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "../public/index.html"));
});

// Only start server if executed directly
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`[General Chatbot Server] Running on http://localhost:${PORT}`);
  });
}

module.exports = app;

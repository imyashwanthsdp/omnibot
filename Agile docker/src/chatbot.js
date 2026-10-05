/**
 * General Purpose Chatbot Engine (OmniBot)
 * Handles general conversation, queries, FAQs, utilities, and system status.
 */

class GeneralChatbotEngine {
  constructor() {
    this.botName = "OmniBot Assistant";
    this.version = "1.0.0";
    
    // Comprehensive intent knowledge base (ordered by specificity)
    this.intents = [
      {
        name: "greeting",
        patterns: [/hello/i, /hi\b/i, /hey/i, /greetings/i, /good morning/i, /good evening/i],
        responses: [
          "Hello! I am OmniBot, your General AI Assistant. How can I assist you today?",
          "Hi there! How can I help you today?",
          "Greetings! Feel free to ask me any question or try one of the quick options below."
        ]
      },
      {
        name: "tech_faq",
        patterns: [/jenkins/i, /docker/i, /pipeline/i, /cloud/i, /devops/i, /continuous integration/i],
        responses: [
          "Docker packages applications into lightweight containers to ensure smooth execution across all environments.",
          "Jenkins automates continuous integration pipelines by testing code and building container images on every GitHub commit.",
          "Continuous Integration (CI) catches bugs early, improves code quality, and speeds up software delivery cycles."
        ]
      },
      {
        name: "time_date",
        patterns: [/time/i, /date/i, /day/i, /what time/i, /what date/i, /today/i],
        responses: [
          `The current system date & time is: ${new Date().toLocaleString()}`,
          `Today's UTC timestamp is: ${new Date().toISOString()}`
        ]
      },
      {
        name: "capabilities",
        patterns: [/what can you do/i, /help/i, /features/i, /capabilities/i, /commands/i],
        responses: [
          "I am a General Purpose Chatbot! You can ask me about: general questions, time/date, basic math calculations, project status, technology FAQs, or try typing 'hello'."
        ]
      },
      {
        name: "general_knowledge",
        patterns: [/who are you/i, /what is your name/i, /who created you/i, /tell me about yourself/i],
        responses: [
          "I am OmniBot, a general-purpose conversational chatbot built with Node.js and containerized with Docker!",
          "I am an intelligent assistant designed to process user queries, execute automated validation tests, and run inside containerized environments."
        ]
      },
      {
        name: "weather_smalltalk",
        patterns: [/weather/i, /how are you/i, /how is it going/i, /feeling/i],
        responses: [
          "I'm doing great and running smoothly! How can I help you today?",
          "Systems are operational and all circuits are running at peak performance!"
        ]
      },
      {
        name: "farewell",
        patterns: [/bye/i, /goodbye/i, /see you/i, /exit/i],
        responses: [
          "Goodbye! Have a fantastic day ahead!",
          "Farewell! Reach out whenever you need assistance."
        ]
      },
      {
        name: "status",
        patterns: [/status/i, /health/i, /system info/i, /version/i],
        responses: [
          `OmniBot v${this.version} is ONLINE and healthy!`
        ]
      }
    ];
  }

  processMessage(userMessage) {
    if (!userMessage || typeof userMessage !== "string" || userMessage.trim() === "") {
      return {
        reply: "I didn't receive any text. Please type a message!",
        intent: "empty_input",
        timestamp: new Date().toISOString()
      };
    }

    const cleanedInput = userMessage.trim();

    // Math evaluation
    const mathMatch = cleanedInput.match(/(?:calculate|math|what is|\=)?\s*(\d+\s*[\+\-\*\/]\s*\d+)/i);
    if (mathMatch) {
      try {
        const expression = mathMatch[1];
        const result = Function(`"use strict"; return (${expression})`)();
        return {
          reply: `The result of ${expression} is ${result}.`,
          intent: "math_calculation",
          timestamp: new Date().toISOString()
        };
      } catch (err) {
        // Fall back to intent matching
      }
    }

    // Intent matching
    for (const intent of this.intents) {
      for (const pattern of intent.patterns) {
        if (pattern.test(cleanedInput)) {
          const randomIndex = Math.floor(Math.random() * intent.responses.length);
          return {
            reply: intent.responses[randomIndex],
            intent: intent.name,
            timestamp: new Date().toISOString()
          };
        }
      }
    }

    // Default fallback
    return {
      reply: `I'm not completely sure about "${cleanedInput}", but I am learning every day! Try asking about 'help', 'time', 'weather', or technology topics.`,
      intent: "general_fallback",
      timestamp: new Date().toISOString()
    };
  }
}

module.exports = GeneralChatbotEngine;

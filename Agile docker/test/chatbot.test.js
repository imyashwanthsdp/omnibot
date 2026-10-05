const assert = require("assert");
const test = require("node:test");
const GeneralChatbotEngine = require("../src/chatbot");

test("GeneralChatbotEngine - Greeting Intent Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("Hello there!");
  assert.strictEqual(res.intent, "greeting");
  assert.ok(res.reply.length > 0);
});

test("GeneralChatbotEngine - Math Calculation Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("calculate 25 * 4");
  assert.strictEqual(res.intent, "math_calculation");
  assert.ok(res.reply.includes("100"));
});

test("GeneralChatbotEngine - Time and Date Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("What time is it?");
  assert.strictEqual(res.intent, "time_date");
  assert.ok(res.reply.length > 0);
});

test("GeneralChatbotEngine - Tech FAQ Intent Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("Tell me about Docker container");
  assert.strictEqual(res.intent, "tech_faq");
  assert.ok(res.reply.includes("Docker"));
});

test("GeneralChatbotEngine - General Fallback Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("random obscure query 9999");
  assert.strictEqual(res.intent, "general_fallback");
});

test("GeneralChatbotEngine - Empty Input Test", () => {
  const bot = new GeneralChatbotEngine();
  const res = bot.processMessage("");
  assert.strictEqual(res.intent, "empty_input");
});

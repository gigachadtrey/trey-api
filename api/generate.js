import { Configuration, GenerativeModel } from "@gemini-ai/sdk";

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

if (!GEMINI_API_KEY) {
  throw new Error("GEMINI_API_KEY environment variable is not set.");
}

const geminiModel = new GenerativeModel(GEMINI_API_KEY);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { accessKey, input, model = "gemini-1.5-flash" } = req.body;

  if (accessKey !== "geminiaccesskey6383") {
    return res.status(403).json({ error: "Unauthorized" });
  }

  if (!input) {
    return res.status(400).json({ error: "No input provided" });
  }

  try {
    const response = await geminiModel.generateContent(input, model);
    return res.status(200).json({ generated_content: response.text });
  } catch (error) {
    return res.status(500).json({ error: `Failed to generate content: ${error.message}` });
  }
}

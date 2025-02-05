import GroqClient from "groq-sdk";

const GROQ_API_KEY = process.env.GROQ_API_KEY;

const groqClient = new GroqClient(GROQ_API_KEY);

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { accessKey, input, model = "llama-3.3-70b-versatile" } = req.body;

  if (accessKey !== "geminiaccesskey6383") {
    return res.status(403).json({ error: "Unauthorized" });
  }

  if (!input) {
    return res.status(400).json({ error: "No input provided" });
  }

  try {
    const stream = await groqClient.chat.completions.create({
      messages: [{ role: "user", content: input }],
      model,
      stream: true
    });

    stream.on("data", (chunk) => {
      const token = chunk.choices[0].delta.content || "";
      res.write(token + " ");
    });

    stream.on("end", () => res.end());
  } catch (error) {
    res.status(500).json({ error: `Failed to generate content: ${error.message}` });
  }
}

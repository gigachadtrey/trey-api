export default function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  const { accessKey } = req.body;

  if (accessKey !== "geminiaccesskey6383") {
    return res.status(403).json({ error: "Unauthorized" });
  }

  res.status(200).json({ GEMINI_API_KEY: process.env.GEMINI_API_KEY });
}

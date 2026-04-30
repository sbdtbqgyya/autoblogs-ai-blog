import { routeModel } from "../services/router";
import { callDeepSeek } from "../services/deepseek";
import { callGemini } from "../services/gemini";
import { saveLog } from "../services/supabase";

export default async function handler(req, res) {
  try {
    const { prompt, userId } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: "prompt is required" });
    }

    const model = routeModel(prompt);

    let result = "";

    if (model === "deepseek") {
      result = await callDeepSeek(prompt);
    } else {
      result = await callGemini(prompt);
    }

    try {
      await saveLog({
        userId,
        prompt,
        model,
        result,
      });
    } catch (e) {
      console.log("log save failed:", e);
    }

    res.json({
      model,
      result,
    });

  } catch (err) {
    console.error("AI Gateway Error:", err);
    res.status(500).json({ error: "internal error" });
  }
}

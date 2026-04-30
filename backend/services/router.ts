export function routeModel(prompt: string) {
  const len = prompt.length;

  // 长文本 → DeepSeek
  if (len > 1500) return "deepseek";

  // 编程类任务 → DeepSeek
  if (
    prompt.includes("code") ||
    prompt.includes("error") ||
    prompt.includes("debug") ||
    prompt.includes("function")
  ) {
    return "deepseek";
  }

  // 默认 → Gemini（快）
  return "gemini";
}

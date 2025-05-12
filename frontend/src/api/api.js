import axios from "axios";

export const getAIMessage = async (
  userMessage,
  chatHistory,
  contextText = ""
) => {
  const payload = {
    user_message: userMessage,
    chat_history: chatHistory,
    context: contextText, // 如果没有 context，也可以默认是空字符串
  };

  console.log("Payload to /chat:", payload); // 🐞 Debug 时看清楚传了什么

  const response = await axios.post("http://localhost:8000/chat", payload);
  return response.data;
};

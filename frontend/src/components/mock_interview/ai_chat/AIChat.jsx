import { useState, useRef, useEffect } from "react";
import { Box, TextField, Typography, IconButton, CircularProgress } from "@mui/material";
import { BiUpArrowCircle } from "react-icons/bi";
import { Visibility, VisibilityOff, SmartToy } from "@mui/icons-material";
import ReactMarkdown from "react-markdown";
import Logo from "../../Logo";
import axios from "axios";

const AIChat = ({ difficulty, code, auth0UserId }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionData, setSessionData] = useState(null);
  const messagesEndRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [isCodeContext, setIsCodeContext] = useState(true);
  const eventSourceRef = useRef(null);
  const [user, setUser] = useState(null);

  // Get question and save initial convo, update messages array
  useEffect(() => {
    const startInterview = async () => {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/interview/start-interview`, {
          difficulty: difficulty,
        });

        const { message, question } = response.data;
        const initialConversation = [
          {
            role: "system",
            content: [
              {
                type: "text",
                text: `You are an AI technical interviewer named Cody. You are conducting a coding interview.
                     Your role is to:
                     1. Guide the candidate through the coding problem
                     2. Provide hints when they're stuck
                     3. Ask follow-up questions about their solution
                     4. Evaluate their problem-solving approach
                     5. Keep responses clear and concise
                     Be professional but friendly, and focus on helping the candidate demonstrate their skills.`,
              },
            ],
          },
          {
            role: "assistant",
            content: [{ type: "text", text: message }],
          },
        ];

        setSessionData({
          sessionId: auth0UserId,
          conversation: initialConversation,
        });
        setMessages([{ sender: "Bot", text: message }]);

        // Store question ID and conversation for submission
        sessionStorage.setItem("currentQuestionId", question.id);
        sessionStorage.setItem("conversation", JSON.stringify(initialConversation));
      } catch (error) {
        console.error("Error starting interview:", error);
      }
    };

    startInterview();
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [difficulty]);

  // Initialize the SSE connection
  useEffect(() => {
    const initializeSSE = () => {
      console.log("Initializing SSE connection");

      if (eventSourceRef.current) {
        console.log("Closing existing SSE connection");
        eventSourceRef.current.close();
      }

      // Try and establish connection using auth0 user id
      const eventSource = new EventSource(
        `${import.meta.env.VITE_API_URL}/interview/stream?auth0_user_id=${user?.sub}`,
        { withCredentials: true },
      );

      eventSource.onopen = () => {
        console.log("SSE connection opened");
      };

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "heartbeat") {
          console.log("Received heartbeat");
        }
      };

      eventSource.onerror = (error) => {
        console.error("SSE Error:", error);
        eventSource.close();
        setTimeout(initializeSSE, 5000);
      };

      eventSourceRef.current = eventSource;
    };

    if (user?.sub) {
      initializeSSE();
    }

    return () => {
      if (eventSourceRef.current) {
        console.log("Cleaning up SSE connection");
        eventSourceRef.current.close();
      }
    };
  }, [user?.sub]);

  // Send message to chatbot
  const handleSend = async () => {
    if (!input.trim()) return;

    // Retrieve the current input and reset
    const curInput = input;
    setInput("");
    setLoading(true);

    // Update messages with the new message from the user
    const newUserMessage = { sender: "You", text: curInput };
    setMessages((prev) => [...prev, newUserMessage]);

    try {
      // Call api to get response containing readable stream
      const response = await fetch(`${import.meta.env.VITE_API_URL}/interview/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: curInput,
          code: isCodeContext ? code : "",
          session_data: sessionData,
        }),
      });

      // Reader to process the stream
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let botMessage = "";

      // Process stream
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(5));

            if (data.type === "chunk") {
              botMessage += data.content;
              setMessages((prev) => {
                const newMessages = [...prev];
                // Update or add the bot's message
                const lastMessage = newMessages[newMessages.length - 1];
                if (lastMessage.sender === "Bot") {
                  lastMessage.text = botMessage;
                } else {
                  newMessages.push({ sender: "Bot", text: botMessage });
                }
                return newMessages;
              });
            } else if (data.type === "done") {
              setSessionData(data.session_data);
              sessionStorage.setItem("conversation", JSON.stringify(data.session_data.conversation));
              setLoading(false);
            }
          }
        }
      }
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: "Sorry, there was an error processing your message.",
        },
      ]);
      setLoading(false);
    }
  };


  
  const handleSubmitSolution = async () => {
    if (!code.trim()) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: "Please write some code before submitting.",
        },
      ]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/interview/submit-solution`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: code,
          session_data: sessionData,
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let botMessage = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = JSON.parse(line.slice(5));

            if (data.type === "chunk") {
              botMessage += data.content;
              setMessages((prev) => {
                const newMessages = [...prev];
                // Update or add the bot's message
                const lastMessage = newMessages[newMessages.length - 1];
                if (lastMessage.sender === "Bot") {
                  lastMessage.text = botMessage;
                } else {
                  newMessages.push({ sender: "Bot", text: botMessage });
                }
                return newMessages;
              });
            } else if (data.type === "done") {
              setSessionData(data.session_data);
              sessionStorage.setItem("conversation", JSON.stringify(data.session_data.conversation));
            }
          }
        }
      }
    } catch (error) {
      console.error("Error submitting solution:", error);
      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: "Sorry, there was an error analyzing your solution. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  const handleLogoClick = () => {
    navigate("/dashboard");
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Box display="flex" flexDirection="column" height="100%" p={0}>
      <Box
        sx={{
          bgcolor: "#F5F5F5",
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 2,
          minHeight: "38px",
          flexShrink: 0,
          borderBottom: "2px solid #BDBDBD", // BORDER - top
          justifyContent: "space-between",
        }}>
        <Logo onClick={handleLogoClick} />

        <Box
          sx={{
            borderRadius: "8px",
            pt: "4px",
            pb: "4px",
            pl: "4px",
            pr: "4px",
          }}>
          <Typography
            variant="h6"
            sx={{
              color:
                difficulty === "Easy"
                  ? "#4caf50" // Green
                  : difficulty === "Medium"
                    ? "#ffa000" // Amber
                    : "#f44336", // Red
              fontWeight: "bold",
              fontSize: "0.8rem",
              padding: "1px",
            }}>
            {difficulty}
          </Typography>
        </Box>
      </Box>

      {/* Chat Messages */}
      <Box
        flex={1}
        overflow="auto"
        mb={0}
        p={2}
        borderRadius={0}
        color="black"
        sx={{
          bgcolor: "#FFFFFF",
        }}>
        {messages.map((message, index) => (
          <Box key={index} mb={2}>
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1,
                mb: 0.5,
              }}>
              {message.sender === "You" ? (
                <Typography
                  variant="caption"
                  sx={{
                    color: "#f4a261",
                    fontWeight: "bold",
                  }}>
                  {message.sender}
                </Typography>
              ) : (
                <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                  <SmartToy
                    sx={{
                      color: "#569cd6",
                      fontSize: 20,
                      mb: 0.2,
                    }}
                  />
                  <Typography
                    variant="caption"
                    sx={{
                      color: "#569cd6",
                      fontWeight: "bold",
                    }}>
                    Cody
                  </Typography>
                </Box>
              )}
              <Box
                sx={{
                  flexGrow: 1,
                  height: "1px",
                  bgcolor: "#f2f2f220",
                }}
              />
            </Box>
            {/* Message Text */}
            <Typography
              variant="body1"
              className="ai-chat-message"
              sx={{
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
                overflowWrap: "break-word",
                maxWidth: "100%",
              }}>
              <ReactMarkdown>{message.text}</ReactMarkdown>
            </Typography>
          </Box>
        ))}
        <div ref={messagesEndRef} />
        {loading && (
          <Box display="flex" justifyContent="flex-start" alignItems="left" mt={2}>
            <CircularProgress color="inherit" size={20} />
          </Box>
        )}
      </Box>

      {/* Input Box */}
      <Box
        sx={{
          borderTop: "2px solid #BDBDBD", // BORDER - bottom
          bgcolor: "#F5F5F5",
        }}>
        <Box display="flex" flexDirection="column" gap={0.5} p={1}>
          <Box display="flex" alignItems="center" gap={1}>
            <TextField
              variant="standard"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              fullWidth
              placeholder="Type your message..."
              multiline
              minRows={2}
              maxRows={7}
              slotProps={{
                input: {
                  disableUnderline: true,
                  sx: {
                    color: "black",
                  },
                },
              }}
            />
          </Box>

          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box
              display="flex"
              alignItems="center"
              gap={1}
              sx={{
                border: "1px solid #f4a261",
                borderRadius: 1,
                padding: "0px 8px",
              }}>
              <Typography
                variant="caption"
                sx={{
                  color: isCodeContext ? "primary.main" : "#666",
                  userSelect: "none",
                  textDecoration: isCodeContext ? "none" : "line-through",
                  fontStyle: isCodeContext ? "normal" : "italic",
                }}>
                Current Code
              </Typography>
              <IconButton
                size="small"
                onClick={() => setIsCodeContext(!isCodeContext)}
                sx={{
                  color: isCodeContext ? "primary.main" : "#666",
                }}>
                {isCodeContext ? <Visibility /> : <VisibilityOff />}
              </IconButton>
            </Box>

            <IconButton aria-label="send" color="primary" onClick={handleSend}>
              <BiUpArrowCircle size={35} />
            </IconButton>
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default AIChat;

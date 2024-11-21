import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, IconButton } from "@mui/material";
import axios from "axios";
import { IoArrowUpCircleOutline } from "react-icons/io5";
import { BiUpArrow, BiUpArrowCircle } from "react-icons/bi";
import { Terminal, SmartToy } from "@mui/icons-material";
import { Code, CodeOff, Visibility, VisibilityOff } from '@mui/icons-material';

const AIChat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]); // store all messages
  const messagesEndRef = useRef(null); // reference to end of message list
  
  const [isCodeContext, setIsCodeContext] = useState(false);

  const handleToggleCodeContext = (index) => {
    setMessages(messages.map((msg, i) => 
      i === index 
        ? { ...msg, hasCodeContext: !msg.hasCodeContext }
        : msg
    ));
  };
  // scroll to the bottom of the messages
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]); //run whenever the array changes

  const handleSend = async () => {
    if (!input.trim()) return;

    const curInput = input;

    setInput("");

    // add the users message to the chat
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "You", text: curInput, hasCodeContext: isCodeContext },
    ]);

    try {
      const res = await axios.post(
        "https://api.openai.com/v1/completions",
        {
          model: "text-davinci-003",
          prompt: curInput,
          max_tokens: 150,
        },
        {
          headers: { Authorization: `Bearer YOUR_API_KEY` },
        },
      );

      const aiResponse = res.data.choices[0].text.trim();

      // add the ai response to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "Bot", text: aiResponse, hasCodeContext: false },
      ]);
    } catch (error) {
      console.error("Error fetching AI response:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "Bot", text: "Sorry, I couldn't process that." },
      ]);
    }
    setInput("");
  };

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
          bgcolor: "#1e1e1e",
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 2, // Match AIChat padding
          minHeight: "32px", // Match AIChat height
          flexShrink: 0,
          borderBottom: "2px solid black",
        }}
      >
        <Terminal
          sx={{
            fontSize: 24,
            color: "#f4a261",
          }}
        />
        <Typography
          variant="h6"
          sx={{
            color: "#f4a261",
            fontWeight: "bold",
            fontSize: "1.1rem",
          }}
        >
          Hackilo
        </Typography>
      </Box>

      {/* Chat Messages */}
      <Box
        flex={1}
        overflow="auto"
        mb={0}
        p={2}
        borderRadius={0}
        color="white"
        sx={{
          bgcolor: "#2e2e2e",
        }}
      >
        {messages.map((message, index) => (
          <Box key={index} mb={2}>
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                gap: 1,
                mb: 0.5,
              }}
            >
              {message.sender === "You" ? (
                <Typography
                  variant="caption"
                  sx={{
                    color: "#f4a261",
                    fontWeight: "bold",
                  }}
                >
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
                    }}
                  >
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
              sx={{
                whiteSpace: "pre-wrap", // Allow text wrapping
                wordWrap: "break-word", // Break long words
                overflowWrap: "break-word", // Ensure long words wrap
                maxWidth: "100%", // Contain within parent
              }}
            >
              {message.text}
            </Typography>
          </Box>
        ))}
        {/* Dummy div to ensure scrolling */}
        <div ref={messagesEndRef} />
      </Box>

      {/* Input Box */}
      <Box
        sx={{
          borderTop: "2px solid black",
          bgcolor: "#1e1e1e",
        }}
        color="white"
      >
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
                    color: "white",
                  },
                },
              }}
            />
          </Box>
          
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box display="flex" alignItems="center" gap={1}
            sx={{
              border: '1px solid rgba(255, 255, 255, 0.1)',
              borderRadius: 1,
              padding: '0px 8px',
            }}>
              <Typography
                variant="caption"
                sx={{
                  color: isCodeContext ? "#f4a261" : "#666",
    userSelect: "none",
    textDecoration: isCodeContext ? "none" : "line-through",
    fontStyle: isCodeContext ? "normal" : "italic",
                }}
              >
                Current Code
              </Typography>
              <IconButton 
                size="small"
                onClick={() => setIsCodeContext(!isCodeContext)}
                sx={{ 
                  color: isCodeContext ? "#f4a261" : "#666"
                }}
              >
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

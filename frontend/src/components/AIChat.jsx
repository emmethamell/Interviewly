import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, IconButton } from "@mui/material";
import axios from "axios";
import { IoArrowUpCircleOutline } from "react-icons/io5";
import { BiUpArrow, BiUpArrowCircle } from "react-icons/bi";

const AIChat = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]); // store all messages
  const messagesEndRef = useRef(null); // reference to end of message list

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
      { sender: "You", text: curInput },
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
        { sender: "Bot", text: aiResponse },
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
      {/* Chat Messages */}
      <Box
        flex={1}
        overflow="auto"
        mb={0}
        p={2}
        pt={10} 
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
              <Typography
                variant="caption"
                sx={{
                  color: message.sender === "You" ? "#f4a261" : "#569cd6",
                  fontWeight: "bold",
                }}
              >
                {message.sender}
              </Typography>
              <Box
                sx={{
                  flexGrow: 1,
                  height: "1px",
                  bgcolor: "#f2f2f220",
                }}
              />
            </Box>
            {/* Message Text */}
            <Typography variant="body1">{message.text}</Typography>
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
        <Box display="flex" alignItems="center" gap={1} p={1}>
          <TextField
            variant="standard"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            fullWidth
            placeholder="Type your message..."
            multiline
            rows={2}
            slotProps={{
              input: {
                disableUnderline: true,
                sx: {
                  color: "white",
                },
              },
            }}
          />
          <IconButton aria-label="send" color="primary" onClick={handleSend}>
            <BiUpArrowCircle size={35} />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
};

export default AIChat;

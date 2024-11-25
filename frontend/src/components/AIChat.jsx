import React, { useState, useRef, useEffect } from "react";
import { Box, TextField, Button, Typography, IconButton } from "@mui/material";
import { IoArrowUpCircleOutline } from "react-icons/io5";
import { BiUpArrow, BiUpArrowCircle } from "react-icons/bi";
import { Terminal, SmartToy } from "@mui/icons-material";
import { Code, CodeOff, Visibility, VisibilityOff } from "@mui/icons-material";

const AIChat = ({ difficulty, socket, code}) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const [isCodeContext, setIsCodeContext] = useState(false);

  const handleToggleCodeContext = (index) => {
    setMessages(
      messages.map((msg, i) =>
        i === index ? { ...msg, hasCodeContext: !msg.hasCodeContext } : msg,
      ),
    );
  };

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ensure that the event listener for bot_message is set up when component mounts
  // when the server emits a bot_message event, client recieves it and updates messages state, which re renders the page
  useEffect(() => { 
    if (socket) {
      console.log("Setting up socket event listeners");
      socket.on("bot_message", (message) => { //on bot_message event
        console.log("Received bot_message:", message);
        setMessages((prevMessages) => [ //update the messanges state
          ...prevMessages,
          { sender: "Bot", text: message.message, hasCodeContext: false },
        ]);
      });
    }

    // clean up when the component unmounts or when the instance of socket changes
    return () => {
      if (socket) {
        console.log("Cleaning up socket event listeners");
        socket.off("bot_message");
      }
    };
  }, [socket]);

  
  const handleSend = () => {
    if (!input.trim()) return;

    const curInput = input;
    setInput("");

    // update the messages to re render the state
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "You", text: curInput, code: isCodeContext? code : "" },
    ]);

    // send to the server using emit
    if (socket) {
      socket.emit("user_message", { message: curInput, code: isCodeContext? code : "" }); // server listens for user_message event
    }
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
          p: 2,
          minHeight: "32px",
          flexShrink: 0,
          borderBottom: "2px solid black",
          justifyContent: "space-between",
        }}
      >
        <Box display="flex" flexDirection="row" p={0}>
          <Terminal
            sx={{
              fontSize: 24,
              color: "#f4a261",
              padding: "1px",
            }}
          />
          <Typography
            variant="h6"
            sx={{
              color: "#f4a261",
              fontWeight: "bold",
              fontSize: "1.1rem",
              padding: "1px",
            }}
          >
            Hackilo
          </Typography>
        </Box>

        <Box
          sx={{
            
            borderRadius: "8px",
            pt: "4px",
            pb: "4px",
            pl: "4px",
            pr: "4px",
          }}
        >
          <Typography
            variant="h6"
            sx={{
              color:
                difficulty === "Easy"
                  ? "#4caf50"
                  : difficulty === "Medium"
                    ? "#ffeb3b"
                    : "#f44336",
              fontWeight: "bold",
              fontSize: "0.8rem",
              padding: "1px",
            }}
          >
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
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
                overflowWrap: "break-word",
                maxWidth: "100%",
              }}
            >
              {message.text}
            </Typography>
          </Box>
        ))}
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

          <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
          >
            <Box
              display="flex"
              alignItems="center"
              gap={1}
              sx={{
                border: "1px solid rgba(255, 255, 255, 0.1)",
                borderRadius: 1,
                padding: "0px 8px",
              }}
            >
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
                  color: isCodeContext ? "#f4a261" : "#666",
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

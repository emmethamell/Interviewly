import { useState, useRef, useEffect } from "react";
import { Box, TextField, Typography, IconButton, CircularProgress } from "@mui/material";
import { BiUpArrowCircle } from "react-icons/bi";
import { Visibility, VisibilityOff, SmartToy } from "@mui/icons-material";
import ReactMarkdown from "react-markdown";
import Logo from "../../Logo";

const AIChat = ({ difficulty, socket, code }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [questionContents, setQuestionContents] = useState(null);

  const [isCodeContext, setIsCodeContext] = useState(true);

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

  useEffect(() => {
    if (socket) {
      console.log("Setting up socket event listeners");
      socket.on("bot_message", (message) => {
        //on bot_message event
        if (message.first_message) {
          setQuestionContents({
            id: message.question_id,
            content: message.question_content,
            difficulty: message.question_difficulty,
            name: message.question_name,
          });
        }
        setMessages((prevMessages) => [
          //update the messages state
          ...prevMessages,
          { sender: "Bot", text: message.message, hasCodeContext: false },
        ]);
        setLoading(false);
      });
    }
    return () => {
      if (socket) {
        socket.off("bot_message");
      }
    };
  }, [socket]);

  const handleSend = () => {
    if (!input.trim()) return;

    const curInput = input;
    setInput("");
    setLoading(true);

    // update the messages to re-render the state
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: "You", text: curInput, code: isCodeContext ? code : "" },
    ]);

    // send to server using emit
    if (socket) {
      socket.emit("user_message", {
        message: curInput,
        code: isCodeContext ? code : "",
      });
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
          bgcolor: "#F5F5F5",
          display: "flex",
          alignItems: "center",
          gap: 1,
          p: 2,
          minHeight: "38px",
          flexShrink: 0,
          borderBottom: "2px solid black",
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
              color: difficulty === "Easy" 
                ? "#4caf50"  // Green 
                : difficulty === "Medium" 
                ? "#ffa000"  // Amber 
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
          borderTop: "2px solid black",
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

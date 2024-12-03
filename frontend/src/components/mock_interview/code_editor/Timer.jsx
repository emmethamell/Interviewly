// Timer.jsx
import React, { useState, useEffect } from "react";
import { Box, Typography } from "@mui/material";
import { AccessTime } from "@mui/icons-material";

export const Timer = ({ minutes, onTimeUp }) => {
  const [timeLeft, setTimeLeft] = useState(minutes * 60);
  const [isRunning, setIsRunning] = useState(true);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTimeLeft((prevTime) => {
        if (prevTime <= 1) {
          clearInterval(intervalId);
          if (onTimeUp) {
            onTimeUp();
          }
          return 0;
        }
        return prevTime - 1;
      });
    }, 1000);

    return () => clearInterval(intervalId);
  }, [onTimeUp]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1,
        bgcolor: "#333",
        padding: "4px 12px",
        borderRadius: 1,
        border: "1px solid #555",
        cursor: "pointer",
      }}
      onClick={() => setIsRunning(!isRunning)}
    >
      <AccessTime sx={{ color: "#f4a261", fontSize: 20 }} />
      <Typography sx={{ color: "white", minWidth: "60px", userSelect: "none" }}>
        {formatTime(timeLeft)}
      </Typography>
    </Box>
  );
};

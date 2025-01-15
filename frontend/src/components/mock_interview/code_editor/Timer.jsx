import { useState, useEffect } from "react";
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
        padding: "4px 12px",
        borderRadius: 1,
      }}
      onClick={() => setIsRunning(!isRunning)}
    >
      <AccessTime sx={{ color: "black", fontSize: 30 }} />
      <Typography
        sx={{
          color: "Black",
          minWidth: "60px",
          userSelect: "none",
          fontSize: 20,
        }}
      >
        {formatTime(timeLeft)}
      </Typography>
    </Box>
  );
};

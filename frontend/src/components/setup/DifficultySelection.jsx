// DifficultySelection.jsx
import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  Radio,
  RadioGroup,
  Typography,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import LoginButton from "../auth/LoginButton";
import LogoutButton from "../auth/LogoutButton";

const DifficultySelection = ({ socket }) => {
  const [difficulty, setDifficulty] = useState("Easy");
  const navigate = useNavigate();

  const handleStart = () => {
    navigate("/main", { state: { difficulty } });
  };

  return (
    <div>
      <LoginButton />
      <LogoutButton />
      <Box
        sx={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          bgcolor: "#1e1e1e",
          color: "white",
        }}
      >
        <Typography variant="h4" mb={4}>
          Select Difficulty
        </Typography>
        <FormControl component="fieldset">
          <RadioGroup
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <FormControlLabel value="Easy" control={<Radio />} label="Easy" />
            <FormControlLabel
              value="Medium"
              control={<Radio />}
              label="Medium"
            />
            <FormControlLabel value="Hard" control={<Radio />} label="Hard" />
          </RadioGroup>
        </FormControl>
        <Button
          variant="contained"
          color="primary"
          onClick={handleStart}
          sx={{ mt: 4 }}
        >
          Start
        </Button>
      </Box>
    </div>
  );
};

export default DifficultySelection;

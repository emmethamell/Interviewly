import { useState, useEffect } from "react";
import { Box, Button, FormControl, FormControlLabel, Radio, RadioGroup, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const DifficultySelection = ({ socket }) => {
  const [difficulty, setDifficulty] = useState("Easy");
  const navigate = useNavigate();

  const handleStart = () => {
    navigate("/main", { state: { difficulty } });
  };

  return (
    <div>
      <Box
        sx={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}>
        <Typography variant="h4" mb={4}>
          Select Difficulty
        </Typography>
        <FormControl component="fieldset">
          <RadioGroup value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <FormControlLabel value="Easy" control={<Radio />} label="Easy" />
            <FormControlLabel value="Medium" control={<Radio />} label="Medium" />
            <FormControlLabel value="Hard" control={<Radio />} label="Hard" />
          </RadioGroup>
        </FormControl>
        <Button variant="contained" onClick={handleStart} sx={{ mt: 4 }}>
          Start
        </Button>
      </Box>
    </div>
  );
};

export default DifficultySelection;

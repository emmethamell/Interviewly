import React, { useState, useEffect } from "react";
import { Typography, Box } from "@mui/material";
import { useLocation } from "react-router-dom";

const Score = () => {
  const location = useLocation();
  const { analysis } = location.state || { analysis: [] };

  return (
    <>
    <Box p={3}>
      <Typography variant="h4" color="white" gutterBottom>
        Final Analysis
      </Typography>
      <Box mt={2}>
        <Typography variant="h6" color="white">
          Qualitative Score:
        </Typography>
        <Typography variant="body1" color="white">
          {analysis.qualitative_score}
        </Typography>
      </Box>
      <Box mt={2}>
        <Typography variant="h6" color="white">
          Ratings:
        </Typography>
        <Typography variant="body1" color="white">
          Technical Ability: {analysis.ratings?.technical_ability}
        </Typography>
        <Typography variant="body1" color="white">
          Problem Solving Skills: {analysis.ratings?.problem_solving_skills}
        </Typography>
        <Typography variant="body1" color="white">
          Summary: {analysis.summary}
        </Typography>
        </Box>
        </Box>
        </>
  );
};

export default Score;

import React, { useState, useEffect } from "react";
import { Typography, Box, CircularProgress } from "@mui/material";
import { useLocation } from "react-router-dom";

const Score = ({ socket }) => {
  const location = useLocation();
  const [analysis, setAnalysis] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (socket) {
      socket.on("final_analysis", (data) => {
        setAnalysis(data.analysis);
        setLoading(false)
      });

      return () => {
        socket.off("final_analysis");
      };
    }
  }, [socket]);


  return (
    <Box p={3}>
    { loading ? (
      <Box display="flex" justifyContent="center" alignItems="center" mt={2}>
        <CircularProgress />
      </Box>
    ) : (
      <>
    <Typography variant="h4" color="white" gutterBottom>
      Final Analysis
    </Typography>
        <Box mt={2}>
          <Typography variant="h6" color="white">
            Qualitative Score:
          </Typography>
          <Typography variant="body1" color="white">
            {analysis.qualitative_score || "N/A"}
          </Typography>
        </Box>
        <Box mt={2}>
          <Typography variant="h6" color="white">
            Ratings:
          </Typography>
          <Typography variant="body1" color="white">
            Technical Ability: {analysis.ratings?.technical_ability || "N/A"}
          </Typography>
          <Typography variant="body1" color="white">
            Problem Solving Skills: {analysis.ratings?.problem_solving_skills || "N/A"}
          </Typography>
        </Box>
        <Box mt={2}>
          <Typography variant="h6" color="white">
            Summary:
          </Typography>
          <Typography variant="body1" color="white">
            {analysis.summary || "N/A"}
          </Typography>
        </Box>
      </>
    )}
  </Box>
  );
};

export default Score;

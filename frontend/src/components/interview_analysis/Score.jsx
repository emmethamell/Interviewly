import React, { useState, useEffect } from "react";
import { Typography, Box, CircularProgress } from "@mui/material";
import { useLocation } from "react-router-dom";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

const Score = ({ socket }) => {
  const { getAccessTokenSilently } = useAuth0();
  const location = useLocation();
  const [analysis, setAnalysis] = useState({});
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);

  useEffect(() => {
    if (socket) {
      socket.on("final_analysis", (data) => {
        setAnalysis(data.analysis);
        setQuestion(question)
        setLoading(false)

      });

      return () => {
        socket.off("final_analysis");
      };
    }
  }, [socket]);

  return (
    <Box p={3}>
      {loading ? (
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
              Problem Solving Skills:{" "}
              {analysis.ratings?.problem_solving_skills}
            </Typography>
          </Box>
          <Box mt={2}>
            <Typography variant="h6" color="white">
              Summary:
            </Typography>
            <Typography variant="body1" color="white">
              {analysis.summary}
            </Typography>
          </Box>
        </>
      )}
    </Box>
  );
};

export default Score;

import { useState, useEffect } from "react";
import { Typography, Box, CircularProgress } from "@mui/material";

const Score = ({ socket }) => {
  const [analysis, setAnalysis] = useState({});
  const [loading, setLoading] = useState(true);
  const [question, setQuestion] = useState(null);

  useEffect(() => {
    if (socket) {
      socket.on("final_analysis", (data) => {
        setAnalysis(data.analysis);
        setQuestion(question);
        setLoading(false);
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
          <Typography variant="h4" gutterBottom>
            Final Analysis
          </Typography>
          <Box mt={2}>
            <Typography variant="h6">Qualitative Score:</Typography>
            <Typography variant="body1">{analysis.qualitative_score}</Typography>
          </Box>
          <Box mt={2}>
            <Typography variant="h6">Ratings:</Typography>
            <Typography variant="body1">Technical Ability: {analysis.ratings?.technical_ability}</Typography>
            <Typography variant="body1">Problem Solving Skills: {analysis.ratings?.problem_solving_skills}</Typography>
          </Box>
          <Box mt={2}>
            <Typography variant="h6">Summary:</Typography>
            <Typography variant="body1">{analysis.summary}</Typography>
          </Box>
        </>
      )}
    </Box>
  );
};

export default Score;

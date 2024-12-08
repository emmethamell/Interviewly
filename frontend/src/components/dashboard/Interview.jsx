import React from 'react';
import { Card, CardContent, Typography, Grid2, Box} from '@mui/material';
import { formatDistanceToNow } from 'date-fns';
const Interview = ({ interview }) => {
  const getDifficultyColor = (difficulty) => {
    return difficulty === "Easy"
      ? "#4caf50"
      : difficulty === "Medium"
        ? "#ffeb3b"
        : "#f44336";
  };

  const getScoreColor = (score) => {
    return score === "Hire"
      ? "#4caf50"
      : score === "No Hire"
        ? "#f44336"
        : score === "Lean Hire"
          ? "#ffeb3b"
          : "#2196f3"; // Strong Hire
  };

  return (
    <Card sx={{ mb: 2, backgroundColor: '#f5f5f5' }}>
      <CardContent>
        <Grid2 container alignItems="center" spacing={0}>
          <Grid2 size={3}>
            <Typography variant="h6" component="div">
              {interview.question_name}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography variant="body2" sx={{ color: getDifficultyColor(interview.question_difficulty) }}>
              {interview.question_difficulty}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography variant="body2" sx={{ color: getScoreColor(interview.score) }}>
              {interview.score}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
          <Box display="flex" justifyContent="flex-end">
            <Typography variant="body2" color="text.secondary">
              {formatDistanceToNow(new Date(interview.date), { addSuffix: true })}
            </Typography>
            </Box>
          </Grid2>
        </Grid2>
      </CardContent>
    </Card>
  );
};

/*
interview.transcript
*/
export default Interview;
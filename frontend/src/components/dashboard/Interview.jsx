import React from "react";
import {
  Card,
  CardContent,
  Typography,
  Grid2,
  Box,
  Button,
} from "@mui/material";
import { formatDistanceToNow, isToday } from "date-fns";
import { styled } from "@mui/material/styles";
import InterviewTranscript from "./InterviewTranscript";
import { useNavigate } from "react-router-dom";

const Interview = ({ interview, index, sx }) => {
  const navigate = useNavigate();
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

  const CardContentNoPadding = styled(CardContent)(`
    padding: 0;
    &:last-child {
      padding-bottom: 0;
    }
  `);

  const handleTranscriptClick = () => {
    navigate(`/transcript/${interview.id}`);
  };

  return (
    <Card sx={{ ...sx, boxShadow: "none" }}>
      <CardContentNoPadding>
        <Grid2 container alignItems="center" spacing={0} p={2}>
          <Grid2 size={3}>
            <Typography
              variant="subtitle2"
              component="div"
              onClick={handleTranscriptClick}
              sx={{
                cursor: "pointer",
                "&:hover": {
                  backgroundColor: index % 2 === 0 ? "#d0d0d0" : "#f0f0f0",
                  color: "#000",
                },
              }}
            >
              {interview.question_name}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography
              variant="body2"
              sx={{ color: getDifficultyColor(interview.question_difficulty) }}
            >
              {interview.question_difficulty}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography
              variant="body2"
              sx={{ color: getScoreColor(interview.score) }}
            >
              {interview.score}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Box display="flex" justifyContent="flex-end">
              <Typography variant="body2" color="text.secondary">
                {isToday(new Date(interview.date))
                  ? "Today"
                  : formatDistanceToNow(new Date(interview.date), {
                      addSuffix: true,
                    })}
              </Typography>
            </Box>
          </Grid2>
        </Grid2>
      </CardContentNoPadding>
    </Card>
  );
};

export default Interview;

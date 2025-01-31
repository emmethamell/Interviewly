import { Card, CardContent, Typography, Grid2, Box } from "@mui/material";
import { formatDistanceToNow, isToday } from "date-fns";
import { styled } from "@mui/material/styles";
import { useNavigate } from "react-router-dom";

const Interview = ({ interview, index, sx }) => {
  const navigate = useNavigate();
  const getDifficultyColor = (difficulty) => {
    return difficulty === "Easy" ? "#4caf50" : difficulty === "Medium" ? "#ffeb3b" : "#f44336";
  };

  const getScoreColor = (score) => {
    switch (score) {
      case "Strong No Hire":
        return "#ef4444"; // Red
      case "No Hire":
        return "#f97316"; // Orange
      case "Lean No Hire":
        return "#facc15"; // Yellow
      case "Lean Hire":
        return "#84cc16"; // Light Green
      case "Hire":
        return "#22c55e"; // Green
      case "Strong Hire":
        return "#15803d"; // Dark Green
      default:
        return "#2196f3"; // Blue
    }
  };

  const getDifficultyStyle = (difficulty) => {
    switch (difficulty) {
      case "Easy":
        return {
          color: "#4caf50", // Green
          fontSize: "0.875rem",
          fontWeight: "bold",
        };
      case "Medium":
        return {
          color: "#ffa000", // Amber
          fontSize: "0.875rem",
          fontWeight: "bold",
        };
      case "Hard":
        return {
          color: "#f44336", // Red
          fontSize: "0.875rem",
          fontWeight: "bold",
        };
      default:
        return {
          fontSize: "0.875rem", // Blue
          fontWeight: "bold",
        };
    }
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
          <Grid2 size={4}>
            <Typography
              variant="body2"
              component="div"
              onClick={handleTranscriptClick}
              sx={{
                cursor: "pointer",
                display: "inline-block",
                fontWeight: "bold",
                textDecoration: "underline",
                "&:hover": {
                  color: "#2196f3",
                },
              }}>
              {interview.question_name}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography
              variant="body2"
              sx={{
                ...getDifficultyStyle(interview.question_difficulty),
              }}>
              {interview.question_difficulty}
            </Typography>
          </Grid2>
          <Grid2 size={3}>
            <Typography
              variant="body2"
              sx={{
                color: getScoreColor(interview.score),
                fontWeight: "bold",
              }}>
              {interview.score}
            </Typography>
          </Grid2>
          <Grid2 size={2}>
            <Typography variant="body2" color="text.secondary">
              {new Date(interview.date).getTime() > Date.now() - 24 * 60 * 60 * 1000
                ? "Today"
                : formatDistanceToNow(new Date(interview.date), {
                    addSuffix: true,
                  })}
            </Typography>
          </Grid2>
        </Grid2>
      </CardContentNoPadding>
    </Card>
  );
};

export default Interview;

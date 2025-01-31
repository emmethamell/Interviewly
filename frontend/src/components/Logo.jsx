import { Box, Typography } from "@mui/material";
import { Terminal } from "@mui/icons-material";

const Logo = () => {
  return (
    <Box display="flex" flexDirection="row" alignItems="center" p={0}>
      <Terminal
        sx={{
          fontSize: 24,
          color: "primary.main",
          padding: "1px",
        }}
      />
      <Typography
        variant="h6"
        sx={{
          color: "primary.main",
          fontWeight: "bold",
          fontSize: "1.1rem",
          padding: "1px",
        }}>
        Interviewly
      </Typography>
    </Box>
  );
};

export default Logo;

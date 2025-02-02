import { Box, Typography } from "@mui/material";
import { TerminalTwoTone } from "@mui/icons-material";

const Logo = () => {
  return (
    <Box display="flex" flexDirection="row" alignItems="center" p={0}>
      <TerminalTwoTone
        sx={{
          fontSize: 35,
          padding: "1px",
          // Changing the color of the terminal svg icon
          "& > path:first-of-type": {
            color: "black",  // Fill
            opacity: "80%"
          },
          "& path:nth-child(2)": {
            color: "primary.main",  // This thing (_)
          },
          "& path:nth-child(3)": {
            color: "primary.main",  // Border
          },
          "& > path:last-of-type": {
            color: "primary.main",  // This thing (>)
          }
        }}
      />
      <Typography
        variant="h6"
        sx={{
          color: "black",
          fontSize: "1.3rem",
          padding: "1px",
        }}>
        codeprep.ai
      </Typography>
    </Box>
  );
};

export default Logo;

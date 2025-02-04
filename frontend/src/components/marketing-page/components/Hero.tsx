import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import InputLabel from "@mui/material/InputLabel";
import Link from "@mui/material/Link";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useAuth0 } from "@auth0/auth0-react";
import { visuallyHidden } from "@mui/utils";
import { styled } from "@mui/material/styles";
import { redirect } from "react-router-dom";

const StyledBox = styled("div")(({ theme }) => ({
  alignSelf: "center",
  width: "100%",
  height: "0",
  paddingTop: "52%",
  position: "relative",
  marginTop: theme.spacing(8),
  borderRadius: (theme.vars || theme).shape.borderRadius,
  outline: "6px solid",
  outlineColor: "hsla(220, 25%, 80%, 0.2)",
  border: "1px solid",
  borderColor: (theme.vars || theme).palette.grey[200],
  boxShadow: "0 0 12px 8px hsla(220, 25%, 80%, 0.2)",
  backgroundImage: `url('../../../../public/Interviewly_Screenshot.png')`,
  backgroundSize: "100% 100%",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",
  [theme.breakpoints.up("sm")]: {
    marginTop: theme.spacing(7),
    width: "100%",
    paddingTop: "52%",
  },
  ...theme.applyStyles("dark", {
    boxShadow: "0 0 24px 12px hsla(210, 100%, 25%, 0.2)",
    backgroundImage: `url(${"https://mui.com"}/static/screenshots/material-ui/getting-started/templates/dashboard-dark.jpg)`,
    outlineColor: "hsla(220, 20%, 42%, 0.1)",
    borderColor: (theme.vars || theme).palette.grey[700],
  }),
}));

export default function Hero() {
  const { loginWithRedirect } = useAuth0();

  const redirectToSignup = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: "signup",
      },
    });
  };

  return (
    <Box
      id="hero"
      sx={(theme) => ({
        width: "100%",
        backgroundRepeat: "no-repeat",
        backgroundImage: "radial-gradient(ellipse 80% 50% at 50% -20%, #, white)",
        ...theme.applyStyles("dark", {
          backgroundImage: "radial-gradient(ellipse 80% 50% at 50% -20%, hsl(210, 100%, 16%), transparent)",
        }),
      })}>
      <Container
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          pt: { xs: 14, sm: 20 },
          pb: { xs: 8, sm: 12 },
        }}>
        <Stack spacing={2} useFlexGap sx={{ alignItems: "center", width: { xs: "100%", sm: "70%" } }}>
          <Stack spacing={-1} alignItems="center">
            <Typography
              variant="h1"
              sx={{
                display: "flex",
                flexDirection: { xs: "column", sm: "row" },
                alignItems: "center",
                fontSize: "clamp(3rem, 10vw, 3.5rem)",
                textAlign: "center",
                mb: 0,
              }}>
              <Typography
                component="span"
                variant="h1"
                sx={{
                  fontSize: "inherit",
                  color: "primary.main",
                }}>
                AI-Powered&nbsp;
              </Typography>
              <Typography
                component="span"
                variant="h1"
                sx={{
                  fontSize: "inherit",
                  color: "black",
                }}>
                Technical&nbsp;
              </Typography>
            </Typography>
            <Typography
              component="span"
              variant="h1"
              sx={{
                color: "black",
                fontSize: "clamp(3rem, 10vw, 3.5rem)",
                mt: 0,
              }}>
              Interview Prep
            </Typography>
          </Stack>
          <Typography
            sx={{
              textAlign: "center",
              color: "text.secondary",
              width: { sm: "100%", md: "80%" },
            }}>
            Simulate real technical interviews with AI. Get follow-up questions and detailed feedback.
          </Typography>

          <Button
            variant="contained"
            color="primary"
            size="small"
            sx={{ minWidth: "fit-content" }}
            onClick={() => redirectToSignup()}>
            Create Account
          </Button>
        </Stack>
        <StyledBox id="image" />
      </Container>
    </Box>
  );
}

import { AppBar, Box, Toolbar, IconButton } from "@mui/material";
import Logo from "../Logo";
import LogoutButton from "../auth/LogoutButton";
import { useNavigate } from "react-router-dom";

const Navbar = () => {
  const navigate = useNavigate();
  const handleLogoClick = () => {
    navigate("/dashboard");
  };
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="#F5F5F5" elevation={1}>
        <Toolbar sx={{ p: "4px" }}>
          {/* Menu Icon */}
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={handleLogoClick}>
            <Logo />
          </IconButton>
          {/* Buttons */}
          <Box sx={{ flexGrow: 1 }} />
          <LogoutButton />
        </Toolbar>
      </AppBar>
    </Box>
  );
};
export default Navbar;

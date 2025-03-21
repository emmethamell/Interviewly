import { useAuth0 } from "@auth0/auth0-react";
import { Button } from "@mui/material";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <Button
      onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
      variant="outlined"
      size="small"
      sx={{
        color: "black",
        borderColor: "primary.main",
        "&:hover": {
          backgroundColor: "primary.main",
          borderColor: "primary.main",
          color: "white",
        },
      }}>
      Log Out
    </Button>
  );
};

export default LogoutButton;

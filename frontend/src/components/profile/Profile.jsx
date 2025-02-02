import { useAuth0 } from "@auth0/auth0-react";
import { Box } from "@mui/material";

const Profile = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    isAuthenticated && (
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </Box>
    )
  );
};

export default Profile;

import React, { useEffect } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const { isAuthenticated, loginWithRedirect } = useAuth0();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
        navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="landing-page">
      <h1>Welcome to Interviewly</h1>
      <p>BLAH BLAH BLAH</p>
      <button onClick={() => loginWithRedirect()}>Get Started</button>
    </div>
  );
};

export default LandingPage;
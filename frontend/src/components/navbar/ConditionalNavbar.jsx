import { useLocation } from "react-router-dom";
import Navbar from "./Navbar";

const ConditionalNavbar = () => {
  const location = useLocation();
  // Where navbar should not be displayed
  const noNavbarRoutes = ["/main", "/"];
  const shouldShowNavbar = !noNavbarRoutes.includes(location.pathname);
  return shouldShowNavbar ? <Navbar /> : null;
};

export default ConditionalNavbar;

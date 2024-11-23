import React from "react";
import SplitPane from "react-split-pane";
import { useLocation } from "react-router-dom";
import { Box } from "@mui/material";
import CodeEditor from "./CodeEditor";
import AIChat from "./AIChat";

const Layout = () => {
  const location = useLocation();
  const { difficulty } = location.state || { difficulty: "Easy" };

  return (
    <Box
      sx={{
        height: "100%", // Inherit height from parent
        overflow: "hidden",
        bgcolor: "#1e1e1e",
      }}
    >
      <SplitPane
        split="vertical"
        minSize={200}
        defaultSize="35%"
        className="custom-split-pane"
        style={{
          width: "100%",
          height: "100%",
        }}
      >
        {/* Left Pane */}
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <AIChat difficulty={difficulty} />
        </Box>

        {/* Right Pane */}
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <CodeEditor difficulty={difficulty}/>
        </Box>
      </SplitPane>
    </Box>
  );
};

export default Layout;

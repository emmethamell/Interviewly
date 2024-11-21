import React from "react";
import SplitPane from "react-split-pane";
import { Box } from "@mui/material";
import CodeEditor from "./CodeEditor";
import AIChat from "./AIChat";

const Layout = () => {
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
          <AIChat />
        </Box>

        {/* Right Pane */}
        <Box sx={{ height: "100%", overflow: "auto" }}>
          <CodeEditor />
        </Box>
      </SplitPane>
    </Box>
  );
};

export default Layout;

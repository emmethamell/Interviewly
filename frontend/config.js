const config = {
    apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:5001',
    wsUrl: import.meta.env.VITE_WS_URL || 'ws://localhost:5001',
    auth0: {
      domain: import.meta.env.VITE_AUTH0_DOMAIN,
      clientId: import.meta.env.VITE_AUTH0_CLIENT_ID,
      redirectUri: `${window.location.origin}/dashboard`,
    }
  };
  
  export default config;
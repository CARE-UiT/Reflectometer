import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import DrawLineChart from './DrawLineChart';

const theme = createTheme();

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <DrawLineChart />
    </ThemeProvider>
  );
};

export default App;

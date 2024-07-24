import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import AppAppBar from './components/AppAppBar';
import { PaletteMode } from '@mui/material';

const theme = createTheme();

const App = (props: { children: React.ReactNode }): React.ReactNode => {
  const [mode, setMode] = React.useState<PaletteMode>('light');
  const toggleColorMode = () => {
    setMode((prev) => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppAppBar mode={mode} toggleColorMode={toggleColorMode} />
      {props.children}
    </ThemeProvider>
  );
};

export default App;

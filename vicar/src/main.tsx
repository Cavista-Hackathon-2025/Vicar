  import './index.css'
  import '@mantine/core/styles.css';
  import { createRoot } from 'react-dom/client';
  import { MantineProvider } from '@mantine/core';
  import { BrowserRouter } from 'react-router-dom';
  import App from './App.tsx';
  const root = createRoot(document.getElementById("root")!);
  root.render(
    <MantineProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </MantineProvider>

  );
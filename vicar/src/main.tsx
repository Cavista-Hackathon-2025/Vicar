import '@mantine/core/styles.css';
import './index.css'
import * as React from "react";
import { createRoot } from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './routes.tsx';
import { MantineProvider } from '@mantine/core';
const root = createRoot(document.getElementById("root"));
root.render(
  

    <React.StrictMode>
      <MantineProvider><RouterProvider router={router} /></MantineProvider>

    </React.StrictMode>
  

);
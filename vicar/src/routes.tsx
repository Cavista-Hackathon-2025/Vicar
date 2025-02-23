
import {
    createBrowserRouter,
} from "react-router";

import { Dashboard } from "./pages/auth/dashboard";
import { Index } from "./pages";

export const router = createBrowserRouter([
    {
        path: "/",
        element: <Index />,

    },
    {
        path: "dashboard",
        element: <Dashboard />,
    }
]);




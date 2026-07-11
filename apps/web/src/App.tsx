import { RouterProvider } from "react-router-dom";

import { PhaseTwoProvider } from "./pages";
import { router } from "./router";

export default function App() {
  return (
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>
  );
}

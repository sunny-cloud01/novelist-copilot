import { RouterProvider } from "react-router-dom";

import { router } from "./router";
import { PhaseTwoProvider } from "./state/phase-two-provider";

export default function App() {
  return (
    <PhaseTwoProvider>
      <RouterProvider router={router} />
    </PhaseTwoProvider>
  );
}

import { Suspense } from "react";
import SignInClient from "./signin-client";

export default function SignInPage() {
  return (
    <Suspense fallback={<div>Loading sign-in…</div>}>
      <SignInClient />
    </Suspense>
  );
}

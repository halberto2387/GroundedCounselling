import type { Metadata } from "next";
import "./globals.css";

import { ThemeProvider } from "@grounded-counselling/ui";

export const metadata: Metadata = {
  title: "GroundedCounselling",
  description: "Professional counselling practice management system",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className="font-sans antialiased"
      >
        <ThemeProvider
          defaultTheme="system"
          storageKey="grounded-counselling-theme"
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}

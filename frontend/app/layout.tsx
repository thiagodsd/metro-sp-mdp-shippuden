import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Metro SP MDP",
  description: "Markov Decision Process for São Paulo Metro System",
  keywords: "metro, sao paulo, mdp, route planning",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}

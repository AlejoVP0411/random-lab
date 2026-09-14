import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = { title: "Random Lab", description: "Generador y pruebas de números pseudoaleatorios" };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="es"><body>{children}</body></html>; }

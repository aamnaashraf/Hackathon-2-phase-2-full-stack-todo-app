"use client"

import * as React from "react"
import { ThemeProvider as NextThemesProvider } from "next-themes"

// TypeScript ke liye safe children type
type ThemeProviderProps = {
  children: React.ReactNode
  attribute?: "class" | "data-theme"
  defaultTheme?: string
  enableSystem?: boolean
}

export function ThemeProvider({
  children,
  ...props
}: ThemeProviderProps) {
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>
}

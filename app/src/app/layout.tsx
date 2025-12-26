import '../styles/globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/src/lib/auth'
import { ToastProvider } from '@/src/lib/toast'
import Navigation from './components/Navigation'
import { ThemeProvider } from '@/src/app/components/theme-provider'


const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A secure todo application with user authentication',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning className="scroll-smooth">
      <body className={`
        ${inter.className}
        bg-white dark:bg-gradient-to-br dark:from-indigo-950 dark:via-purple-950 dark:to-pink-950
        text-gray-900 dark:text-white
        min-h-screen w-full min-w-0
        transition-colors duration-300
      `}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <ToastProvider>
            <AuthProvider>
              <Navigation />
              <main className="container mx-auto px-4 py-8 min-h-[calc(100vh-4rem)]">
                {children}
              </main>
            </AuthProvider>
          </ToastProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
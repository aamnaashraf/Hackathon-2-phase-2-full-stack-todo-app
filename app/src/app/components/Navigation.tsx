'use client';

import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { LogOut, LogIn, User, Menu, X, Sun, Moon } from 'lucide-react';

export default function Navigation() {
  const pathname = usePathname();
  const [isClient, setIsClient] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false); // default to light mode initially, will be corrected by useEffect

  useEffect(() => {
    setIsClient(true);

    // Load saved theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      const isDark = savedTheme === 'dark';
      setIsDarkMode(isDark);
      document.documentElement.classList.toggle('dark', isDark);
    } else {
      // Default to dark
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    }

    // Auth check (demo logic)
    if (pathname && !pathname.includes('/login') && !pathname.includes('/register') && pathname !== '/') {
      setIsLoggedIn(true);
    } else if (pathname === '/') {
      setIsLoggedIn(false);
    }
  }, [pathname]);

  const toggleTheme = () => {
    const newTheme = !isDarkMode;
    setIsDarkMode(newTheme);
    if (newTheme) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', newTheme ? 'dark' : 'light');
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  if (!isClient) return null;

  return (
    <nav className="backdrop-blur-md bg-black/30 dark:bg-black/40 border-b border-white/10 dark:border-white/5 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <div className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent">
                TodoApp
              </div>
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-6 lg:space-x-8">
            {!isLoggedIn ? (
              <>
                <Link
                  href="/login"
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                    pathname === '/login'
                      ? 'bg-indigo-600/20 text-indigo-300 shadow-lg'
                      : 'text-white/80 dark:text-white/90 hover:text-white hover:bg-white/10 dark:hover:bg-white/5'
                  }`}
                >
                  <LogIn className="w-4 h-4 inline mr-2" />
                  Login
                </Link>
                <Link
                  href="/register"
                  className={`px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105`}
                >
                  <User className="w-4 h-4 inline mr-2" />
                  Sign Up
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/dashboard"
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                    pathname === '/dashboard'
                      ? 'bg-purple-600/20 text-purple-300 shadow-lg'
                      : 'text-white/80 dark:text-white/90 hover:text-white hover:bg-white/10 dark:hover:bg-white/5'
                  }`}
                >
                  Dashboard
                </Link>
                <button
                  onClick={() => {
                    setIsLoggedIn(false);
                    setIsMobileMenuOpen(false);
                  }}
                  className="flex items-center space-x-2 px-4 py-2 text-white/80 dark:text-white/90 hover:text-white hover:bg-red-600/20 rounded-lg transition-all duration-300"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            )}

            {/* Theme Toggle - Desktop */}
            <button
              onClick={toggleTheme}
              className="p-2.5 rounded-full bg-white/10 dark:bg-white/5 hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300 transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              aria-label="Toggle dark/light mode"
            >
              {isDarkMode ? (
                <Sun className="w-5 h-5 text-yellow-300" />
              ) : (
                <Moon className="w-5 h-5 text-indigo-300" />
              )}
            </button>
          </div>

          {/* Mobile: Theme Toggle + Menu Button */}
          <div className="md:hidden flex items-center space-x-4">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-full bg-white/10 dark:bg-white/5 hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300"
              aria-label="Toggle dark/light mode"
            >
              {isDarkMode ? (
                <Sun className="w-5 h-5 text-yellow-300" />
              ) : (
                <Moon className="w-5 h-5 text-indigo-300" />
              )}
            </button>

            <button
              onClick={toggleMobileMenu}
              className="text-white/80 hover:text-white p-2 rounded-lg hover:bg-white/10 transition"
            >
              {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-white/10 dark:border-white/5 bg-black/40 backdrop-blur-md">
          <div className="px-4 py-6 space-y-4">
            {!isLoggedIn ? (
              <>
                <Link
                  href="/login"
                  className="flex items-center space-x-3 px-4 py-3 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <LogIn className="w-5 h-5" />
                  <span>Login</span>
                </Link>
                <Link
                  href="/register"
                  className="flex items-center space-x-3 px-4 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg transition"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <User className="w-5 h-5" />
                  <span>Sign Up</span>
                </Link>
              </>
            ) : (
              <>
                <Link
                  href="/dashboard"
                  className="block px-4 py-3 text-white/90 hover:text-white hover:bg-white/10 rounded-lg transition"
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  Dashboard
                </Link>
                <button
                  onClick={() => {
                    setIsLoggedIn(false);
                    setIsMobileMenuOpen(false);
                  }}
                  className="w-full text-left px-4 py-3 text-white/90 hover:text-white hover:bg-red-600/20 rounded-lg transition flex items-center space-x-3"
                >
                  <LogOut className="w-5 h-5" />
                  <span>Logout</span>
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
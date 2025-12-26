// app/page.tsx
'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion'; 
import HowItWorks from './components/Howitworks';
import JoinThousands from './components/JoinThousands';
import { Twitter, Instagram, Mail, Github } from 'lucide-react';

export default function HomePage() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) return null; // avoid hydration mismatch

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Background subtle pattern */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="w-full h-full bg-[radial-gradient(circle_at_10%_20%,rgba(255,255,255,0.1)_0%,transparent_50%)]" />
      </div>

      {/* Main Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        

        {/* Hero Section */}
        <main className="flex-1 flex items-center justify-center px-6 py-12">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="text-center max-w-4xl"
          >
            <h1 className="text-4xl md:text-7xl lg:text-8xl font-extrabold tracking-tight leading-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-800 via-blue-900 to-pink-700 dark:from-indigo-400 dark:via-purple-300 dark:to-pink-300">
              Manage Your Tasks<br className="hidden md:block" /> Effortlessly
            </h1>

            <p className="text-xl md:text-2xl text-gray-700 dark:text-white/80 mb-12 max-w-3xl mx-auto leading-relaxed">
              A secure, fast, and beautifully designed todo app to organize your life, boost productivity, and stay focused.
            </p>

            <div className="flex flex-col sm:flex-row gap-5 justify-center items-center">
              <Link
                href="/register"
                className="group relative px-10 py-5 bg-indigo-600 hover:bg-indigo-500 rounded-xl font-semibold text-lg shadow-2xl shadow-indigo-600/40 transition-all duration-300 hover:scale-[1.03] hover:shadow-indigo-500/60"
              >
                Get Started Free
                <span className="absolute inset-0 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 opacity-0 group-hover:opacity-20 transition-opacity" />
              </Link>

              <Link
  href="/login"
  className={`
    px-10 py-5 
    bg-white/70 dark:bg-gray-900/40 
    backdrop-blur-md 
    border border-gray-300/50 dark:border-indigo-500/30 
    rounded-xl 
    font-semibold text-lg 
    text-gray-900 dark:text-gray-100
    hover:bg-white/90 dark:hover:bg-gray-900/60 
    hover:border-indigo-400/60 dark:hover:border-indigo-400/50 
    hover:shadow-lg hover:shadow-indigo-400/30 dark:hover:shadow-indigo-500/30 
    transition-all duration-300 hover:scale-[1.03] active:scale-[0.98]
  `}
>
  Already have an account? Login
</Link>
            </div>

{/* Trust signals / features */}
<div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 md:gap-10">
  {[
    { icon: "🔒", title: "Secure & Private", desc: "End-to-end encryption & zero data sharing" },
    { icon: "⚡", title: "Lightning Fast", desc: "Instant sync across all your devices" },
    { icon: "📱", title: "Fully Responsive", desc: "Perfect on phone, tablet & desktop" },
    { icon: "🌙", title: "Dark Mode", desc: "Beautiful dark theme that’s easy on the eyes" },
  ].map((item, i) => (
    <motion.div
      key={i}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: i * 0.1 }}
      viewport={{ once: true }}
      whileHover={{
        scale: 1.08,
        y: -10,
        transition: { duration: 0.3, ease: "easeOut" },
      }}
      className="group relative overflow-hidden rounded-3xl bg-white/80 dark:bg-gradient-to-br dark:from-blue-900/80 dark:via-purple-950/60 dark:to-purple-950/50 backdrop-blur-xl border border-gray-200 dark:border-gray-700/50 hover:border-indigo-500/60 hover:bg-white/100 dark:hover:bg-gradient-to-br dark:hover:from-indigo-950/70 dark:hover:via-purple-950/60 dark:hover:to-pink-950/40 shadow-lg shadow-gray-200/50 dark:shadow-black/40 hover:shadow-xl dark:hover:shadow-indigo-500/40 transition-all duration-500 min-h-[220px] md:min-h-[260px] flex flex-col justify-center"
    >
      {/* Subtle inner glow on hover */}
      <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/0 via-purple-500/0 to-pink-500/0 group-hover:from-indigo-500/10 group-hover:via-purple-500/10 group-hover:to-pink-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

      <div className="relative z-10 p-8 md:p-10 text-center flex flex-col items-center justify-center h-full">
        <div className="text-6xl md:text-7xl mb-6 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-400 ease-out">
          {item.icon}
        </div>

        <h3 className="text-xl md:text-2xl font-semibold text-gray-800 dark:text-white mb-4 group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors duration-300">
          {item.title}
        </h3>

        <p className="text-gray-600 dark:text-gray-300 text-base md:text-lg group-hover:text-gray-800 dark:group-hover:text-gray-100 transition-colors duration-300 leading-relaxed">
          {item.desc}
        </p>
      </div>
    </motion.div>
  ))}
</div>

          </motion.div>
        </main>

        <HowItWorks />
        <JoinThousands />
        

        {/* Footer */}
<footer className="py-12 px-6 md:px-12 bg-gradient-to-t from-gray-100/80 to-white dark:from-gray-950 dark:to-gray-900 border-t border-gray-200/80 dark:border-indigo-500/20">
  <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-10">
    {/* Left: Logo & Tagline */}
    <div className="text-center md:text-left">
      <Link href="/" className="inline-block mb-4">
        <div className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent dark:from-indigo-400 dark:via-purple-400 dark:to-pink-400">
          TodoApp
        </div>
      </Link>
      <p className="text-gray-600 dark:text-gray-400 text-sm max-w-xs mx-auto md:mx-0">
        Organize your life with secure, fast, and beautiful task management.
      </p>
    </div>

    {/* Center: Quick Links */}
    <div className="text-center">
      <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
        Quick Links
      </h4>
      <div className="flex flex-col gap-3 text-sm">
        <Link href="/dashboard" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition">
          Dashboard
        </Link>
        <Link href="/privacy" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition">
          Privacy Policy
        </Link>
        <Link href="/terms" className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition">
          Terms of Service
        </Link>
      </div>
    </div>

    {/* Right: Social / Contact */}
    <div className="text-center md:text-right">
      <h4 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
        Connect With Us
      </h4>
    

<div className="flex justify-center md:justify-end gap-6">
  <a 
    href="https://github.com/aamnaashraf" 
    target="_blank" 
    rel="noopener noreferrer"
    className="text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-300 transition transform hover:scale-110"
    title="View on GitHub"
  >
    <Github className="w-6 h-6" /> {/* lucide-react GitHub icon */}
  </a>
</div>
      <p className="mt-4 text-sm text-gray-500 dark:text-gray-500">
        © {new Date().getFullYear()} TodoApp. Made with ❤️
      </p>
    </div>
  </div>
</footer>


      </div>
    </div>
  );
}
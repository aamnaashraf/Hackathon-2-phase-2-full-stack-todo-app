// components/HowItWorksSection.tsx
import { motion } from 'framer-motion';

const steps = [
  {
    number: 1,
    title: "Sign Up",
    desc: "Create your account in seconds with just an email and password.",
  },
  {
    number: 2,
    title: "Add Tasks",
    desc: "Quickly capture your ideas, tasks, and goals anytime.",
  },
  {
    number: 3,
    title: "Organize",
    desc: "Categorize, prioritize, and set due dates effortlessly.",
  },
  {
    number: 4,
    title: "Stay Productive",
    desc: "Track progress, get reminders, and achieve more every day.",
  },
];

export default function HowItWorksSection() {
  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-b from-gray-50 to-white dark:from-purple-900 dark:to-gray-900 border-t border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto">
        {/* Section Heading */}
        <motion.h2
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-4xl sm:text-5xl font-extrabold text-center mb-16 bg-gradient-to-r from-blue-400 via-purple-600 to-pink-500 bg-clip-text text-transparent dark:from-indigo-400 dark:via-purple-500 dark:to-pink-800"
        >
          How It Works
        </motion.h2>

        {/* Steps Grid */}
        <div className="grid md:grid-cols-4 gap-6 lg:gap-8 relative">
          {/* Connecting Line (only on desktop) */}
          <div className="hidden md:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-indigo-300/40 via-purple-300/40 to-pink-300/40 dark:from-indigo-500/30 dark:via-purple-500/30 dark:to-pink-500/30 rounded-full" />

          {steps.map((step, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              whileInView={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.7, delay: i * 0.15, ease: "easeOut" }}
              viewport={{ once: true }}
              whileHover={{
                scale: 1.07,
                y: -10,
                boxShadow: "0 25px 50px -12px rgba(79, 70, 229, 0.4)",
                transition: { duration: 0.4 },
              }}
              className="relative z-10 group"
            >
              <div
                className={`
                  h-full bg-white/95 dark:bg-gradient-to-br dark:from-indigo-800/70 dark:via-purple-800/60 dark:to-pink-800/50
                  backdrop-blur-xl border border-gray-200/70 dark:border-indigo-400/30
                  rounded-3xl p-8 lg:p-10 shadow-lg shadow-gray-300/40 dark:shadow-indigo-500/20
                  group-hover:border-indigo-400/70 dark:group-hover:border-indigo-400/60
                  group-hover:shadow-2xl group-hover:shadow-indigo-400/40 dark:group-hover:shadow-indigo-500/40
                  transition-all duration-500 flex flex-col items-center justify-center
                  min-h-[260px] md:min-h-[300px]
                `}
              >
                {/* Number Circle */}
                <div className="w-20 h-20 md:w-24 md:h-24 mx-auto mb-6 rounded-full bg-gradient-to-br from-indigo-500 to-purple-800 flex items-center justify-center text-white text-4xl md:text-5xl font-extrabold shadow-xl group-hover:scale-110 group-hover:shadow-indigo-500/50 transition-all duration-400">
                  {step.number}
                </div>

                {/* Title */}
                <h3 className="text-xl md:text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4 group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors duration-300">
                  {step.title}
                </h3>

                {/* Description */}
                <p className="text-gray-600 dark:text-gray-300 text-base md:text-lg leading-relaxed text-center group-hover:text-gray-800 dark:group-hover:text-gray-100 transition-colors duration-300">
                  {step.desc}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
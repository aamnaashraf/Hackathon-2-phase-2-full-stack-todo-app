// components/JoinThousandsSection.tsx
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function JoinThousandsSection() {
  return (
    <section className="py-16 md:py-20 px-6 bg-gradient-to-b from-transparent via-gray-100/30 to-gray-200/40 dark:via-purple-950/30 dark:to-indigo-950/20 border-t border-gray-200 dark:border-white/10">
      <div className="max-w-4xl mx-auto text-center">
        <motion.h2
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl lg:text-5xl font-bold mb-8 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent"
        >
          Join Thousands of Productive People
        </motion.h2>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.2 }}
          viewport={{ once: true }}
          className="text-lg md:text-xl text-gray-600 dark:text-gray-200 mb-12 max-w-3xl mx-auto leading-relaxed"
        >
          People just like you are using TodoApp to stay organized, hit their goals, and reclaim their time every single day.
        </motion.p>

        {/* Simple stats / badges */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 md:gap-10">
          {[
            { number: "50K+", label: "Active Users" },
            { number: "1M+", label: "Tasks Managed" },
            { number: "4.9", label: "App Rating" },
            { number: "100%", label: "Secure" },
          ].map((stat, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              viewport={{ once: true }}
              className="bg-white/80 dark:bg-white/5 backdrop-blur-lg border border-gray-200 dark:border-white/10 rounded-2xl p-6 text-center hover:border-indigo-500/40 transition-all duration-300 hover:shadow-lg hover:shadow-indigo-500/20"
            >
              <div className="text-3xl md:text-4xl font-bold text-indigo-600 dark:text-indigo-300 mb-2">
                {stat.number}
              </div>
              <p className="text-gray-600 dark:text-gray-400 text-sm md:text-base font-medium">
                {stat.label}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Final CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-12"
        >
          <Link
            href="/register"
            className="inline-block px-10 py-5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-lg rounded-xl shadow-2xl shadow-indigo-600/40 hover:shadow-indigo-500/60 transition-all duration-300 transform hover:scale-105"
          >
            Join Them Today – It's Free
          </Link>
        </motion.div>
      </div>
    </section>
  );
}
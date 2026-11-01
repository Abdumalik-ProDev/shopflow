import type { Config } from "tailwindcss";

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        indigo: {
          900: "#1e1b4b",
          950: "#0f0a2a",
        },
        charcoal: {
          900: "#18181b",
          800: "#27272a",
        },
        cream: {
          50: "#fafaf9",
          100: "#f5f5f4",
        },
        amber: {
          500: "#d97706",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Playfair Display", "serif"],
      },
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
          },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#090D16",
        surface: "#111827",
        border: "#1F2937",
        primary: "#3B82F6",
        accent: "#10B981",
      },
    },
  },
  plugins: [],
}

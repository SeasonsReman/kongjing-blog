/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#3617cf",
        "background-light": "#f6f6f8",
        "background-dark": "#141121",
      },
      fontFamily: {
        display: ["Manrope", "sans-serif"],
        serif: ["Noto Serif SC", "serif"],
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      backdropBlur: {
        xs: "2px",
      },
    },
  },
  plugins: [],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bgApp: "rgba(135, 171, 243, 0.88)",
      },
    },
  },
  plugins: [],
}
  
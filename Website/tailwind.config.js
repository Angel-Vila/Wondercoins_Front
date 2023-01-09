/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.{html,js}"],
  theme: {
      colors: {
          "fondo": "#d4dfdf",
          "cabecera": "#03989e"
      },
        extend: {
          fontFamily: {
              "josefin": ["Josefin Sans", "sans-serif"],
              "alice": ["Alice", "serif"]
          }
        },
  },
  plugins: [require("daisyui")],
}

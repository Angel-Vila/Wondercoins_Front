/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.{html,js}"],
  theme: {
      colors: {
          "fondo": "#d4dfdf",
          "cabecera": "#03989e",
          "blanco": "#FFFFFF",
      },
        extend: {
          fontFamily: {
              "josefin": ["Josefin Sans", "sans-serif"],
              "alice": ["Alice", "serif"]
          },
            backgroundImage: {
              "wondercoins": "../static/logo-sinletras-sinfondo.jpg"
            }
        },
  },
  plugins: [require("daisyui")],
}

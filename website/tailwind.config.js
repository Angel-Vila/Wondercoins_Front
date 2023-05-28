/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.{html,js}"],
  theme: {
      colors: {
          "fondo": "#d4dfdf",
          "cabecera": "#03989e",
          "blanco": "#FFFFFF",
          "fondo_barra": "#e5e5e5"
      },
        extend: {
          fontFamily: {
              "josefin": ["Josefin Sans", "sans-serif"],
              "alice": ["Alice", "serif"]
          },
            backgroundImage: {
              "wondercoins": "url('../WONDERLOGO_fondo.png')"
            }
        },
  },
  plugins: [require("daisyui")],
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#F5A623',
        'primary-light': '#FFB347',
        background: '#FAF8F5',
        card: '#FFFFFF',
        'text-muted': '#888888',
        accent: '#FFB6C1',
        success: '#98D8AA',
        error: '#FF6B6B',
      },
      borderRadius: {
        'sm': '8px',
        'md': '12px',
        'lg': '16px',
      },
      boxShadow: {
        'sm': '0 2px 4px rgba(0,0,0,0.06)',
        'md': '0 4px 8px rgba(0,0,0,0.08)',
        'lg': '0 8px 16px rgba(0,0,0,0.12)',
      },
    },
  },
  plugins: [],
}

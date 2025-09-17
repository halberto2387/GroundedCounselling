import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    '../packages/ui/src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Brand Primary Colors (Evergreen)
        primary: {
          50: '#f0f9f4',
          100: '#dcf2e4',
          200: '#bce4cd',
          300: '#8dd0ab',
          400: '#56b382',
          500: '#2E6F4E', // Evergreen - main brand color
          600: '#265a40',
          700: '#1f4832',
          800: '#1a3a29',
          900: '#162f22',
        },
        
        // Surface/Background Colors (Sand)
        surface: {
          50: '#fefffe',
          100: '#fdfdfc',
          200: '#faf8f6',
          300: '#f7f4f0',
          400: '#f6f2ed',
          500: '#F5F1EA', // Sand - main surface color
          600: '#e8ddc9',
          700: '#dbc9a8',
          800: '#ceb587',
          900: '#c1a166',
        },
        
        // Neutral Colors (Charcoal)
        neutral: {
          50: '#f9f9f9',
          100: '#f3f3f3',
          200: '#e7e7e7',
          300: '#dbdbdb',
          400: '#c4c4c4',
          500: '#adadad',
          600: '#969696',
          700: '#7f7f7f',
          800: '#3f3f3f',
          900: '#1E1E1E', // Charcoal
        },
        
        // Slate Colors
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#6B7280', // Slate
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        
        // Sky Colors
        sky: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#3BA6FF', // Sky
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        
        // CSS variables for theme switching
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Source Serif 4', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
};

export default config;
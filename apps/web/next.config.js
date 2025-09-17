/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  transpilePackages: ['@grounded-counselling/ui', '@grounded-counselling/sdk'],
  output: 'standalone',
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: true,
  },
  
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-eval' https://meet.jit.si https://*.sentry.io",
              "style-src 'self' 'unsafe-inline'",
              "img-src 'self' data: https:",
              "font-src 'self' data:",
              "connect-src 'self' https://api.groundedcounselling.com https://*.sentry.io",
              "frame-src 'self' https://meet.jit.si",
              "frame-ancestors 'none'",
              "object-src 'none'",
              "base-uri 'self'",
              "upgrade-insecure-requests"
            ].join('; ')
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin'
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=self https://meet.jit.si, microphone=self https://meet.jit.si, geolocation=()'
          }
        ]
      }
    ];
  },
  
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env['NEXT_PUBLIC_API_BASE_URL'] || 'http://localhost:8000'}/:path*`
      }
    ];
  }
};

module.exports = nextConfig;

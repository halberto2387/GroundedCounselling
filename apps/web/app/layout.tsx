import { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'GroundedCounselling',
  description: 'A secure, HIPAA-compliant platform for counselling practice management',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
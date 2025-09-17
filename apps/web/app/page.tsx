'use client';

import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import Link from 'next/link';

import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';
import '../lib/i18n';

export default function Home() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      {/* Navigation */}
      <nav className="border-b bg-surface-50/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-xl font-bold text-primary-600">
                GroundedCounselling
              </Link>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/services" className="text-neutral-600 hover:text-primary-600">
                {t('navigation.services')}
              </Link>
              <Link href="/specialists" className="text-neutral-600 hover:text-primary-600">
                {t('navigation.specialists')}
              </Link>
              <Link href="/book" className="text-neutral-600 hover:text-primary-600">
                {t('navigation.book')}
              </Link>
              <Link href="/blog" className="text-neutral-600 hover:text-primary-600">
                {t('navigation.blog')}
              </Link>
              <Link href="/auth/signin" className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700">
                {t('auth.signIn')}
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-6xl font-bold text-neutral-900 mb-6 font-serif">
            {t('welcome')}
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto leading-relaxed">
            {t('description')}
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-12">
          <Card>
            <CardHeader>
              <CardTitle>For Counsellors</CardTitle>
              <CardDescription>
                Manage your practice with integrated tools for client management, scheduling, and billing.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-neutral-600">
                <li>• Client management system</li>
                <li>• Integrated video sessions</li>
                <li>• Practice analytics</li>
                <li>• Secure billing</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>For Clients</CardTitle>
              <CardDescription>
                Find the right counsellor and book sessions that fit your schedule and needs.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-neutral-600">
                <li>• Easy booking system</li>
                <li>• Secure video sessions</li>
                <li>• Session history</li>
                <li>• Mental health resources</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Security & Compliance</CardTitle>
              <CardDescription>
                Built with healthcare compliance in mind, ensuring your data is always protected.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-neutral-600">
                <li>• HIPAA-ready infrastructure</li>
                <li>• End-to-end encryption</li>
                <li>• Comprehensive audit logs</li>
                <li>• GDPR compliant</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        {/* CTA Section */}
        <div className="text-center">
          <div className="space-x-4">
            <Link
              href="/book"
              className="bg-primary-600 text-white px-8 py-3 rounded-md text-lg font-medium hover:bg-primary-700 transition-colors"
            >
              Book a Session
            </Link>
            <Link
              href="/services"
              className="border border-primary-600 text-primary-600 px-8 py-3 rounded-md text-lg font-medium hover:bg-primary-50 transition-colors"
            >
              Learn More
            </Link>
          </div>
        </div>
      </main>
    </div>
  );
}

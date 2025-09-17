'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function TwoFactorAuthPage() {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Mock 2FA verification - in real app, this would call the API
    console.log('2FA verification attempt:', { code });
    
    // Simulate API call
    setTimeout(() => {
      setIsLoading(false);
      alert('Two-factor authentication not yet implemented - this is a placeholder');
    }, 1000);
  };

  const handleResendCode = () => {
    alert('Resend functionality not yet implemented');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <Link href="/" className="text-2xl font-bold text-primary-600">
            GroundedCounselling
          </Link>
          <h2 className="mt-6 text-3xl font-bold text-neutral-900">
            Two-Factor Authentication
          </h2>
          <p className="mt-2 text-sm text-neutral-600">
            Enter the verification code from your authenticator app
          </p>
        </div>

        <Card>
          <CardContent className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label htmlFor="code" className="block text-sm font-medium text-neutral-700">
                  Verification Code
                </label>
                <input
                  id="code"
                  name="code"
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  maxLength={6}
                  required
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                  className="mt-1 block w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 text-center text-2xl tracking-widest"
                  placeholder="000000"
                />
                <p className="mt-2 text-xs text-neutral-500">
                  Enter the 6-digit code from your authenticator app
                </p>
              </div>

              <button
                type="submit"
                disabled={isLoading || code.length !== 6}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Verifying...' : 'Verify'}
              </button>
            </form>

            <div className="mt-6 text-center">
              <p className="text-sm text-neutral-600">
                Didn't receive a code?{' '}
                <button
                  type="button"
                  onClick={handleResendCode}
                  className="text-primary-600 hover:text-primary-700 font-medium"
                >
                  Resend
                </button>
              </p>
            </div>

            <div className="mt-4 text-center">
              <Link 
                href="/auth/signin" 
                className="text-sm text-neutral-600 hover:text-neutral-900"
              >
                ← Back to sign in
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
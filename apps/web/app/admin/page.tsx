'use client';

import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function AdminPage() {
  const [isAuthorized, setIsAuthorized] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Mock authentication check - in real app, this would verify admin role
    const checkAuth = () => {
      setTimeout(() => {
        setIsLoading(false);
        // For demo purposes, always return false (not authorized)
        setIsAuthorized(false);
      }, 1000);
    };

    checkAuth();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-4 text-neutral-600">Checking authorization...</p>
        </div>
      </div>
    );
  }

  if (!isAuthorized) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200 flex items-center justify-center">
        <Card className="max-w-md">
          <CardHeader>
            <CardTitle className="text-center text-red-600">Access Denied</CardTitle>
            <CardDescription className="text-center">
              You do not have permission to access this area.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="text-center space-y-4">
              <p className="text-neutral-600 text-sm">
                Admin access requires proper authentication and authorization.
              </p>
              <div className="space-y-2">
                <a
                  href="/auth/signin"
                  className="block w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition-colors"
                >
                  Sign In
                </a>
                <a
                  href="/"
                  className="block w-full border border-neutral-300 text-neutral-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-neutral-50 transition-colors"
                >
                  Go Home
                </a>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // This would be the actual admin interface when authorized
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Admin Dashboard
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            System administration and management tools.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>User Management</CardTitle>
              <CardDescription>
                Manage user accounts, roles, and permissions
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600 mb-4">
                View and manage all user accounts, assign roles, and configure access permissions.
              </p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                Manage Users
              </button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>System Settings</CardTitle>
              <CardDescription>
                Configure system-wide settings and preferences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600 mb-4">
                Update system configuration, email settings, and integration preferences.
              </p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                System Settings
              </button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Analytics</CardTitle>
              <CardDescription>
                View system usage and performance metrics
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600 mb-4">
                Monitor system performance, user activity, and generate reports.
              </p>
              <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                View Analytics
              </button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
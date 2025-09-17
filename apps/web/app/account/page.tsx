import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function AccountPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            My Account
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Manage your account settings and preferences.
          </p>
        </div>

        <div className="max-w-4xl mx-auto grid md:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>
                Update your personal information and contact details
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-neutral-700 mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    placeholder="Enter your full name"
                    className="w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    disabled
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-neutral-700 mb-1">
                    Email Address
                  </label>
                  <input
                    type="email"
                    placeholder="Enter your email"
                    className="w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    disabled
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-neutral-700 mb-1">
                    Phone Number
                  </label>
                  <input
                    type="tel"
                    placeholder="Enter your phone number"
                    className="w-full px-3 py-2 border border-neutral-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                    disabled
                  />
                </div>
                <button className="w-full bg-neutral-300 text-neutral-500 px-4 py-2 rounded-md text-sm cursor-not-allowed">
                  Update Profile (Coming Soon)
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Security Settings</CardTitle>
              <CardDescription>
                Manage your password and security preferences
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-neutral-900 mb-2">Password</h4>
                  <p className="text-sm text-neutral-600 mb-3">
                    Last changed 3 months ago
                  </p>
                  <button className="w-full border border-neutral-300 text-neutral-700 px-4 py-2 rounded-md text-sm hover:bg-neutral-50 cursor-not-allowed">
                    Change Password (Coming Soon)
                  </button>
                </div>
                <div>
                  <h4 className="font-medium text-neutral-900 mb-2">Two-Factor Authentication</h4>
                  <p className="text-sm text-neutral-600 mb-3">
                    Add an extra layer of security to your account
                  </p>
                  <button className="w-full border border-neutral-300 text-neutral-700 px-4 py-2 rounded-md text-sm hover:bg-neutral-50 cursor-not-allowed">
                    Enable 2FA (Coming Soon)
                  </button>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Appointment History</CardTitle>
              <CardDescription>
                View your past and upcoming appointments
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center py-8">
                  <p className="text-neutral-500 text-sm">
                    No appointments found
                  </p>
                  <p className="text-neutral-400 text-xs mt-2">
                    Your appointment history will appear here
                  </p>
                </div>
                <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                  Book New Appointment
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Preferences</CardTitle>
              <CardDescription>
                Customize your experience and notifications
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-neutral-900">Email Notifications</h4>
                    <p className="text-sm text-neutral-600">Receive appointment reminders</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" disabled />
                    <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                  </label>
                </div>
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-medium text-neutral-900">SMS Notifications</h4>
                    <p className="text-sm text-neutral-600">Receive text message alerts</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" className="sr-only peer" disabled />
                    <div className="w-11 h-6 bg-neutral-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-neutral-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                  </label>
                </div>
                <button className="w-full bg-neutral-300 text-neutral-500 px-4 py-2 rounded-md text-sm cursor-not-allowed">
                  Save Preferences (Coming Soon)
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
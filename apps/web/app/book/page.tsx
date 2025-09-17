import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function BookPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Book a Session
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Schedule your counseling session with our qualified professionals.
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Coming Soon</CardTitle>
              <CardDescription>
                Our booking system is currently under development.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div className="bg-sky-50 border border-sky-200 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-sky-800 mb-2">
                    What to expect:
                  </h3>
                  <ul className="space-y-2 text-sky-700">
                    <li>• Easy online scheduling with calendar integration</li>
                    <li>• Secure video session links</li>
                    <li>• Automated reminders and confirmations</li>
                    <li>• Flexible rescheduling options</li>
                  </ul>
                </div>

                <div className="text-center">
                  <p className="text-neutral-600 mb-4">
                    For now, please contact us directly to schedule your appointment.
                  </p>
                  <div className="space-x-4">
                    <a
                      href="tel:+1-555-0123"
                      className="bg-primary-600 text-white px-6 py-3 rounded-md text-lg font-medium hover:bg-primary-700 transition-colors"
                    >
                      Call (555) 012-3456
                    </a>
                    <a
                      href="mailto:appointments@groundedcounselling.com"
                      className="border border-primary-600 text-primary-600 px-6 py-3 rounded-md text-lg font-medium hover:bg-primary-50 transition-colors"
                    >
                      Email Us
                    </a>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function ServicesPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Our Services
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Comprehensive mental health services designed to support your wellness journey.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Individual Therapy</CardTitle>
              <CardDescription>
                One-on-one sessions tailored to your specific needs and goals.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                Work through personal challenges with personalized therapeutic approaches
                including CBT, DBT, and mindfulness-based interventions.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Couples Therapy</CardTitle>
              <CardDescription>
                Strengthen relationships through guided communication and understanding.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                Address relationship challenges and build stronger connections with
                evidence-based couples therapy techniques.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Family Therapy</CardTitle>
              <CardDescription>
                Improve family dynamics and resolve conflicts together.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                Create healthier family relationships through systemic therapy
                approaches and family-centered interventions.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Group Therapy</CardTitle>
              <CardDescription>
                Connect with others facing similar challenges in a supportive environment.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                Participate in therapeutic groups focused on specific topics like
                anxiety, depression, grief, and addiction recovery.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Crisis Support</CardTitle>
              <CardDescription>
                Immediate support when you need it most.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                24/7 crisis intervention and support services for urgent mental
                health needs and emergency situations.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Specialized Programs</CardTitle>
              <CardDescription>
                Targeted treatment for specific conditions and populations.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-neutral-600">
                Specialized programs for trauma, PTSD, eating disorders, addiction,
                and adolescent mental health.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
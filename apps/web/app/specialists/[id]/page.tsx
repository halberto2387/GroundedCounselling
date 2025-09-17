import { notFound } from 'next/navigation';
import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

// Mock data (in real app, this would come from API)
const specialists = {
  '1': {
    id: '1',
    name: 'Dr. Sarah Johnson',
    title: 'Licensed Clinical Psychologist',
    specializations: ['Anxiety', 'Depression', 'Trauma'],
    bio: 'Dr. Johnson has over 10 years of experience in cognitive behavioral therapy and trauma-informed care. She specializes in helping individuals overcome anxiety and depression through evidence-based therapeutic approaches.',
    education: ['Ph.D. in Clinical Psychology - University of California', 'M.A. in Psychology - Stanford University'],
    certifications: ['Licensed Clinical Psychologist (CA)', 'Trauma-Informed Care Certified'],
    rate: 120,
    availability: ['Monday 9:00 AM - 5:00 PM', 'Wednesday 10:00 AM - 6:00 PM', 'Friday 9:00 AM - 3:00 PM'],
  },
  '2': {
    id: '2',
    name: 'Dr. Michael Chen',
    title: 'Licensed Marriage and Family Therapist',
    specializations: ['Couples Therapy', 'Family Therapy', 'Communication'],
    bio: 'Specializing in relationship counseling with a focus on systemic approaches and mindfulness. Dr. Chen helps couples and families build stronger connections and resolve conflicts.',
    education: ['Ph.D. in Marriage and Family Therapy - Alliant University', 'M.S. in Counseling Psychology - USC'],
    certifications: ['Licensed Marriage and Family Therapist (CA)', 'Gottman Method Couples Therapy'],
    rate: 110,
    availability: ['Tuesday 10:00 AM - 7:00 PM', 'Thursday 10:00 AM - 7:00 PM', 'Saturday 9:00 AM - 2:00 PM'],
  },
  '3': {
    id: '3',
    name: 'Dr. Emily Rodriguez',
    title: 'Licensed Professional Counselor',
    specializations: ['Adolescents', 'ADHD', 'Life Transitions'],
    bio: 'Passionate about helping young people navigate life challenges with strength-based approaches. Dr. Rodriguez specializes in adolescent therapy and supports individuals through major life transitions.',
    education: ['Ph.D. in Counseling Psychology - UCLA', 'M.A. in Clinical Psychology - Pepperdine University'],
    certifications: ['Licensed Professional Counselor (CA)', 'Child and Adolescent Therapy Specialist'],
    rate: 100,
    availability: ['Monday 2:00 PM - 8:00 PM', 'Wednesday 1:00 PM - 7:00 PM', 'Thursday 2:00 PM - 8:00 PM'],
  },
};

interface SpecialistPageProps {
  params: {
    id: string;
  };
}

export default function SpecialistPage({ params }: SpecialistPageProps) {
  const specialist = specialists[params.id as keyof typeof specialists];

  if (!specialist) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="mb-8">
            <Link 
              href="/specialists" 
              className="text-primary-600 hover:text-primary-700 mb-4 inline-block"
            >
              ← Back to Specialists
            </Link>
            
            <div className="bg-white rounded-lg shadow-sm p-8">
              <div className="text-center mb-8">
                <h1 className="text-4xl font-bold text-neutral-900 mb-2 font-serif">
                  {specialist.name}
                </h1>
                <p className="text-xl text-neutral-600">{specialist.title}</p>
                <div className="flex justify-center flex-wrap gap-2 mt-4">
                  {specialist.specializations.map((spec) => (
                    <span
                      key={spec}
                      className="bg-primary-100 text-primary-700 px-3 py-1 rounded-full text-sm"
                    >
                      {spec}
                    </span>
                  ))}
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>About</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-neutral-600">{specialist.bio}</p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Education</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {specialist.education.map((edu, index) => (
                          <li key={index} className="text-neutral-600 text-sm">
                            • {edu}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Certifications</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {specialist.certifications.map((cert, index) => (
                          <li key={index} className="text-neutral-600 text-sm">
                            • {cert}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>
                </div>

                <div className="space-y-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>Availability</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <ul className="space-y-2">
                        {specialist.availability.map((slot, index) => (
                          <li key={index} className="text-neutral-600 text-sm">
                            • {slot}
                          </li>
                        ))}
                      </ul>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Session Rate</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-3xl font-bold text-primary-600">
                        ${specialist.rate}
                      </p>
                      <p className="text-sm text-neutral-600">per 50-minute session</p>
                    </CardContent>
                  </Card>

                  <div className="space-y-4">
                    <Link
                      href="/book"
                      className="w-full bg-primary-600 text-white px-6 py-3 rounded-md text-lg font-medium hover:bg-primary-700 transition-colors text-center block"
                    >
                      Book Session
                    </Link>
                    <Link
                      href="/contact"
                      className="w-full border border-primary-600 text-primary-600 px-6 py-3 rounded-md text-lg font-medium hover:bg-primary-50 transition-colors text-center block"
                    >
                      Contact
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
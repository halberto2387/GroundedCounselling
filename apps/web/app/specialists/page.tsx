import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

// Mock data for specialists
const specialists = [
  {
    id: '1',
    name: 'Dr. Sarah Johnson',
    title: 'Licensed Clinical Psychologist',
    specializations: ['Anxiety', 'Depression', 'Trauma'],
    bio: 'Dr. Johnson has over 10 years of experience in cognitive behavioral therapy and trauma-informed care.',
    rate: 120,
  },
  {
    id: '2',
    name: 'Dr. Michael Chen',
    title: 'Licensed Marriage and Family Therapist',
    specializations: ['Couples Therapy', 'Family Therapy', 'Communication'],
    bio: 'Specializing in relationship counseling with a focus on systemic approaches and mindfulness.',
    rate: 110,
  },
  {
    id: '3',
    name: 'Dr. Emily Rodriguez',
    title: 'Licensed Professional Counselor',
    specializations: ['Adolescents', 'ADHD', 'Life Transitions'],
    bio: 'Passionate about helping young people navigate life challenges with strength-based approaches.',
    rate: 100,
  },
];

export default function SpecialistsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Our Specialists
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Connect with experienced mental health professionals who are committed to your wellbeing.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {specialists.map((specialist) => (
            <Card key={specialist.id}>
              <CardHeader>
                <CardTitle>{specialist.name}</CardTitle>
                <CardDescription>{specialist.title}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <p className="text-sm text-neutral-600">{specialist.bio}</p>
                  
                  <div>
                    <h4 className="font-medium text-sm mb-2">Specializations:</h4>
                    <div className="flex flex-wrap gap-2">
                      {specialist.specializations.map((spec) => (
                        <span
                          key={spec}
                          className="bg-primary-100 text-primary-700 px-2 py-1 rounded-full text-xs"
                        >
                          {spec}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-between items-center pt-4">
                    <span className="text-lg font-bold text-primary-600">
                      ${specialist.rate}/session
                    </span>
                    <Link
                      href={`/specialists/${specialist.id}`}
                      className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700 transition-colors"
                    >
                      View Profile
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
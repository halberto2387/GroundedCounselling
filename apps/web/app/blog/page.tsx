import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function BlogPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Mental Health Resources
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Educational content, insights, and resources for your mental health journey.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Understanding Anxiety</CardTitle>
              <CardDescription>Posted on Dec 15, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Learn about the different types of anxiety disorders and effective coping strategies
                that can help you manage anxiety in your daily life.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Building Resilience</CardTitle>
              <CardDescription>Posted on Dec 10, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Discover practical techniques for building emotional resilience and developing
                healthy coping mechanisms during challenging times.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Communication Skills</CardTitle>
              <CardDescription>Posted on Dec 5, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Improve your relationships with effective communication strategies that promote
                understanding and connection with others.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Mindfulness Techniques</CardTitle>
              <CardDescription>Posted on Nov 28, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Explore mindfulness practices that can help reduce stress, improve focus,
                and enhance your overall well-being.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Supporting Loved Ones</CardTitle>
              <CardDescription>Posted on Nov 20, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Learn how to provide meaningful support to friends and family members
                who may be struggling with mental health challenges.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Self-Care Strategies</CardTitle>
              <CardDescription>Posted on Nov 15, 2023</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-neutral-600 text-sm mb-4">
                Discover the importance of self-care and practical ways to prioritize
                your mental and emotional health in busy daily life.
              </p>
              <a href="#" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
                Read more →
              </a>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
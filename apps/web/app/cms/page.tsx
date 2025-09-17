import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@grounded-counselling/ui';

export default function CMSPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-50 to-surface-200">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold text-neutral-900 mb-6 font-serif">
            Content Management
          </h1>
          <p className="text-xl text-neutral-600 max-w-3xl mx-auto">
            Manage website content, blog posts, and resources.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Blog Posts</CardTitle>
              <CardDescription>
                Create and manage educational blog content
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="bg-primary-50 border border-primary-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-primary-800">Understanding Anxiety</h4>
                    <span className="text-xs text-primary-600 bg-primary-100 px-2 py-1 rounded">Published</span>
                  </div>
                  <p className="text-sm text-primary-700">
                    Posted 5 days ago • 1,234 views
                  </p>
                </div>
                <div className="bg-neutral-50 border border-neutral-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-neutral-800">Building Resilience</h4>
                    <span className="text-xs text-neutral-600 bg-neutral-100 px-2 py-1 rounded">Draft</span>
                  </div>
                  <p className="text-sm text-neutral-700">
                    Last edited 2 days ago
                  </p>
                </div>
                <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                  Create New Post
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Resources</CardTitle>
              <CardDescription>
                Manage mental health resources and materials
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">Anxiety Worksheets</span>
                    <span className="text-xs text-neutral-500">PDF</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">Mindfulness Guide</span>
                    <span className="text-xs text-neutral-500">PDF</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">Crisis Resources</span>
                    <span className="text-xs text-neutral-500">PDF</span>
                  </div>
                </div>
                <button className="w-full border border-primary-600 text-primary-600 px-4 py-2 rounded-md text-sm hover:bg-primary-50">
                  Upload Resource
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Page Content</CardTitle>
              <CardDescription>
                Edit website pages and static content
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">Home Page</span>
                    <span className="text-xs text-primary-600">Live</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">Services</span>
                    <span className="text-xs text-primary-600">Live</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-neutral-700">About Us</span>
                    <span className="text-xs text-neutral-500">Draft</span>
                  </div>
                </div>
                <button className="w-full border border-primary-600 text-primary-600 px-4 py-2 rounded-md text-sm hover:bg-primary-50">
                  Edit Pages
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Media Library</CardTitle>
              <CardDescription>
                Manage images, videos, and other media files
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-2">
                  <div className="aspect-square bg-neutral-200 rounded-lg flex items-center justify-center">
                    <span className="text-xs text-neutral-500">IMG</span>
                  </div>
                  <div className="aspect-square bg-neutral-200 rounded-lg flex items-center justify-center">
                    <span className="text-xs text-neutral-500">IMG</span>
                  </div>
                  <div className="aspect-square bg-neutral-200 rounded-lg flex items-center justify-center">
                    <span className="text-xs text-neutral-500">VID</span>
                  </div>
                </div>
                <p className="text-xs text-neutral-500 text-center">
                  12 files • 2.4 MB used
                </p>
                <button className="w-full border border-primary-600 text-primary-600 px-4 py-2 rounded-md text-sm hover:bg-primary-50">
                  Upload Media
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Analytics</CardTitle>
              <CardDescription>
                Track content performance and engagement
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-sm">
                      <span className="text-neutral-700">Page Views</span>
                      <span className="font-medium">8,432</span>
                    </div>
                    <div className="w-full bg-neutral-200 rounded-full h-2 mt-1">
                      <div className="bg-primary-600 h-2 rounded-full" style={{ width: '75%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm">
                      <span className="text-neutral-700">Blog Reads</span>
                      <span className="font-medium">2,156</span>
                    </div>
                    <div className="w-full bg-neutral-200 rounded-full h-2 mt-1">
                      <div className="bg-sky-400 h-2 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm">
                      <span className="text-neutral-700">Downloads</span>
                      <span className="font-medium">543</span>
                    </div>
                    <div className="w-full bg-neutral-200 rounded-full h-2 mt-1">
                      <div className="bg-primary-400 h-2 rounded-full" style={{ width: '25%' }}></div>
                    </div>
                  </div>
                </div>
                <button className="w-full border border-primary-600 text-primary-600 px-4 py-2 rounded-md text-sm hover:bg-primary-50">
                  View Full Report
                </button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
              <CardDescription>
                Common content management tasks
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <button className="w-full bg-primary-600 text-white px-4 py-2 rounded-md text-sm hover:bg-primary-700">
                  Create New Post
                </button>
                <button className="w-full border border-primary-600 text-primary-600 px-4 py-2 rounded-md text-sm hover:bg-primary-50">
                  Schedule Publication
                </button>
                <button className="w-full border border-neutral-300 text-neutral-700 px-4 py-2 rounded-md text-sm hover:bg-neutral-50">
                  Export Content
                </button>
                <button className="w-full border border-neutral-300 text-neutral-700 px-4 py-2 rounded-md text-sm hover:bg-neutral-50">
                  Backup Data
                </button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
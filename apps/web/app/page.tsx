export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            GroundedCounselling
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            A secure, HIPAA-compliant platform for counselling practice management
          </p>
          <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Development Environment
            </h2>
            <p className="text-gray-600 mb-4">
              This is a placeholder frontend for Docker testing.
            </p>
            <div className="space-y-2 text-sm text-gray-500">
              <p>✅ Next.js 14 with App Router</p>
              <p>✅ TypeScript</p>
              <p>✅ Tailwind CSS</p>
              <p>✅ Docker containerized</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
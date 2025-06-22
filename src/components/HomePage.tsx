import React from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MapPin, Heart, Users, Clock } from "lucide-react";

interface HomePageProps {
  onGetStarted: () => void;
}

const HomePage = ({ onGetStarted }: HomePageProps) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Header */}
      <header className="px-4 py-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <MapPin className="h-8 w-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">
              San Francisco Local Help
            </h1>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="px-4 py-12">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Find Help
            <span className="text-blue-600"> Near You</span>
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Ask simple questions to discover food banks, shelters, clinics, and
            essential services in your area. Get real-time information when you
            need it most.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Button
              onClick={onGetStarted}
              size="lg"
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 text-lg"
            >
              Get Started
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8">
          <Card className="text-center">
            <CardHeader>
              <Heart className="h-12 w-12 text-red-500 mx-auto mb-4" />
              <CardTitle>Personalized AI Assistance</CardTitle>
              <CardDescription>
                Here to assist you in a best way possible
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <MapPin className="h-12 w-12 text-green-500 mx-auto mb-4" />
              <CardTitle>Exact Location Match</CardTitle>
              <CardDescription>
                Automatically finds services near you with real-time
                availability and directions.
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="text-center">
            <CardHeader>
              <Clock className="h-12 w-12 text-blue-500 mx-auto mb-4" />
              <CardTitle>Most Updated Datase</CardTitle>
              <CardDescription>
                Results are tailored using the most recent datasets
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default HomePage;

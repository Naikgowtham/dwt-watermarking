import React from 'react';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { ShieldCheck, Upload, Fingerprint } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-blue-50 to-white">
      <header className="container mx-auto text-center py-16">
        <h1 className="text-5xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          Protect your digital creations with blockchain-verified watermarks
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600">
          Secure your images, art, and music with invisible watermarks that are verified on the blockchain.
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Button size="lg">Upload & Protect</Button>
          <Button size="lg" variant="outline">
            Verify Artwork
          </Button>
        </div>
      </header>

      <main className="container mx-auto px-6 pb-24">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-6 w-6 text-blue-600" />
                Upload Artwork
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Easily upload your digital creations to our platform and prepare them for watermarking.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <ShieldCheck className="h-6 w-6 text-blue-600" />
                Embed Watermark
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Embed a unique, invisible watermark with your copyright information into your artwork.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Fingerprint className="h-6 w-6 text-blue-600" />
                Verify Ownership
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600">
                Verify the ownership of any artwork by uploading it and checking its blockchain-verified watermark.
              </p>
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;

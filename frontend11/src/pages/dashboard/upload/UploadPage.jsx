import React from 'react';
import { Button } from '../../../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card';
import { Input } from '../../../components/ui/input';
import { Label } from '../../../components/ui/label';

const UploadPage = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder for API call to the backend
    alert('This is a placeholder. The form would be submitted to the backend here.');
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Upload & Protect Artwork</h1>
      <Card>
        <CardHeader>
          <CardTitle>Upload a new creation</CardTitle>
          <CardDescription>
            Upload your image and enter a watermark message to protect your artwork.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="grid gap-6">
            <div className="grid gap-2">
              <Label htmlFor="artwork">Artwork File</Label>
              <Input id="artwork" type="file" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="message">Watermark Message</Label>
              <Input id="message" placeholder="e.g., © Your Name 2024" required />
            </div>
            <Button type="submit">Upload & Protect</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default UploadPage;

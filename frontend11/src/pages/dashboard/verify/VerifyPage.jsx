import React, { useState } from 'react';
import { Button } from '../../../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../../components/ui/card';
import { Input } from '../../../components/ui/input';
import { Label } from '../../../components/ui/label';

const VerifyPage = () => {
  const [verificationResult, setVerificationResult] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder for API call to the backend
    setVerificationResult({
      creator: 'John Doe',
      copyright: '© John Doe 2024',
      hash: '0x1234567890abcdef1234567890abcdef12345678',
    });
  };

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Verify Artwork</h1>
      <Card>
        <CardHeader>
          <CardTitle>Verify an artwork</CardTitle>
          <CardDescription>
            Upload an image to extract and verify its watermark.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="grid gap-6">
            <div className="grid gap-2">
              <Label htmlFor="artwork">Artwork File</Label>
              <Input id="artwork" type="file" required />
            </div>
            <Button type="submit">Verify Artwork</Button>
          </form>
        </CardContent>
      </Card>

      {verificationResult && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Verification Result</CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2">
            <p><strong>Creator:</strong> {verificationResult.creator}</p>
            <p><strong>Copyright:</strong> {verificationResult.copyright}</p>
            <p><strong>Blockchain Hash:</strong> {verificationResult.hash}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default VerifyPage;

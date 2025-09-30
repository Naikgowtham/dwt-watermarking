import React from 'react';
import { Card, CardContent, CardFooter, CardHeader } from '../../../components/ui/card';

const creations = [
  {
    id: 1,
    thumbnail: 'https://via.placeholder.com/150',
    message: '© John Doe 2024',
    hash: '0x1234567890abcdef1234567890abcdef12345678',
  },
  {
    id: 2,
    thumbnail: 'https://via.placeholder.com/150',
    message: '© John Doe 2024',
    hash: '0xabcdef1234567890abcdef1234567890abcdef12',
  },
  {
    id: 3,
    thumbnail: 'https://via.placeholder.com/150',
    message: '© John Doe 2024',
    hash: '0x1234567890abcdef1234567890abcdef12345678',
  },
];

const MyCreationsPage = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">My Creations</h1>
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {creations.map((creation) => (
          <Card key={creation.id}>
            <CardHeader>
              <img src={creation.thumbnail} alt="Artwork" className="rounded-lg" />
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">{creation.message}</p>
            </CardContent>
            <CardFooter>
              <p className="text-xs text-gray-400 truncate">Hash: {creation.hash}</p>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default MyCreationsPage;

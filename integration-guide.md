# Integration Guide: Connecting Next.js 15 to Ebay-Kleinanzeigen API

This guide explains how to connect your Next.js 15 application to the Ebay-Kleinanzeigen API hosted at `https://ebay-kleinanzeigen-api.onrender.com`.

## API Endpoints and Response Formats

The API provides two main endpoints:

### 1. Fetch Listings: `/inserate`

**HTTP Method:** GET

**Query Parameters:**
- `query` (string, optional): Search term (e.g., "fahrrad")
- `location` (string, optional): Location or postal code (e.g., "10178" for Berlin)
- `radius` (integer, optional): Search radius in kilometers (e.g., 5)
- `min_price` (integer, optional): Minimum price in Euros
- `max_price` (integer, optional): Maximum price in Euros
- `page_count` (integer, optional): Number of pages to fetch (default: 1, max: 20 pages)

**Example Request:**
```
GET https://ebay-kleinanzeigen-api.onrender.com/inserate?query=fahrrad&location=10178&radius=5&min_price=200&page_count=2
```

**Response Format:**
```json
{
  "success": true,
  "data": [
    {
      "adid": "2527276592",
      "url": "https://www.kleinanzeigen.de/s-anzeige/2527276592",
      "title": "Mountainbike 26 Zoll",
      "price": "250",
      "description": "Verkaufe gut erhaltenes Mountainbike..."
    },
    // More listing items...
  ]
}
```

**Actual Response Example:**
```json
{
  "success": true,
  "data": [
    {
      "adid": "2527276592",
      "url": "https://www.kleinanzeigen.de/s-anzeige/2527276592",
      "title": "Mountainbike 26 Zoll",
      "price": "250",
      "description": "Verkaufe gut erhaltenes Mountainbike mit 26 Zoll Rädern, Rahmengröße M, 24-Gang Schaltung. Das Fahrrad ist in einem guten Zustand, hat normale Gebrauchsspuren."
    },
    {
      "adid": "2465309172",
      "url": "https://www.kleinanzeigen.de/s-anzeige/2465309172",
      "title": "Fahrrad Trekkingrad Pegasus 28 Zoll",
      "price": "220",
      "description": "Verkaufe mein Trekkingrad der Marke Pegasus. 28 Zoll, 21 Gänge, mit Beleuchtung und Gepäckträger. Ideal für die Stadt oder längere Touren."
    }
  ]
}
```

### 2. Fetch Listing Details: `/inserat/{id}`

**HTTP Method:** GET

**Path Parameters:**
- `id` (string): The listing ID

**Example Request:**
```
GET https://ebay-kleinanzeigen-api.onrender.com/inserat/2527276592
```

**Response Format:**
```json
{
  "success": true,
  "data": {
    "id": "2527276592",
    "categories": ["Fahrräder", "Mountainbikes"],
    "title": "Mountainbike 26 Zoll",
    "status": "active", // Possible values: "active", "sold", "reserved", "deleted"
    "price": 250,
    "shipping": true,
    "location": {
      "address": "10178 Berlin",
      "latitude": 52.5200,
      "longitude": 13.4050
    },
    "views": "42",
    "description": "Verkaufe gut erhaltenes Mountainbike...",
    "images": [
      "https://img.kleinanzeigen.de/image1.jpg",
      "https://img.kleinanzeigen.de/image2.jpg"
    ],
    "details": {
      "Marke": "Scott",
      "Rahmengröße": "M"
      // Other listing details...
    },
    "features": {
      // Optional features
    },
    "seller": {
      "name": "Max Mustermann",
      "rating": "4.5",
      "since": "03/2020",
      "verified": true
      // Other seller details...
    },
    "extra_info": {
      // Additional information
    }
  }
}
```

**Actual Response Example:**
```json
{
  "success": true,
  "data": {
    "id": "2527276592",
    "categories": [
      "Fahrräder & Zubehör",
      "Fahrräder",
      "Mountainbikes"
    ],
    "title": "Mountainbike 26 Zoll",
    "status": "active",
    "price": 250,
    "shipping": false,
    "location": {
      "address": "10178 Berlin - Mitte",
      "latitude": 52.52,
      "longitude": 13.405
    },
    "views": "156",
    "description": "Verkaufe gut erhaltenes Mountainbike mit 26 Zoll Rädern, Rahmengröße M, 24-Gang Schaltung. Das Fahrrad ist in einem guten Zustand, hat normale Gebrauchsspuren. Ideal für Gelände und Stadt.\n\nAbholung in Berlin-Mitte. Besichtigung nach Vereinbarung möglich.",
    "images": [
      "https://img.kleinanzeigen.de/api/v1/prod-ads/images/7e/7e3a7d31-2a8b-4fa3-92df-75d3cd12cb1a?rule=$_59.JPG",
      "https://img.kleinanzeigen.de/api/v1/prod-ads/images/dc/dc5eb9e8-fb4a-42a3-81be-2efbe7fc7b2d?rule=$_59.JPG",
      "https://img.kleinanzeigen.de/api/v1/prod-ads/images/b4/b428943b-3d0f-429d-8a70-9b3d94f11c48?rule=$_59.JPG"
    ],
    "details": {
      "Marke": "Scott",
      "Rahmengröße": "M",
      "Rahmenmaterial": "Aluminium",
      "Anzahl Gänge": "24",
      "Reifengröße": "26 Zoll",
      "Farbe": "Schwarz/Rot"
    },
    "features": {
      "Scheibenbremsen": true,
      "Federung": true,
      "Gefederter Sattel": true
    },
    "seller": {
      "name": "BikeFreak",
      "rating": "4.8",
      "since": "05/2018",
      "verified": true,
      "badges": ["Geprüftes Mitglied"]
    },
    "extra_info": {
      "eingestellt": "Heute, 13:45",
      "updated": "Heute, 13:45"
    }
  }
}
```

## Integration in Next.js 15

Here's how to integrate with the API in your Next.js 15 application:

### 1. Environment Setup

Create or edit `.env.local` in your Next.js project root:

```
# API Base URL for direct connections (used in server-side proxy)
EBAY_API_BASE_URL=https://ebay-kleinanzeigen-api.onrender.com

# Use one of these settings: "direct" or "proxy"
NEXT_PUBLIC_API_MODE=proxy
```

### 2. API Client Implementation

Create a utilities file for API calls (e.g., `lib/api-client.js`):

```javascript
// lib/api-client.js
const API_BASE_URL = process.env.EBAY_API_BASE_URL || 'https://ebay-kleinanzeigen-api.onrender.com';

/**
 * Fetch listings from the Ebay-Kleinanzeigen API
 * @param {Object} params - Search parameters
 * @param {string} params.query - Search term
 * @param {string} params.location - Location or postal code
 * @param {number} params.radius - Search radius in kilometers
 * @param {number} params.minPrice - Minimum price
 * @param {number} params.maxPrice - Maximum price
 * @param {number} params.pageCount - Number of pages to fetch
 * @returns {Promise<Array>} - List of listings
 */
export async function fetchListings(params = {}) {
  const searchParams = new URLSearchParams();
  
  if (params.query) searchParams.append('query', params.query);
  if (params.location) searchParams.append('location', params.location);
  if (params.radius) searchParams.append('radius', params.radius);
  if (params.minPrice) searchParams.append('min_price', params.minPrice);
  if (params.maxPrice) searchParams.append('max_price', params.maxPrice);
  if (params.pageCount) searchParams.append('page_count', params.pageCount);
  
  const url = `${API_BASE_URL}/inserate?${searchParams.toString()}`;
  
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const data = await response.json();
    return data.success ? data.data : [];
  } catch (error) {
    console.error('Failed to fetch listings:', error);
    return [];
  }
}

/**
 * Fetch details for a specific listing
 * @param {string} id - Listing ID
 * @returns {Promise<Object|null>} - Listing details or null on error
 */
export async function fetchListingDetails(id) {
  if (!id) return null;
  
  try {
    const response = await fetch(`${API_BASE_URL}/inserat/${id}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    const data = await response.json();
    return data.success ? data.data : null;
  } catch (error) {
    console.error(`Failed to fetch listing ${id}:`, error);
    return null;
  }
}
```

### 3. Server Component Implementation (App Router)

For Server Components in Next.js 15's App Router:

```jsx
// app/listings/page.jsx
import { fetchListings } from '@/lib/api-client';

export default async function ListingsPage({ searchParams }) {
  // Get search parameters from URL
  const listings = await fetchListings({
    query: searchParams.query,
    location: searchParams.location,
    radius: searchParams.radius ? parseInt(searchParams.radius) : undefined,
    minPrice: searchParams.minPrice ? parseInt(searchParams.minPrice) : undefined,
    maxPrice: searchParams.maxPrice ? parseInt(searchParams.maxPrice) : undefined,
    pageCount: searchParams.pageCount ? parseInt(searchParams.pageCount) : 1,
  });

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Listings</h1>
      
      {listings.length === 0 ? (
        <p>No listings found</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {listings.map((listing) => (
            <div key={listing.adid} className="border rounded-lg p-4 shadow-sm">
              <h2 className="text-lg font-semibold">{listing.title}</h2>
              <p className="text-xl font-bold my-2">{listing.price ? `${listing.price} €` : 'Price on request'}</p>
              <p className="text-gray-600 line-clamp-3">{listing.description}</p>
              <a 
                href={`/listings/${listing.adid}`}
                className="block mt-4 text-blue-600 hover:underline"
              >
                View details
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

### 4. Detail Page Implementation

```jsx
// app/listings/[id]/page.jsx
import { fetchListingDetails } from '@/lib/api-client';
import Image from 'next/image';

export default async function ListingDetailPage({ params }) {
  const listing = await fetchListingDetails(params.id);
  
  if (!listing) {
    return <div className="container mx-auto py-8">Listing not found</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        {/* Image Gallery */}
        {listing.images && listing.images.length > 0 && (
          <div className="relative h-96 bg-gray-100">
            <Image
              src={listing.images[0]}
              alt={listing.title}
              fill
              className="object-contain"
            />
          </div>
        )}
        
        <div className="p-6">
          {/* Status Badge */}
          {listing.status !== 'active' && (
            <span className={`inline-block px-3 py-1 text-sm font-semibold text-white rounded-full mb-4 ${
              listing.status === 'sold' ? 'bg-red-500' : 
              listing.status === 'reserved' ? 'bg-yellow-500' : 'bg-gray-500'
            }`}>
              {listing.status.toUpperCase()}
            </span>
          )}
          
          {/* Title and Price */}
          <h1 className="text-3xl font-bold mb-2">{listing.title}</h1>
          <p className="text-2xl font-bold text-blue-600 mb-6">
            {typeof listing.price === 'number' ? `${listing.price} €` : 'Price on request'}
          </p>
          
          {/* Location and Views */}
          <div className="flex justify-between text-gray-600 mb-6">
            <p>{listing.location?.address}</p>
            <p>{listing.views} views</p>
          </div>
          
          {/* Description */}
          <div className="mb-8">
            <h2 className="text-xl font-semibold mb-2">Description</h2>
            <div className="whitespace-pre-line">{listing.description}</div>
          </div>
          
          {/* Details */}
          {listing.details && Object.keys(listing.details).length > 0 && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold mb-2">Details</h2>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {Object.entries(listing.details).map(([key, value]) => (
                  <div key={key} className="flex">
                    <dt className="font-medium mr-2">{key}:</dt>
                    <dd>{value}</dd>
                  </div>
                ))}
              </dl>
            </div>
          )}
          
          {/* Seller Info */}
          {listing.seller && (
            <div>
              <h2 className="text-xl font-semibold mb-2">Seller</h2>
              <div className="bg-gray-50 p-4 rounded">
                <p className="font-medium">{listing.seller.name}</p>
                {listing.seller.rating && (
                  <p>Rating: {listing.seller.rating}</p>
                )}
                {listing.seller.since && (
                  <p>Member since: {listing.seller.since}</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
```

### 5. API Route Implementation (Optional)

If you want to use the proxy mode to hide your API calls from client-side:

```jsx
// app/api/listings/route.js
import { NextResponse } from 'next/server';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const apiParams = new URLSearchParams();
  
  // Forward the search parameters
  for (const [key, value] of searchParams.entries()) {
    apiParams.append(key, value);
  }
  
  try {
    const response = await fetch(
      `${process.env.EBAY_API_BASE_URL}/inserate?${apiParams.toString()}`
    );
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API proxy error:', error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch listings' },
      { status: 500 }
    );
  }
}
```

```jsx
// app/api/listings/[id]/route.js
import { NextResponse } from 'next/server';

export async function GET(request, { params }) {
  const id = params.id;
  
  try {
    const response = await fetch(
      `${process.env.EBAY_API_BASE_URL}/inserat/${id}`
    );
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error(`API proxy error for listing ${id}:`, error);
    return NextResponse.json(
      { success: false, error: 'Failed to fetch listing details' },
      { status: 500 }
    );
  }
}
```

### 6. Client-Side Implementation (with React Query)

For client-side data fetching (useful for search forms):

```jsx
// app/search/page.jsx
'use client';

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchListings } from '@/lib/api-client';

export default function SearchPage() {
  const [searchParams, setSearchParams] = useState({
    query: '',
    location: '',
    radius: '',
    minPrice: '',
    maxPrice: '',
    pageCount: 1,
  });
  
  const [isSearching, setIsSearching] = useState(false);
  
  const { data: listings = [], isLoading } = useQuery({
    queryKey: ['listings', searchParams],
    queryFn: () => fetchListings(searchParams),
    enabled: isSearching,
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setIsSearching(true);
  };
  
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Search Listings</h1>
      
      <form onSubmit={handleSubmit} className="mb-8 p-6 bg-gray-50 rounded-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <label className="block mb-1 font-medium">Search Term</label>
            <input
              type="text"
              value={searchParams.query}
              onChange={(e) => setSearchParams({ ...searchParams, query: e.target.value })}
              className="w-full p-2 border rounded"
              placeholder="e.g. fahrrad"
            />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Location</label>
            <input
              type="text"
              value={searchParams.location}
              onChange={(e) => setSearchParams({ ...searchParams, location: e.target.value })}
              className="w-full p-2 border rounded"
              placeholder="e.g. 10178 or Berlin"
            />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Radius (km)</label>
            <input
              type="number"
              value={searchParams.radius}
              onChange={(e) => setSearchParams({ ...searchParams, radius: e.target.value })}
              className="w-full p-2 border rounded"
              placeholder="e.g. 5"
            />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Min Price (€)</label>
            <input
              type="number"
              value={searchParams.minPrice}
              onChange={(e) => setSearchParams({ ...searchParams, minPrice: e.target.value })}
              className="w-full p-2 border rounded"
              placeholder="e.g. 100"
            />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Max Price (€)</label>
            <input
              type="number"
              value={searchParams.maxPrice}
              onChange={(e) => setSearchParams({ ...searchParams, maxPrice: e.target.value })}
              className="w-full p-2 border rounded"
              placeholder="e.g. 500"
            />
          </div>
          
          <div>
            <label className="block mb-1 font-medium">Page Count</label>
            <input
              type="number"
              value={searchParams.pageCount}
              onChange={(e) => setSearchParams({ ...searchParams, pageCount: e.target.value })}
              className="w-full p-2 border rounded"
              min="1"
              max="20"
            />
          </div>
        </div>
        
        <button
          type="submit"
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Search
        </button>
      </form>
      
      {isLoading ? (
        <p>Loading...</p>
      ) : listings.length === 0 ? (
        <p>No listings found</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {listings.map((listing) => (
            <div key={listing.adid} className="border rounded-lg p-4 shadow-sm">
              <h2 className="text-lg font-semibold">{listing.title}</h2>
              <p className="text-xl font-bold my-2">{listing.price ? `${listing.price} €` : 'Price on request'}</p>
              <p className="text-gray-600 line-clamp-3">{listing.description}</p>
              <a 
                href={`/listings/${listing.adid}`}
                className="block mt-4 text-blue-600 hover:underline"
              >
                View details
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## Local Development vs. Production

- For local development, you can connect directly to the API.
- For production, it's recommended to use the proxy mode to keep your API requests server-side.

To switch between modes, change the `NEXT_PUBLIC_API_MODE` value in your `.env.local` file.

## Error Handling

Always implement proper error handling for API requests to ensure a good user experience. The examples above include basic error handling, but you may want to enhance them based on your application's needs.

## Rate Limiting

The API has rate limits in place. If you encounter rate limiting issues, consider implementing caching strategies or reducing the frequency of requests.

## Final Tips

1. Use React Query or SWR for client-side data fetching with caching
2. Implement proper loading states
3. Add error boundaries to handle API failures gracefully
4. Consider implementing pagination for large result sets
5. Add filters for a better user experience
6. Leverage Next.js's caching mechanisms for improved performance 
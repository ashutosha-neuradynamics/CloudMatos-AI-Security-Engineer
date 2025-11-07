/**
 * Main demo page for Prompt Firewall.
 */

'use client';

import { useState } from 'react';
import PromptInput from '@/components/demo/PromptInput';
import ResponseDisplay from '@/components/demo/ResponseDisplay';
import { QueryResponse } from '@/lib/api-client';

export default function Home() {
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleResult = (queryResult: QueryResponse) => {
    setResult(queryResult);
    setError(null);
  };

  const handleError = (err: Error) => {
    setError(err.message);
    setResult(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Prompt Firewall Demo
        </h1>
        <p className="text-lg text-gray-600">
          Test the security firewall by entering prompts and responses
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Enter Prompt/Response
          </h2>
          <PromptInput onResult={handleResult} onError={handleError} />
        </div>
        
        <div>
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-red-800 font-medium">Error</p>
              <p className="text-red-600 text-sm mt-1">{error}</p>
            </div>
          )}
          <ResponseDisplay result={result} />
        </div>
      </div>
    </div>
  );
}

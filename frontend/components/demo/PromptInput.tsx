/**
 * Prompt input component for submitting prompts to the firewall.
 */

'use client';

import { useState } from 'react';
import { apiClient, QueryRequest, QueryResponse, APIError } from '@/lib/api-client';

interface PromptInputProps {
  onResult: (result: QueryResponse) => void;
  onError: (error: Error) => void;
}

export default function PromptInput({ onResult, onError }: PromptInputProps) {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!prompt && !response) {
      onError(new Error('Please enter at least a prompt or response'));
      return;
    }

    setLoading(true);
    
    try {
      const request: QueryRequest = {};
      if (prompt) request.prompt = prompt;
      if (response) request.response = response;
      
      const result = await apiClient.query(request);
      onResult(result);
    } catch (error) {
      if (error instanceof APIError) {
        onError(new Error(error.message));
      } else if (error instanceof Error) {
        onError(error);
      } else {
        onError(new Error('An unexpected error occurred'));
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-2">
          Prompt
        </label>
        <textarea
          id="prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          rows={6}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter your prompt here..."
          disabled={loading}
        />
      </div>
      
      <div>
        <label htmlFor="response" className="block text-sm font-medium text-gray-700 mb-2">
          Response (Optional)
        </label>
        <textarea
          id="response"
          value={response}
          onChange={(e) => setResponse(e.target.value)}
          rows={6}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter model response here (optional)..."
          disabled={loading}
        />
      </div>
      
      <button
        type="submit"
        disabled={loading || (!prompt && !response)}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? 'Processing...' : 'Submit for Analysis'}
      </button>
    </form>
  );
}


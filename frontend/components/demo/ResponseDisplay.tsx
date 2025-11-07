/**
 * Response display component showing firewall decisions and results.
 */

'use client';

import { QueryResponse, Risk } from '@/lib/api-client';
import RiskIndicator from './RiskIndicator';

interface ResponseDisplayProps {
  result: QueryResponse | null;
}

export default function ResponseDisplay({ result }: ResponseDisplayProps) {
  if (!result) {
    return null;
  }

  const getDecisionColor = (decision: string) => {
    switch (decision) {
      case 'block':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'redact':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'warn':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'allow':
        return 'bg-green-100 text-green-800 border-green-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Firewall Decision</h2>
        
        <div className={`inline-block px-4 py-2 rounded-md border ${getDecisionColor(result.decision)}`}>
          <span className="font-medium capitalize">{result.decision}</span>
        </div>
        
        <p className="mt-4 text-gray-700">{result.explanation}</p>
      </div>

      {result.risks.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Detected Risks ({result.risks.length})
          </h2>
          
          <div className="space-y-3">
            {result.risks.map((risk: Risk, index: number) => (
              <RiskIndicator key={index} risk={risk} />
            ))}
          </div>
        </div>
      )}

      {result.promptModified && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Modified Prompt</h2>
          <div className="bg-gray-50 rounded-md p-4">
            <pre className="whitespace-pre-wrap text-sm text-gray-700">
              {result.promptModified}
            </pre>
          </div>
        </div>
      )}

      {result.responseModified && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Modified Response</h2>
          <div className="bg-gray-50 rounded-md p-4">
            <pre className="whitespace-pre-wrap text-sm text-gray-700">
              {result.responseModified}
            </pre>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Request Metadata</h2>
        <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Request ID</dt>
            <dd className="mt-1 text-sm text-gray-900 font-mono">
              {result.metadata.requestId}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Timestamp</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {new Date(result.metadata.timestamp).toLocaleString()}
            </dd>
          </div>
        </dl>
      </div>
    </div>
  );
}


/**
 * Risk indicator component for displaying risk severity.
 */

'use client';

import { Risk } from '@/lib/api-client';

interface RiskIndicatorProps {
  risk: Risk;
}

export default function RiskIndicator({ risk }: RiskIndicatorProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return {
          bg: 'bg-red-100',
          text: 'text-red-800',
          border: 'border-red-300',
          dot: 'bg-red-500',
        };
      case 'medium':
        return {
          bg: 'bg-yellow-100',
          text: 'text-yellow-800',
          border: 'border-yellow-300',
          dot: 'bg-yellow-500',
        };
      case 'low':
        return {
          bg: 'bg-blue-100',
          text: 'text-blue-800',
          border: 'border-blue-300',
          dot: 'bg-blue-500',
        };
      default:
        return {
          bg: 'bg-gray-100',
          text: 'text-gray-800',
          border: 'border-gray-300',
          dot: 'bg-gray-500',
        };
    }
  };

  const colors = getSeverityColor(risk.severity);

  return (
    <div
      className={`${colors.bg} ${colors.border} ${colors.text} border rounded-lg p-3 flex items-start space-x-3`}
      role="alert"
      aria-label={`${risk.severity} severity risk: ${risk.type}`}
    >
      <div
        className={`${colors.dot} w-3 h-3 rounded-full mt-1 flex-shrink-0`}
        aria-hidden="true"
      />
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <p className="font-medium text-sm">{risk.type}</p>
          <span className="text-xs capitalize opacity-75">{risk.severity}</span>
        </div>
        <p className="text-xs mt-1 opacity-90">{risk.explanation}</p>
        {risk.match && (
          <code className="block mt-2 text-xs bg-white bg-opacity-50 px-2 py-1 rounded">
            {risk.match}
          </code>
        )}
      </div>
    </div>
  );
}


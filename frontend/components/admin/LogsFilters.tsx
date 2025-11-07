/**
 * Logs filters component.
 */

'use client';

import { useState } from 'react';

interface LogsFiltersProps {
  onFilterChange: (filters: {
    type?: string;
    severity?: string;
    date_from?: string;
    date_to?: string;
  }) => void;
}

export default function LogsFilters({ onFilterChange }: LogsFiltersProps) {
  const [type, setType] = useState('');
  const [severity, setSeverity] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  const handleApply = () => {
    onFilterChange({
      type: type || undefined,
      severity: severity || undefined,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
    });
  };

  const handleClear = () => {
    setType('');
    setSeverity('');
    setDateFrom('');
    setDateTo('');
    onFilterChange({});
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Filters</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div>
          <label htmlFor="type" className="block text-sm font-medium text-gray-700 mb-2">
            Risk Type
          </label>
          <select
            id="type"
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="PII">PII</option>
            <option value="PHI">PHI</option>
            <option value="PROMPT_INJECTION">Prompt Injection</option>
          </select>
        </div>

        <div>
          <label htmlFor="severity" className="block text-sm font-medium text-gray-700 mb-2">
            Severity
          </label>
          <select
            id="severity"
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>
        </div>

        <div>
          <label htmlFor="date_from" className="block text-sm font-medium text-gray-700 mb-2">
            From Date
          </label>
          <input
            id="date_from"
            type="date"
            value={dateFrom}
            onChange={(e) => setDateFrom(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label htmlFor="date_to" className="block text-sm font-medium text-gray-700 mb-2">
            To Date
          </label>
          <input
            id="date_to"
            type="date"
            value={dateTo}
            onChange={(e) => setDateTo(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="flex space-x-2 mt-4">
        <button
          onClick={handleApply}
          className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
        >
          Apply Filters
        </button>
        <button
          onClick={handleClear}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 text-sm"
        >
          Clear
        </button>
      </div>
    </div>
  );
}


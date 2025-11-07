/**
 * Policy editor component for managing policy rules.
 */

'use client';

import { useState, useEffect } from 'react';
import { apiClient, PolicyRule, PolicyResponse, APIError } from '@/lib/api-client';

export default function PolicyEditor() {
  const [rules, setRules] = useState<PolicyRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    fetchPolicy();
  }, []);

  const fetchPolicy = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getPolicy();
      setRules(response.rules);
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError('Failed to fetch policy rules');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    setSuccess(false);
    
    try {
      await apiClient.updatePolicy(rules);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (err) {
      if (err instanceof APIError) {
        setError(err.message);
      } else {
        setError('Failed to update policy rules');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleAddRule = () => {
    setRules([
      ...rules,
      {
        name: '',
        description: '',
        risk_type: 'PII',
        pattern: '',
        pattern_type: 'regex',
        severity: 'high',
        action: 'block',
        enabled: true,
      },
    ]);
  };

  const handleRemoveRule = (index: number) => {
    setRules(rules.filter((_, i) => i !== index));
  };

  const handleRuleChange = (index: number, field: keyof PolicyRule, value: any) => {
    const updated = [...rules];
    updated[index] = { ...updated[index], [field]: value };
    setRules(updated);
  };

  if (loading) {
    return <div className="text-center py-8">Loading policy rules...</div>;
  }

  return (
    <div className="space-y-4">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">Error: {error}</p>
        </div>
      )}

      {success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-green-800">Policy rules updated successfully!</p>
        </div>
      )}

      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold text-gray-900">Policy Rules</h2>
        <div className="flex space-x-2">
          <button
            onClick={handleAddRule}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
          >
            Add Rule
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 text-sm"
          >
            {saving ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {rules.map((rule, index) => (
          <div key={index} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-medium text-gray-900">Rule {index + 1}</h3>
              <button
                onClick={() => handleRemoveRule(index)}
                className="text-red-600 hover:text-red-800 text-sm"
              >
                Remove
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Name
                </label>
                <input
                  type="text"
                  value={rule.name}
                  onChange={(e) => handleRuleChange(index, 'name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Risk Type
                </label>
                <select
                  value={rule.risk_type}
                  onChange={(e) => handleRuleChange(index, 'risk_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="PII">PII</option>
                  <option value="PHI">PHI</option>
                  <option value="PROMPT_INJECTION">Prompt Injection</option>
                  <option value="OTHER">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pattern
                </label>
                <input
                  type="text"
                  value={rule.pattern}
                  onChange={(e) => handleRuleChange(index, 'pattern', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Regex pattern or keyword"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pattern Type
                </label>
                <select
                  value={rule.pattern_type}
                  onChange={(e) => handleRuleChange(index, 'pattern_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="regex">Regex</option>
                  <option value="keyword">Keyword</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Severity
                </label>
                <select
                  value={rule.severity}
                  onChange={(e) => handleRuleChange(index, 'severity', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="high">High</option>
                  <option value="medium">Medium</option>
                  <option value="low">Low</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Action
                </label>
                <select
                  value={rule.action}
                  onChange={(e) => handleRuleChange(index, 'action', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="block">Block</option>
                  <option value="redact">Redact</option>
                  <option value="warn">Warn</option>
                  <option value="allow">Allow</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={rule.description || ''}
                  onChange={(e) => handleRuleChange(index, 'description', e.target.value)}
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="flex items-center">
                  <input
                    type="checkbox"
                    checked={rule.enabled}
                    onChange={(e) => handleRuleChange(index, 'enabled', e.target.checked)}
                    className="mr-2"
                  />
                  <span className="text-sm text-gray-700">Enabled</span>
                </label>
              </div>
            </div>
          </div>
        ))}
      </div>

      {rules.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No policy rules. Click "Add Rule" to create one.
        </div>
      )}
    </div>
  );
}


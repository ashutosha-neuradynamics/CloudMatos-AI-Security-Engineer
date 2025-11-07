/**
 * Admin console page.
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import LogsFilters from '@/components/admin/LogsFilters';
import LogsTable from '@/components/admin/LogsTable';
import PolicyEditor from '@/components/admin/PolicyEditor';

type Tab = 'logs' | 'policy';

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<Tab>('logs');
  const [filters, setFilters] = useState<{
    type?: string;
    severity?: string;
    date_from?: string;
    date_to?: string;
  }>({});
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem('admin_token');
    if (!token) {
      router.push('/admin/login');
    }
  }, [router]);

  const handleLogout = () => {
    sessionStorage.removeItem('admin_token');
    router.push('/admin/login');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Admin Console
          </h1>
          <p className="text-lg text-gray-600">
            Manage policies and review logs
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 text-sm"
        >
          Logout
        </button>
      </div>

      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('logs')}
            className={`${
              activeTab === 'logs'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
          >
            Logs
          </button>
          <button
            onClick={() => setActiveTab('policy')}
            className={`${
              activeTab === 'policy'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
          >
            Policy
          </button>
        </nav>
      </div>

      {activeTab === 'logs' && (
        <div>
          <LogsFilters onFilterChange={setFilters} />
          <div className="bg-white rounded-lg shadow p-6">
            <LogsTable filters={filters} />
          </div>
        </div>
      )}

      {activeTab === 'policy' && (
        <div className="bg-white rounded-lg shadow p-6">
          <PolicyEditor />
        </div>
      )}
    </div>
  );
}


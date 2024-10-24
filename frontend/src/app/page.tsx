// frontend/src/app/page.tsx

'use client';

import React from 'react';
import SidebarComponent from '@/components/SidebarComponent';
import Dashboard from '@/components/pages/dashboard';
import ExpenseList from '@/components/pages/expenseList';
import Analysis from '@/components/pages/analysis';
import Images from '@/components/pages/images';
import PaymentMethods from '@/components/pages/paymentMethods';
import Subscriptions from '@/components/pages/subscriptions';
import ManualInput from '@/components/pages/manualInput';
import ImageInput from '@/components/pages/imageInput';
import { useState } from 'react';

export default function HomePage() {
  const [currentPage, setCurrentPage] = useState<string>('dashboard');

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'expenses':
        return <ExpenseList />;
      case 'analysis':
        return <Analysis />;
      case 'receipts':
        return <Images />;
      case 'payments':
        return <PaymentMethods />;
      case 'subscriptions':
        return <Subscriptions />;
      case 'manual-input':
        return <ManualInput />;
      case 'image-input':
        return <ImageInput />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen">
      <SidebarComponent setCurrentPage={setCurrentPage} />
      <main className="flex-1 p-6 bg-gray-100">
        {renderPage()}
      </main>
    </div>
  );
}
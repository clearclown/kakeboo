// frontend/src/components/SidebarComponent.tsx

'use client';

import React from 'react';
import { Button } from "@/components/ui/button";
import { LayoutDashboard, List, TrendingUp, Image, CreditCard, Repeat, FileText, Camera, DollarSign } from 'lucide-react';

export function SidebarComponent({ setCurrentPage }: { setCurrentPage: (page: string) => void }) {
  return (
    <aside className="w-64 bg-white p-4 shadow-md h-screen">
      <div className="flex items-center mb-6">
        <DollarSign className="h-6 w-6 mr-2 text-blue-500" />
        <h2 className="text-xl font-bold text-blue-700">FinanceManager</h2>
      </div>
      <nav className="space-y-2">
        <SidebarLink icon={<LayoutDashboard className="h-4 w-4" />} label="概要" onClick={() => setCurrentPage('dashboard')} />
        <SidebarLink icon={<List className="h-4 w-4" />} label="支出一覧" onClick={() => setCurrentPage('expenses')} />
        <SidebarLink icon={<TrendingUp className="h-4 w-4" />} label="分析" onClick={() => setCurrentPage('analysis')} />
        <SidebarLink icon={<Image className="h-4 w-4" />} label="レシート画像" onClick={() => setCurrentPage('receipts')} />
        <SidebarLink icon={<CreditCard className="h-4 w-4" />} label="支払い方法" onClick={() => setCurrentPage('payments')} />
        <SidebarLink icon={<Repeat className="h-4 w-4" />} label="サブスクリプション" onClick={() => setCurrentPage('subscriptions')} />
        <SidebarLink icon={<FileText className="h-4 w-4" />} label="手動入力" onClick={() => setCurrentPage('manual-input')} />
        <SidebarLink icon={<Camera className="h-4 w-4" />} label="画像入力" onClick={() => setCurrentPage('image-input')} />
      </nav>
    </aside>
  );
}

function SidebarLink({ icon, label, onClick }: { icon: React.ReactNode; label: string; onClick: () => void }) {
  return (
    <Button variant="ghost" className="w-full justify-start flex items-center" onClick={onClick}>
      {icon}
      <span className="ml-2">{label}</span>
    </Button>
  );
}

export default SidebarComponent;

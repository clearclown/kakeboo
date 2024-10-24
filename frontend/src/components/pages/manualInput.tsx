// frontend/src/components/pages/manualInput.tsx

'use client'

import React from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export function ManualInputComponent() {
  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    // Handle form submission
  };

  return (
    <div>
      <h1 className="text-3xl font-bold text-blue-700 mb-8">手動入力</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input type="date" placeholder="日付" />
          <Input type="time" placeholder="時間" />
          <Select>
            <SelectTrigger>
              <SelectValue placeholder="通貨の種類" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="jpy">日本円</SelectItem>
              <SelectItem value="usd">米ドル</SelectItem>
              {/* Add more currencies */}
            </SelectContent>
          </Select>
          <Input type="number" placeholder="合計金額" />
          <Select>
            <SelectTrigger>
              <SelectValue placeholder="支払い方法" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="cash">現金</SelectItem>
              <SelectItem value="credit">クレジットカード</SelectItem>
              <SelectItem value="debit">デビットカード</SelectItem>
              <SelectItem value="electronic">電子マネー</SelectItem>
            </SelectContent>
          </Select>
          <Input placeholder="支払い方法の詳細" />
          <Input placeholder="店名" />
          <Input placeholder="店の種類" />
          <Input placeholder="店の情報（電話番号等）" />
          <Input placeholder="場所" />
          <Input type="number" placeholder="人数" />
          <textarea className="col-span-2" placeholder="レシート全体像（Markdown形式）" rows={4}></textarea>
          <Input placeholder="備考" />
          <Select>
            <SelectTrigger>
              <SelectValue placeholder="レシートの状態" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="original">原本</SelectItem>
              <SelectItem value="copy">コピー</SelectItem>
              <SelectItem value="digital">デジタル</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Button type="submit">保存</Button>
      </form>
    </div>
  );
}

export default ManualInputComponent;
// frontend/src/components/pages/expenseList.tsx

'use client'

import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import apiClient from '@/utils/api';

// ExpenseListComponent: 支出一覧を表示するコンポーネント
export function ExpenseListComponent() {
  // デバッグ用メッセージ
  console.log("\x1b[33m[DEBUG] : ExpenseListComponent rendered\x1b[0m");

  // 支出データの状態を管理するためのuseStateフック
  const [expenses, setExpenses] = useState([]);

  // コンポーネントがマウントされたときに支出データを取得するためのuseEffectフック
  useEffect(() => {
    // デバッグ用メッセージ
    console.log("\x1b[33m[DEBUG] : Fetching expenses data\x1b[0m");

    // APIクライアントを使用して支出データを取得
    apiClient.get('/expenses')
      .then(response => {
        // デバッグ用メッセージ
        console.log("\x1b[33m[DEBUG] : Expenses data fetched successfully\x1b[0m");

        // 取得したデータを状態にセット
        setExpenses(response.data);
      })
      .catch(error => {
        // エラーメッセージをコンソールに出力
        console.error('支出データの取得中にエラーが発生しました', error);
      });
  }, []);

  // 取得したデータを用いてテーブルを表示
  return (
    <div>
      <h1 className="text-3xl font-bold text-blue-700 mb-8">支出一覧</h1>
      <div className="flex justify-between mb-4">
        <Input className="w-64" placeholder="検索..." />
        <Button>フィルター</Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>日付</TableHead>
            <TableHead>店名</TableHead>
            <TableHead>カテゴリー</TableHead>
            <TableHead>金額</TableHead>
            <TableHead>支払方法</TableHead>
            <TableHead>操作</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {/* 取得した支出データをマッピングしてテーブル行を生成 */}
          {expenses.map((expense, index) => (
            <TableRow key={index}>
              <TableCell>{expense.date}</TableCell>
              <TableCell>{expense.storeName}</TableCell>
              <TableCell>{expense.category}</TableCell>
              <TableCell>{expense.amount}</TableCell>
              <TableCell>{expense.paymentMethod}</TableCell>
              <TableCell>
                {/* 操作ボタンなどを配置 */}
                <Button>編集</Button>
                <Button>削除</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

export default ExpenseListComponent;
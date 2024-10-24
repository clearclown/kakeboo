// frontend/src/components/pages/dashboard.tsx

'use client'

import React, { useState, useEffect } from 'react';
import apiClient from '@/utils/api';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { FileText } from 'lucide-react';

const COLORS = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];

const expenseData = [
  { category: "食費", amount: 85000 },
  { category: "交通費", amount: 45000 },
  { category: "住居費", amount: 80000 },
  { category: "娯楽費", amount: 35678 },
];

export function DashboardComponent() {
  const [monthlyData, setMonthlyData] = useState([]);
  const [recentTransactions, setRecentTransactions] = useState([]);
  const [selectedCharts, setSelectedCharts] = useState(['total', 'food', 'transport', 'housing', 'entertainment']);
  const [selectedRange, setSelectedRange] = useState('6');

  useEffect(() => {
    apiClient.get('/expenses/monthly-summary?range=6')
      .then(response => {
        setMonthlyData(response.data);
        console.log('\x1b[33m%s\x1b[0m', '[DEBUG] : Monthly data fetched successfully', response.data);
      })
      .catch(error => {
        console.error('月別データの取得中にエラーが発生しました', error);
      });

    apiClient.get('/expenses/recent')
      .then(response => {
        setRecentTransactions(response.data);
        console.log('\x1b[33m%s\x1b[0m', '[DEBUG] : Recent transactions fetched successfully', response.data);
      })
      .catch(error => {
        console.error('最近の取引の取得中にエラーが発生しました', error);
      });
  }, []);

  const exportToPDF = () => {
    // Implement PDF export functionality here
    console.log('Exporting to PDF...');
  };

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold text-blue-700">ダッシュボード</h1>
        <Button onClick={exportToPDF}>
          <FileText className="mr-2 h-4 w-4" />
          PDFエクスポート
        </Button>
      </div>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-lg font-medium text-blue-700">月別支出推移</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="mb-4 flex items-center space-x-4">
            <Select value={selectedRange} onValueChange={setSelectedRange}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="表示期間" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="3">3ヶ月</SelectItem>
                <SelectItem value="6">6ヶ月</SelectItem>
                <SelectItem value="12">1年</SelectItem>
              </SelectContent>
            </Select>
            {['total', 'food', 'transport', 'housing', 'entertainment', 'cash', 'credit', 'electronic'].map((chart) => (
              <Button
                key={chart}
                variant={selectedCharts.includes(chart) ? "secondary" : "outline"}
                onClick={() => setSelectedCharts(prev =>
                  prev.includes(chart) ? prev.filter(c => c !== chart) : [...prev, chart]
                )}
              >
                {chart}
              </Button>
            ))}
          </div>
          <div className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyData.slice(-selectedRange)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                {selectedCharts.includes('total') && <Line type="monotone" dataKey="total" stroke="#8884d8" activeDot={{ r: 8 }} />}
                {selectedCharts.includes('food') && <Line type="monotone" dataKey="food" stroke="#82ca9d" />}
                {selectedCharts.includes('transport') && <Line type="monotone" dataKey="transport" stroke="#ffc658" />}
                {selectedCharts.includes('housing') && <Line type="monotone" dataKey="housing" stroke="#ff7300" />}
                {selectedCharts.includes('entertainment') && <Line type="monotone" dataKey="entertainment" stroke="#a4de6c" />}
                {selectedCharts.includes('cash') && <Line type="monotone" dataKey="cash" stroke="#8dd1e1" />}
                {selectedCharts.includes('credit') && <Line type="monotone" dataKey="credit" stroke="#82ca9d" />}
                {selectedCharts.includes('electronic') && <Line type="monotone" dataKey="electronic" stroke="#a4de6c" />}
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 mb-8 grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-medium text-blue-700">カテゴリー別支出</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={expenseData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="amount"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {expenseData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-medium text-blue-700">支払い方法別</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={monthlyData.slice(-1)[0]}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="cash" fill="#8884d8" name="現金" />
                  <Bar dataKey="credit" fill="#82ca9d" name="クレジットカード" />
                  <Bar dataKey="electronic" fill="#ffc658" name="電子マネー" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-medium text-blue-700">最近の取引</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>日付</TableHead>
                <TableHead>説明</TableHead>
                <TableHead>カテゴリー</TableHead>
                <TableHead>金額</TableHead>
                <TableHead>支払方法</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {recentTransactions.map((transaction, index) => (
                <TableRow key={index}>
                  <TableCell>{transaction.date}</TableCell>
                  <TableCell>{transaction.description}</TableCell>
                  <TableCell>{transaction.category}</TableCell>
                  <TableCell>{transaction.amount}</TableCell>
                  <TableCell>{transaction.method}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

export default DashboardComponent;

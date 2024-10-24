// frontend/src/components/pages/paymentMethods.tsx

'use client'

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ResponsiveContainer, PieChart, Pie, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export function PaymentMethodsComponent() {
  // Fetch payment method data here

  return (
    <div>
      <h1 className="text-3xl font-bold text-blue-700 mb-8">支払い方法</h1>
      <div className="grid gap-6 grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>支払い方法別割合</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                {/* Chart components */}
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>支払い方法別推移</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart>
                {/* Chart components */}
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default PaymentMethodsComponent;
